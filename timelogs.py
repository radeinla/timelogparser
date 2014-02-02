import datetime
import re
import sys


class TimelogReader:
    def __init__(self, file):
        self.file = file
        self.linenumber = 0
        self.line = None
        self.timelogs = {}

    def processing_error(self, error_message):
        return Exception('%s at line %d: %s' % (error_message, self.linenumber, self.line))

    def process_date(self):
        tasks = []
        while True:
            line = self.readline()
            if line.strip() == '':
                break
            else:
                match = re.match('\d+\. (.*)', line)
                if match:
                    tasks.append(match.group(1))
                else:
                    tasks.append(line)
        return tasks

    def readline(self):
        self.line = self.file.readline()
        self.linenumber = self.linenumber + 1
        return self.line

    def process(self):
        while True:
            line = self.readline()
            if line == '':
                print 'Finished processing file'
                return
            if line.strip() == '':
                continue
            match = re.match('(\w+ \d+,?( \d+)?)(( - )|\s+)(\d+) .*', self.line)
            if match:
                try:
                    date = datetime.datetime.strptime(match.group(1), '%b %d, %Y')
                except ValueError:
                    raise self.processing_error('cannot parse date for header')
                total = float(match.group(5))
                key = datetime.datetime.strftime(date, '%Y-%b-%d')
                if key in self.timelogs:
                    raise self.processing_error('duplicate date')
                self.timelogs[key] = {'total': total, 'tasks': self.process_date()}
            else:
                raise self.processing_error('malformed header')

    def pretty_print(self):
        total = 0
        keys = sorted(self.timelogs.keys())
        for date in keys:
            log = self.timelogs[date]
            total = total + log['total']
            if log['total'] > 0:
                print '%s: %.2f hours' % (date, log['total'])
                for task in log['tasks']:
                    print task
                print
        print "Total (%d days): %.2f hours" % (len(keys), total)    


def main(argv):
    filenames = argv
    # today = datetime.date.today()
    # print today
    for filename in filenames:
        print 'processing %s' % filename
        with open(filename, 'r') as timelogs_file:
            timelog_reader = TimelogReader(timelogs_file)
            timelog_reader.process()
            print '#######################################'
            timelog_reader.pretty_print()
            print '\n'*7


if __name__ == "__main__":
    main(sys.argv[1:])
