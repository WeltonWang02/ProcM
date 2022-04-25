"""
  Execute OS commands
"""
import subprocess
import asyncio

def exec_shell(command : str, cwd : str = None):
    """
      Execute a OS command
  
      @params
        command = Required : list of arguments for command
        cwd = Optional : working directory
      @return
        (string) stdout if stderr is empty, else stderr 
    """
    command = command.split(" ")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)

    if result.stderr:
      return result.stderr.decode()
      
    return result.stdout.decode()

async def async_exec_shell(command : str, cwd : str = None):
    """
      async version of exec_shell
  
      @params
        command = Required : list of arguments for command
        cwd = Optional : working directory
      @return
        (string) stdout if stderr is empty, else stderr 
    """
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=cwd
    )

    stdout, stderr = await process.communicate()
    
    if stderr:
      return stderr.decode().strip()
      
    return stdout.decode().strip()