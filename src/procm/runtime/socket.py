import socket
import sys, os
import asyncio
from .errors import *

class Socket:

  def __init__(self, proc : type(lambda x : None) = None):
    self.socket_path = "/var/run/procm.sock"
    self.socket = None
    self.func = proc

  def bind(self):
    """
      Binds to the UDS

      @return
        None
    """
    if os.path.exists(self.socket_path):
      os.remove(self.socket_path)

    self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    self.socket.bind(self.socket_path)
    os.chmod(self.socket_path, 0o700)

  def listen(self, callback : type(lambda x: None)):
    """
      Listens on the bound socket

      @params
        callback = Required : a function to run on response
      @return
        None
    """
    if self.socket:
      while True:
        data = self.socket.recv(1024)

        if len(data) > 0:
          callback(data.decode())

  async def async_listen(self):
    """
      Start a UDS socket that is async

      @return
        None
    """
    if os.path.exists(self.socket_path):
      os.remove(self.socket_path)
      
    self.socket = await asyncio.start_unix_server(self.async_process, path=self.socket_path)
    os.chmod(self.socket_path, 0o700)
    async with self.socket:
        await self.socket.serve_forever()

  async def async_process(self, r : asyncio.StreamReader, w : asyncio.StreamWriter):
    """
      Handles async socket message processing

      @params
        r = Required : streamreader
        w = Required : streamwriter
      @return
        None
    """
    request = (await r.read(1024)).decode('utf8')
    await self.func(request)
    

  def send(self, message : str):
    """
      Send a message to the socket.

      @params
        message = Required : the message to send
      @return
        None
      @raises
        WorkerConnectionError is connection fails
    """
    try:
      with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(self.socket_path)
        
        client.send(message.encode())
        client.close()
    except (ConnectionRefusedError) as e:
      raise WorkerConnectionError("Connection to worker refused. Is the service running?")

  
          

      

    

