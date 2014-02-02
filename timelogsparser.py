import argparse
import sys
from refreshbooks import api
from timelogs import Timelogs


parent_parser = argparse.ArgumentParser(description="Timelogs Processor", add_help=False)
parent_parser.add_argument('files', nargs='*', help='file sources')
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')
freshbooks_subparser = subparsers.add_parser('freshbooks', parents=[parent_parser])
freshbooks_subparser.add_argument('--endpoint', dest='endpoint',
    type=str, required=True, default=None,
    help='Freshbooks api endpoint')
freshbooks_subparser.add_argument('--token', dest='token', 
    type=str, required=True, default=None,
    help='Freshbooks api token')
freshbooks_subparser.add_argument('--client-id', dest='client_id', 
    type=int, required=True, default=None,
    help='Freshbooks client for invoicing')
files_subparser = subparsers.add_parser('parse', parents=[parent_parser])

def send_to_freshbooks(timelogs, client):
    print 'sending to freshbooks'

def main(argv):
    args = parser.parse_args(argv)
    timelogs = []
    for filename in args.files:
        print 'processing %s' % filename
        with open(filename, 'r') as timelogs_file:
            timelogs.append(Timelogs(timelogs_file))
    for t in timelogs:
        print '############# START #############'
        t.pretty_print()
        print '############## END ##############'
    if args.subcommand == 'freshbooks':
        if raw_input("send to freshbooks? ").lower().startswith('y'):
            client = api.TokenClient(args.endpoint, 
                args.token, 
                user_agent='radeinla/timelogparser')
            send_to_freshbooks(timelogs, client)

if __name__ == "__main__":
    main(sys.argv[1:])
