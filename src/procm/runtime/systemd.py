"""
  Handles systemd file management
"""
import os
from .utils.command import exec_shell

def detect_systemd():
    """
      Detected if a valid systemd file is present for procm

      @return
        (bool) if systemd file is present and valid
    """
    if os.path.isfile("/usr/lib/systemd/system/python-procm.service") and not exec_shell("systemd-analyze verify python-procm.service"):
      return True
    return False

def write_systemd():
  """
    Writes systemd file

    @return
      None
  """
  curr_dir = os.path.realpath(__file__).replace("/runtime/systemd.py", "")
  file = ("[Unit]\n"
          "Description=Python-procm worker runner service\n"
          "After=multi-user.target\n\n"
          "[Service]\n"
          "Type=idle\n"
          "User=root\n"
          f"ExecStart=/usr/bin/python3 {curr_dir}/service.py\n"
          "Restart=always\n"
          "TimeoutStartSec=10\n"
          "RestartSec=10\n\n"
          "[Install]\n"
          "WantedBy=multi-user.target\n")
  
  with open("/usr/lib/systemd/system/python-procm.service", 'w') as f:
    f.write(file)


def set_systemd(status : bool):
  """
    Enables or disables the systemd service

    @params
      status = Required : to enable or disable service
    @return
      (bool) if successful
  """
  if detect_systemd():
    if status:
      exec_shell("systemctl enable python-procm.service")
      exec_shell("systemctl start python-procm.service")
    else:
      exec_shell("systemctl disable python-procm.service")
      exec_shell("systemctl stop python-procm.service")
    return True
  return False 
