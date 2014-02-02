import argparse
import sys
from timelogs import Timelogs


parser = argparse.ArgumentParser(description="Timelogs Processor")
parser.add_argument('--freshbooks-endpoint', dest='freshbooks_endpoint', type=str, default=None, help='Freshbooks api endpoint')
parser.add_argument('--freshbooks-token', dest='freshbooks_token', type=str, default=None, help='Freshbooks api token')
parser.add_argument('files', nargs='*', default=None, help='Freshbooks api endpoint')

def send_to_freshbooks(timelogs):
    print 'sending to freshbooks'

def main(argv):
    args = parser.parse_args(argv)
    print args
    # filenames = argv
    # today = datetime.date.today()
    # print today
    timelogs = []
    for filename in args.files:
        print 'processing %s' % filename
        with open(filename, 'r') as timelogs_file:
            timelogs.append(Timelogs(timelogs_file))
    for t in timelogs:
        print '############# START #############'
        t.pretty_print()
        print '############## END ##############'
    if raw_input("send to freshbooks? ").lower().startswith('y'):
        if not args.freshbooks_endpoint:
            print 'please specify freshbooks-endpoint'
            return
        if not args.freshbooks_token:
            print 'please specify freshbooks-token'
            return
        send_to_freshbooks(timelogs)

if __name__ == "__main__":
    main(sys.argv[1:])
