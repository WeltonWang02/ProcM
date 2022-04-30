
# Python ProcM

A simple, reliable python process manager

## Purpose
Managing the lifecycle of scripts, ensuring they run after reboot/crash
## Usage
Clone the repository and install dependencies, then setup the cli:
```bash
git clone https://github.com/WeltonWang02/ProcM.git
cd ProcM
pip3 install -r requirements.txt
chmod +x src/procm-cli
```
Setup the systemd service:

```bash
./procm-cli core --init
./procm-cli core --enable
```
Now use the cli to manage scripts:
```bash
# ./procm-cli procs --help
usage: procm-cli procs [-h] [-l] [--stop-all] [--start-all] [--restart-all]
                    [-a ADD] [-d] [-r] [-dl] [-el] [-s] [-t]
                    [--runtime RUNTIME] [--name NAME] [--path PATH]

optional arguments:
  -h, --help         show this help message and exit
  -l, --list         List managed processes
  --stop-all         Stop all running processes
  --start-all        Start all stopped, enabled processes
  --restart-all      Restart all enabled processes
  -a ADD, --add ADD  Add a process by full path
  -d, --delete       Delete a process. Use with --name or --path
  -r, --restart      Restart process(es. Use with --name or --path
  -dl, --disable     Delete a process. Use with --name or --path
  -el, --enable      Restart process(es. Use with --name or --path
  -s, --start        Start process(es. Use with --name or --path
  -t, --stop         Stop process(es. Use with --name or --path
  --runtime RUNTIME  [--add] : Set runtime interpreter path. Default:
                     /usr/bin/python3
  --name NAME        [--add, --delete, --restart] : Set/filter by full process
                     name. Default: filename
  --path PATH        [--delete, --restart] : Filter by partial process path
  --pwd PATH         [--add] : Set the pwd when running the script
```
A config file is located in ~/procm_config.json

## Examples

**Case:** Setup a script located at /home/user/script.py called "Script"

**Run:** `./procm-cli procs --add /home/user/script.py --name Script`

**Case:** Setup a script located at /home/user/script.py called "Script" running Python 2

**Run:** `./procm-cli procs --add /home/user/script.py --name Script --runtime /usr/bin/python2`

**Case:** Delete a script called "Script"

**Run:** `./procm-cli procs --delete --name Script`

**Case:** Delete all scripts that run the file script.py

**Run:** `./procm-cli procs --delete --path script.py`

**Case:** Disable (prevent run at startup) all scripts that run the file script.py

**Run:** `./procm-cli procs --disable --path script.py`

**Case:** Restart all processes

**Run:** `./procm-cli procs --restart-all`

**Case:** Stop all "disabled" processes

**Run:** `./procm-cli procs --stop-all && ./procm-cli procs --start-all`

## TODO
- Run-as user support
## Requirements
- Unix based OS with systemd
- Python 3.6+
- `tabulate` and `psutils` packages
- Root permissions
