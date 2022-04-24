"""
  Systemd service class. 

  Monitors, restarts, manages processes
"""
from runtime.config import *
from runtime.process import *
from runtime.socket import *
from runtime.core import *

import time
import asyncio

class Service:

  def __init__(self):
    """ Run init tasks, start 'enabled' processes """
    self.socket = Socket(self.process_message)
    self.processes = fetch_processes()
        
  async def listen(self):
    """
      Listens on the socket and processes messages. Runs forever

      @return 
        None
    """
    await asyncio.wait([self.socket.async_listen(), # run in background
                        self.manage_procs()])
    
  def get_proc(self, name : str):
    """
      Given a name, return the process or false

      @params
        name = Required : name of the process to return 
      @return
        (bool or Process) object or False
    """
    for proc in self.processes:
      if proc.name == name:
        return proc
    return False

  async def __run_routine(self, tasks : list):
    """
      Runs a list of routines, exiting if empty. Needed to address asyncio.wait empty list blocking
    
      @params
        task = Required : list of routines
      @return
        None
    """
    if len(tasks) > 0:
      await asyncio.wait(tasks)
  
  async def process_message(self, message : str):
    """
      Process a message received from a socket

      @params
        message = Required : message to process
      @return
        None
    """
    if message == "r":
      """ Reload the process list """
      self.processes = fetch_processes()
      
    elif "restart " in message:
      """ restart the proc given 'restart <procname>' """
      proc = self.get_proc(message.split()[1])
      if proc:
        await proc.restart()
        
    elif "start " in message:
      """ starts the proc given 'start <procname>' - must go after restart"""
      proc = self.get_proc(message.split()[1])
      if proc:
        await proc.start()
        
    elif "stop " in message:
      """ stop the proc given 'stop <procname>' """
      proc = self.get_proc(message.split()[1])
      if proc:
        await proc.stop()
  
    elif "stop-all" in message:
      """ halt everything """
      tasks = []
      for proc in self.processes:  # can we optimize these three loops?
        tasks.append(asyncio.get_event_loop().create_task(proc.stop()))
      await self.__run_routine(tasks)
        
    elif "restart-all" in message:
      """ restart everything """
      tasks = []
      for proc in self.processes:
        if proc.proc_stat:
          tasks.append(asyncio.get_event_loop().create_task(proc.restart()))
      await self.__run_routine(tasks)
        
    elif "start-all" in message:
      """ start everything """
      tasks = []
      for proc in self.processes: 
        if proc.proc_stat:
          tasks.append(asyncio.get_event_loop().create_task(proc.start()))
      await self.__run_routine(tasks)

  async def poll_procs(self):
    """
      Runs poll on all processes

      @return 
        None
    """    
    for proc in self.processes:
      proc.poll()
      
  async def restart_stopped(self):
    """
      Loop through procs and restart stopped ones, assuming it was not manually stopped (status = "STOPPED")

      @return 
        None
    """
    tasks = []

    for proc in self.processes:
      if proc.running == False and proc.proc_stat:
        tasks.append(asyncio.get_event_loop().create_task(proc.start()))

    await self.__run_routine(tasks)
  
  async def manage_procs(self):
    """
      Manages and monitors processes

      @return 
        None
    """
    while True:
      await self.poll_procs()
      await self.restart_stopped()
      await asyncio.sleep(2)

if __name__ == "__main__":
  """
    Run forever
  """
  service = Service()
  loop = asyncio.get_event_loop()
  loop.run_until_complete(service.listen())
  loop.close()
