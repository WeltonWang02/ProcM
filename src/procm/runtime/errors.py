class ConfigFileError(Exception):
  """
    Error reading or process file
  """
  pass

class WorkerConnectionError(Exception):
  """
    Error connecting to the service socket
  """
  pass

class ProcessHandlerError(Exception):
  """
    Error launching process
  """
  pass