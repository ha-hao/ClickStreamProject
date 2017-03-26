import os
import classifier
from datetime import datetime, timedelta
from tld import get_tld

class preProcessor:
    def __init__(self):
        self.classifier = classifier()
        self.start_date = ""
        self.end_date = ""
        self.data_dir = ""

    def __init__(self, classifier, start_month, end_month, data_dir):
        self.classifier = classifier
        self.start_date = start_month
        self.end_date = end_month
        self.data_dir = data_dir

    def split_files_by_hours(self):
        for single_date in daterange(self.start_date, self.end_date):
            filepath = os.path.join(self.data_dir,  single_date.strftime("%Y%m%d"))
            with open(filepath, "r") as f:
                self.split_file(self, f)
            f.close()

    def construct_instructions(self, n):
        for single_date in daterange(self.start_date, self.end_date):
            filepath = os.path.join(self.data_dir,  single_date.strftime("%Y%m%d"))
            for i in range(23):
                filepath += format(i, '02d')
                with open(filepath, "r") as f:
                    self.construct_active_map_instructions(self, f, n)
                f.close()

    def split_file(self, f):
        #splitting, get useful domains, extract domains
        filenpaths = []
        for i in range(23):
            filenpaths.append(os.path.join(self.data_dir, (f.names[:8] + format(i, '02d'))))

        files = []
        try:
            for i in filenpaths:
                files.append(open(i, 'w'))

            for line in f:
                linelist = line.split("\t")
                domain = get_tld(linelist[0], fix_protocol=True)
                hour = get_hour(int(linelist[6]))
                if self.in_target_site(domain):
                    files[hour].write(line)
        finally:
            for i in files:
                i.close()

    def construct_active_map_instructions(self, f, n):
        end_time_file_path = os.path.join(self.data_dir, f.names[:10] + "i")
        start_time_file_path = os.path.join(self.data_dir, get_start_date(f.names[:10], n) +"i")
        with open(end_time_file_path, write_append(end_time_file_path)) as fe, \
                open(start_time_file_path, write_append(start_time_file_path)) as fs:
            for line in f:
                linelist = line.split()
                if self.classifier.checkout_match(linelist[0],linelist[2]):
                    fe.write("-" + linelist[6] + "_" + linelist[0] + "\n")
                    fs.write(linelist[6] + "_" + linelist[0] + "\n")
        fe.close()
        fs.close()


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def write_append(filepath):
    if os.path.exists(filepath):
        return 'a'
    else:
        return 'w'


def get_start_date(endtime, n):
    return (datetime.strptime(endtime, '%Y%m%d%H') - timedelta(days = n)).strftime('%Y%m%d%H')


def get_hour(ss2k):
    return (ss2k/86400)/24


def get_ss2k(date_in_string):
    return (datetime.strptime(date_in_string, '%Y%m%d') - datetime.strptime("19991231", '%Y%m%d')).seconds


