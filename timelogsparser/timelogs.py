import datetime
import re

class Timelogs:
    def __init__(self, file):
        self.file = file
        self.linenumber = 0
        self.line = None
        self.data = {}
        self.process()

    def processing_error(self, error_message):
        return Exception('%s at line %d: %s' % (error_message, self.linenumber, self.line))

    def process_date(self):
        tasks = []
        while True:
            line = unicode(self.readline().strip())
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
        self.task = self.readline().strip()
        self.rate = float(self.readline().strip())

        while True:
            line = self.readline()
            if line == '':
                print 'Finished processing file'
                return
            if line.strip() == '':
                continue
            match = re.match('(\w+ \d+,?( \d+)?)(( - )|\s+)((\d+)(\.\d+)?)( .*)?', self.line)
            if match:
                try:
                    date = datetime.datetime.strptime(match.group(1), '%b %d, %Y')
                except ValueError:
                    try:
                        current_year = datetime.date.today().year
                        date = datetime.datetime.strptime("%s, %d" % (match.group(1), current_year), '%b %d, %Y')
                    except ValueError:
                        raise self.processing_error('cannot parse date for header')
                total = float(match.group(5))
                key = datetime.datetime.strftime(date, '%Y-%b-%d')
                if key in self.data:
                    raise self.processing_error('duplicate date')
                try:
                    tasks = self.process_date()
                except UnicodeDecodeError:
                    raise self.processing_error('non-unicode compatible character')
                else:
                    self.data[key] = {'total': total, 'tasks': tasks}
            else:
                raise self.processing_error('malformed header')

    def pretty_print(self):
        total = 0
        keys = sorted(self.data.keys())
        print self.task
        for date in keys:
            log = self.data[date]
            total = total + log['total']
            if log['total'] > 0:
                print '%s: %.2f hours' % (date, log['total'])
                for task in log['tasks']:
                    print task
                print
        print "Total (%d days): %.2f hours" % (len(keys), total)    

    def print_summary(self):
        print self.task
        total = 0
        for date in self.data.keys():
            log = self.data[date]
            total = total + log['total']
        print "Total (%d days): %.2f hours" % (len(keys), total)
