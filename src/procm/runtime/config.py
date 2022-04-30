"""
  Initialize a config class that reads a json file from ~/
"""
import os
import json
from .errors import *

class Config():
  
  def __init__(self):
    """
      Initialized full file path as variable and reads and loads config file if exists

      @return
        None
    """
    self.file = os.path.expanduser('~/procm_config.json')
    self.reload()

  def __repr__(self):
    """
      String representation as config dict

      @return
        (dict) config dict
    """
    return self.config

  def __match(self, crit : dict, p : dict):
    """
      Determine if a process p matches criteria crit

      @params
        crit = Required : criteria to match by
        p = Required : process to check against
      @return
        (bool) true if process matches
    """
    return (crit.get('path') and crit.get('path') in p['path']) or (crit.get('name') and crit.get('name') == p['name']) or crit.get('all') == True

  def validate(self):
    """
      Determine if config file is valid

      @return
        None
    """
    if not 'processes' in self.config:
      raise ConfigFileError("Invalid config file: missing 'processes' key")

    for process in self.config['processes']:
      # ensure required keys are present  
      keys = ['path', 'status', 'name']
      missing = list(set(keys) - set(process.keys()))
      if len(missing) > 0:
        raise ConfigFileError(f"Invalid config file process item: missing {missing} key in: {process}")

      # ensure system users exist
      if 'user' in process:
        try:
            pwd.getpwnam(process['user'])
        except KeyError:
            raise ConfigFileError(f"Invalid config file process item: invalid user {process['user']} specified in: {process}")

      # ensure pwds exist
      if 'pwd' in process and not os.path.isfile(process['pwd']):
        raise ConfigFileError(f"Invalid config file process item: invalid working directory {process['pwd']} specified in: {process}")

    
  def reload(self):
    """
      Re-reads the config file and updates config variable

      @return
        None
      @raises
        ConfigFileError is config file is invalid
    """
    if os.path.isfile(self.file):
      with open(self.file, 'r') as f:
        try:
          self.config = json.load(f)
          self.validate()
        except json.decoder.JSONDecodeError as e:
          raise ConfigFileError(f"Invalid config file: {str(e)}")
    else:
      self.config = {"processes":[]}

  def write(self):
    """
      Writes config dict to config file

      @return
        None
    """
    with open(self.file, 'w') as f:
      json.dump(self.config, f)

  def check_exist(self, proc : dict):
    """
      Checks if a process currently exists in the system

      @args
        proc = Required : process dictionary 
      @return
        (bool) true if exists
    """
    return any([ process['name'] == proc['name'] for process in self.config['processes']])

  def append_proc(self, proc : dict):
    """
      Appends a process to the configuration file

      @params
        proc = Required : process dictionary
      @return
        (bool, string) true on success (no duplicate, invalid keys), error message otherwise
    """
    if not self.check_exist(proc):
      keys = ['path', 'status', 'name']
      missing = list(set(keys) - set(proc.keys()))
      
      if len(missing) == 0:
        if os.path.isfile(proc['path']):
          self.config['processes'].append(proc)
          self.write()
          return True
        return "ERROR: Script does not exist"
      else:
        return "ERROR: Invalid process passed"
        
    return "ERROR: Process under that name already exists"

  def delete_proc(self, criteria : dict):
    """
      Deletes a process by given criteria

      @params
        criteria = Required : either path or name defined
      @return 
        (list) deleted procs
    """
    removed = [l for l in self.config['processes'] if not self.__match(criteria, l) ]

    c = self.get_procs(criteria)
    
    self.config['processes'] = removed
    self.write()
    return c

  def toggle_proc(self, criteria : dict, status : bool):
    """
      Toggles process statuses by given criteria

      @params
        criteria = Required : either path or name defined
        status = Required : enable / disable
      @return 
        (int) modified procs
    """
    c = 0 
    
    for i in range(len(self.config['processes'])):
      if self.__match(criteria, self.config['processes'][i]):
        self.config['processes'][i]['status'] = status
        c += 1

    self.write()

    return c
      
  def get_procs(self, criteria : dict):
    """
      Returns processes by given criteria, only valid ones

      @params
        criteria = Required : either path or name defined
      @return 
        (dict) process data
    """
    possible_procs = [ l for l in self.config['processes'] if self.__match(criteria, l) ]
    return  [ p for p in possible_procs if os.path.isfile(p['path']) ]

  def get_broken_procs(self, criteria : dict):
    """
      Returns processes by given criteria, only broken (no file) ones

      @params
        criteria = Required : either path or name defined
      @return 
        (dict) process data
    """
    possible_procs = [ l for l in self.config['processes'] if self.__match(criteria, l) ]
    return  [ p for p in possible_procs if not os.path.isfile(p['path']) ]
    
        
        