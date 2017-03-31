import os
import classifier
from datetime import datetime, timedelta
from tld import get_tld
import glob
import gzip


class preProcessor:
    def __init__(self):
        self.classifier = classifier()
        self.start_date = ""
        self.end_date = ""
        self.data_dir = ""
        self.tempdata_dir = ""

    def __init__(self, classifier, start_month, end_month, data_dir):
        self.classifier = classifier
        self.start_date = datetime.strptime(start_month, '%Y%m%d')
        self.end_date = datetime.strptime(end_month, '%Y%m%d')
        self.data_dir = data_dir
        self.tempdata_dir = data_dir + "/temp_data"
        if not os.path.exists(self.tempdata_dir):
            os.makedirs(self.tempdata_dir)

    def split_files_by_hours(self):
        for single_date in daterange(self.start_date, self.end_date):
            #filepath = os.path.join(self.data_dir,  single_date.strftime("%Y%m%d"))
            filepath = os.path.join(os.path.join(self.data_dir,  single_date.strftime("%Y%m")),single_date.strftime("%Y%m%d"))
            #filepath += "_raw_qa_100K.bcp"
            filepath += "_raw_qa.bcp.gz"
            with gzip.open(filepath, "r") as f:
                self.split_file(f)
            f.close()

    def split_file(self, f):
        #splitting, get useful domains, extract domains
        filepaths = []
        for i in range(0,24):
            filepaths.append(os.path.join(self.tempdata_dir, os.path.basename(f.name)[:9] + format(i, '02d')))
        files = []

        try:
            for i in filepaths:
                files.append(open(i, 'w'))

            for line in f:
                linelist = line.split("\t")
                try:
                    linelist[0] = get_tld(linelist[0], fix_protocol=True)
                except:
                    linelist[0] = ""
                hour = get_hour(int(linelist[6]))
                if self.classifier.in_relevant_site(linelist[0]):
                    files[hour].write("\t".join(linelist))
        finally:
            for i in files:
                i.close()

    def construct_instructions(self, n):
        for i in glob.glob(os.path.join(self.tempdata_dir,"*i.txt")):
            os.remove(i)

        for single_date in daterange(self.start_date, self.end_date):
            for i in range(0,24):
                path = os.path.join(self.tempdata_dir, single_date.strftime("%Y%m%d") + "_" + format(i, '02d'))
                with open(path, "r") as f:
                    self.construct_active_map_instruction(f, n)
                f.close()

    def construct_active_map_instruction(self, f, n):
        end_time_file_path = os.path.join(self.tempdata_dir, os.path.basename(f.name)[:11] + "i.txt")
        start_time_file_path = os.path.join(self.tempdata_dir, get_start_date(os.path.basename(f.name)[:11], n) +"i.txt")
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
    return (datetime.strptime(endtime, '%Y%m%d_%H') - timedelta(days = n)).strftime('%Y%m%d_%H')


def get_hour(ss2k):
    return (ss2k%86400)%24


def get_ss2k(date_in_string):
    return (datetime.strptime(date_in_string, '%Y%m%d') - datetime.strptime("19991231", '%Y%m%d')).seconds


