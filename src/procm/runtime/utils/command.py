"""
  Execute OS commands
"""
import subprocess
import asyncio
import os, pwd
from .errors import *

def exec_shell(command : str, cwd : str = None, user : str = "root"):
    """
      Execute a OS command
  
      @params
        command = Required : list of arguments for command
        cwd = Optional : working directory
        user = Optional : username of user to drop to
      @return
        (string) stdout if stderr is empty, else stderr 
    """
    command = command.split(" ")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, preexec_fn=drop_perms(user))

    if result.stderr:
      return result.stderr.decode()
      
    return result.stdout.decode()

async def async_exec_shell(command : str, cwd : str = None, user : str = "root"):
    """
      async version of exec_shell
  
      @params
        command = Required : list of arguments for command
        cwd = Optional : working directory
        user = Optional : username of user to drop to
      @return
        (string) stdout if stderr is empty, else stderr 
    """
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=cwd, preexec_fn=drop_perms(user)
    )

    stdout, stderr = await process.communicate()
    
    if stderr:
      return stderr.decode().strip()
      
    return stdout.decode().strip()

def drop_perms(user : str):
  """
    setuid/guid to another user, dropping permissions

    @params
      user = Required : username of user to drop to
    @return
      (function) function to execute
  """
  try:
    pwdu = pwd.getpwnam(user)
  except KeyError:
    raise ProcessHandlerError(f"Error running as {user}. Halted.")

  def func():
    """wrapper function"""
    os.setgid(pwdu.pw_uid)
		os.setuid(pwdu.pw_gid)
    env = os.environ.copy()
    env.update({'HOME': pwdu.pw_dir, 'LOGNAME': user, 'USER': user})

  return func
