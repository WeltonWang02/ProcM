from .utils.command import exec_shell, async_exec_shell
import os, signal, psutil, time, asyncio

class Process:

  def __init__(self, name : str, path : str, status : bool, runtime : str = "/usr/bin/python3"):
    """
      Initialize variables

      @params
        name = Required : name of the process
        path = Required : path to script
        runtime = Optional : runtime executor, defaults to python3
      @return
        None
    """
    self.name = name
    self.file = path
    self.proc_stat = status
    self.inter = runtime
    self.running = False
    self.poll()

  def __repr__(self):
    """
      iterable representation of object

      @return
        (dict) process path, status, run status, and runtime
    """
    return str({"name":self.name, "path": self.file, "status": self.proc_stat, "runtime": self.inter, "running": self.running})

  def __iter__(self):
    """
      iterable representation of object

      @return
        (list) dict keys
    """
    enabled = "Enabled" if self.proc_stat else "Disabled"
    return iter([self.name, self.file, enabled, self.inter, self.running])

  def poll(self):
    """
      Determine if a process is running, refreshes variables

      @return
        (bool) running
    """
    if psutil.pid_exists(getattr(self, 'pid', -1)):
      return self.pid
    
    pid = exec_shell(f"pidof -s procm_p_{self.name}")

    self.running = (not pid == "") if self.running != "STOPPED" else self.running
    self.pid = -1 if pid == "" else int(pid)

    return (not pid == "")

  async def __block_til_stopped(self):
    """
      Wait 5 seconds for process to stop. If not stopped, then kill it with SIGKILL

      @return 
        None
    """
    time = 0
    
    while time < 5:
      await asyncio.sleep(0.1) # poll every 0.1 second

      if not self.poll():
        return

      time += 0.1

    os.kill(self.pid, signal.SIGKILL)

  async def start(self):
    """
      Start the process if not currently running

      @return
        None
    """    
    self.poll()
    
    if self.running != True:
      await async_exec_shell(f"nohup bash -c 'exec -a procm_p_{self.name} {self.inter} {self.file}' >/dev/null 2>&1 &")
      self.running = True
      self.poll()
        
  async def restart(self):
    """
      Restart the process, even if running

      @return
        None
    """
    await self.stop(signal.SIGTERM) # SIGTERM 
    await self.start()
    
  async def stop(self, sig : signal = signal.SIGTERM):
    """
      Stops the process

      @return
        None
    """
    self.poll()

    if self.running == True:
      os.kill(self.pid, sig)
    
    self.running = "STOPPED"

    await self.__block_til_stopped()
    

    

    

    
