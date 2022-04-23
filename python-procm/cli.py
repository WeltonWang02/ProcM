import sys, argparse
import os 

def run_command(parser, args):
    """
        Handle command parsing and function calls
    """
    if args.command == "core":
        pass
    else if args.command == "procm":
        pass
    else:
        print("Invalid command called.")

def run():
  """
    Main function routine
  """
  args = sys.argv
  
  parser = argparse.ArgumentParser(prog='cli.py', description='Manage and monitor python processes', epilog="See '<command> --help' for options.")
  subparsers = parser.add_subparsers(dest='command', help='Commands')

  core_parser = subparsers.add_parser('core', help='Manage runtime status')
  core_parser.add_argument("--disable", action='store_true', help="Disables auto-startup at boot")
  core_parser.add_argument("--enable", action='store_true', help="Enable auto-startup at boot")
  core_parser.add_argument("--init", action='store_true', help="Initilizes system-d service if not created")
  core_parser.set_defaults(func=run_command)

  proc_parser = subparsers.add_parser('procm', help='Manage process')
  proc_parser.add_argument('-l', '--list', action='store_true', required=False, help='List managed processes')
  proc_parser.add_argument('--stop-all', action='store_true', required=False, help='Stop all running processes')
  proc_parser.add_argument('--start-all', action='store_true', required=False, help='Start all stopped processes')
  proc_parser.add_argument('--restart-all', action='store_true', required=False, help='Restart all processes')
  proc_parser.add_argument('-a', '--add', required=False, help='Add a process by full path')
  proc_parser.add_argument('-h', '--holdoff', required=False, help='Used with -a, set holdoff time between restarts')
  proc_parser.add_argument('-d', '--delete', required=False, help='Delete a process by full path')
  proc_parser.add_argument('-r', '--restart', required=False, help='Restart process(es) by partial path match')
  proc_parser.add_argument('-d', '--delete', required=False, help='Delete a process by full path')
  proc_parser.set_defaults(func=run_command)
    
  args = parser.parse_args()

  if args.command is not None:
      args.func(parser, args)
  else:
      parser.print_help()

if __name__ == "__main__":
  run()