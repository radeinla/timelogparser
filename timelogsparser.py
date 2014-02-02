import argparse
import sys
from refreshbooks import api
from timelogs import Timelogs


parent_parser = argparse.ArgumentParser(description="Timelogs Processor", add_help=False)
parent_parser.add_argument('files', nargs='*', help='file sources', type=argparse.FileType('r'))
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')
freshbooks_subparser = subparsers.add_parser('freshbooks', parents=[parent_parser], 
    help='Parse, merge and send to freshbooks as draft invoice')
freshbooks_subparser.add_argument('--endpoint', dest='endpoint',
    type=str, required=True, default=None,
    help='Freshbooks api endpoint')
freshbooks_subparser.add_argument('--token', dest='token', 
    type=str, required=True, default=None,
    help='Freshbooks api token')
freshbooks_subparser.add_argument('--client-id', dest='client_id', 
    type=int, required=True, default=None,
    help='Freshbooks client_id for invoicing')
files_subparser = subparsers.add_parser('parse', parents=[parent_parser], 
    help='Only parse and merge files for further processing')

def send_to_freshbooks(employee_timelogs, client_id, freshbooks_client):
    print 'sending to freshbooks'
    client_response = freshbooks_client.client.get(client_id=client_id)
    print 'creating invoice for %s %s (%s)' % (
        client_response.client.first_name, 
        client_response.client.last_name, 
        client_response.client.organization
    )
    lines = []
    for employee_timelog in employee_timelogs:
        for key in sorted(employee_timelog.data.keys()):
            day = employee_timelog.data[key]
            if day['total'] > 0:
                description = '\n'.join(day['tasks'])
                lines.append(api.types.line(
                    name=employee_timelog.task,
                    unit_cost=employee_timelog.rate,
                    quantity=day['total'],
                    description="[%s]\n%s" % (key, description)
                ))
    freshbooks_client.invoice.create(
        invoice = dict(
            client_id=client_id,
            status='draft',
            currency_code='USD',
            language='en',
            lines=lines
        )
    )


def main(argv):
    args = parser.parse_args(argv)
    employee_timelogs = []
    for timelogs_file in args.files:
        print 'processing %s' % timelogs_file.name
        employee_timelogs.append(Timelogs(timelogs_file))
    for t in employee_timelogs:
        print '############# START #############'
        t.pretty_print()
        print '############## END ##############'
    if args.subcommand == 'freshbooks':
        if raw_input("send to freshbooks? ").lower().startswith('y'):
            freshbooks_client = api.TokenClient(args.endpoint, 
                args.token, 
                user_agent='github/radeinla/timelogparser')
            send_to_freshbooks(employee_timelogs, args.client_id, freshbooks_client)

if __name__ == "__main__":
    main(sys.argv[1:])
