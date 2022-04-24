from .errors import *
from .config import *
from .process import *
from .socket import *

config = Config()
socket = Socket()

def fetch_processes():
  """
    Retrieves and returns the status of working process listed in config file

    @return
      (list) proccess objects
  """
  config.reload()
  return [Process(**proc) for proc in config.get_procs({"all": True})]

def fetch_broken_processes():
  """
    Retrieves and returns the status of broken process listed in config file

    @return
      (list) proccess objects
  """
  config.reload()
  return [Process(**proc) for proc in config.get_broken_procs({"all": True})]

def append_process(proc : dict):
  """
    Adds a process to config, and calls service mon reload

    @params
      proc = Required : dictionary of process
    @return
      (string) response message
  """
  append = config.append_proc(proc)
  
  if append == True:
    socket.send("r")
    return "Successfully added process"
  else:
    return append

def delete_processes(proc : dict):
  """
    Deletes a process from config, stops process, and calls service mon reload

    @params
      proc = Required : dictionary/criteria for process deletion
    @return
      (int) number of delete processes
  """
  deleted = config.delete_proc(proc)

  for proc in deleted:
    socket.send(f"stop {proc.name}")
    
  socket.send("r")
  return len(deleted)


def manage_processes(proc : dict, action : str):
  """
    Manages each process match the criteria

    @params
      proc = Required : dictionary/criteria for process start
      action = Required : action 
    @return
      (int) number of processes managed
  """
  procs = config.get_procs(proc)
  
  for proc in procs:
    if action in ["start", "stop", "restart"]:
      socket.send(f"{action} {proc['name']}")

  return len(procs)

def manage_all_processes(action : str):
  """
    Manages each process match the criteria

    @params
      action = Required : action 
    @return
      None
  """
  if action in ["start", "stop", "restart"]:
    socket.send(f"{action}-all")

def toggle_processes(proc : dict, action : bool):
  """
    Toggles the startup status of a process. Helper function for config.toggle_proc

    @params
      proc = Required : process match criteria
      action = Required : enable / disable
    @return
      (int) procs affected
  """
  mod = config.toggle_proc(proc, action)
  socket.send("r")
  return mod
