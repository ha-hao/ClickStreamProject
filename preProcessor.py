import os
from classifier import classifier
from datetime import datetime, timedelta
from tld import get_tld
import glob
import gzip
import subprocess
from activeMap import activeMap
from random import random

class preProcessor:
    def __init__(self):
        self.classifier = classifier()
        self.start_date = ""
        self.end_date = ""
        self.data_dir = ""
        self.tempdata_dir = ""
        self.sampled = ""

    def __init__(self, classifier, start_month, end_month, data_dir, sampled):
        self.classifier = classifier
        self.start_date = datetime.strptime(start_month, '%Y%m%d')
        self.end_date = datetime.strptime(end_month, '%Y%m%d')
        self.data_dir = data_dir
        self.tempdata_dir = data_dir + "/temp_data"
        if not os.path.exists(self.tempdata_dir):
            os.makedirs(self.tempdata_dir)
        self.sampled = sampled

    def get_relevant_lines_all_files(self, overwrite):
        for single_date in daterange(self.start_date, self.end_date):
            filepath = os.path.join(os.path.join(self.data_dir,  single_date.strftime("%Y%m")),single_date.strftime("%Y%m%d"))
            # filepath += "_raw_qa_100K.bcp"
            filepath += "_raw_qa.bcp.gz"
            output_path = os.path.join(self.tempdata_dir,(single_date.strftime("%Y%m%d") + "r"))
            if (not os.path.exists(output_path)) or overwrite:
                with gzip.open(filepath, "r") as f:
                # with open(filepath, "r") as f
                    with open(output_path, "w") as o:
                        for line in f:
                            linelist = line.split("\t")
                            try:
                                linelist[0] = get_tld(linelist[0], fix_protocol=True)
                            except:
                                linelist[0] = ""
                            if self.classifier.in_relevant_site(linelist[0]):
                                o.write("\t".join(linelist))
                        o.close()
                f.close()

    def sample_files(self, n, overwrite):
        for i in glob.glob(os.path.join(self.tempdata_dir,"*r")):
            output_path = i + "s"
            if (not os.path.exists(output_path)) or overwrite:
                with open(i, "r") as f,\
                    open(output_path, "w") as o:
                    for line in f:
                        if random() <= 1.0/n:
                            o.write(line)
                f.close()
                o.close()

    def split_files_by_hours(self):
        if self.sampled:
            fileformat = os.path.join(self.tempdata_dir,"*rs")
        else:
            fileformat = os.path.join(self.tempdata_dir,"*r")
        for i in glob.glob(fileformat):
            with open(i, "r") as f:
                self.split_file(f)
            f.close()

    def split_file(self, f):
        filepaths = []
        for i in range(0,24):
            output_name = os.path.join(self.tempdata_dir, os.path.basename(f.name)[:8] + format(i, '02d'))
            if f.name[-1:] == "s":
                output_name += "s"
            filepaths.append(output_name)
        files = []
        for i in filepaths:
            files.append(open(i, 'w'))

        for line in f:
            linelist = line.split("\t")
            hour = get_hour(int(linelist[6]))
            files[hour].write("\t".join(linelist))
        for i in files:
            i.close()

    def get_start_date(self, endtime, n):
         if (datetime.strptime(endtime, '%Y%m%d%H') - timedelta(days = n)) < self.start_date:
             return self.start_date.strftime('%Y%m%d%H')
         else:
             return (datetime.strptime(endtime, '%Y%m%d%H') - timedelta(days = n)).strftime('%Y%m%d%H')

    def construct_instructions(self, n):
        for i in glob.glob(os.path.join(self.tempdata_dir,"*i.txt")):
            os.remove(i)

        for single_date in daterange(self.start_date, self.end_date):
            for i in range(0,24):
                path = os.path.join(self.tempdata_dir, single_date.strftime("%Y%m%d") + format(i, '02d'))
                print(path)
                if self.sampled:
                    path+="s"
                with open(path, "r") as f:
                    self.construct_active_map_instruction(f, n)
                f.close()

    def construct_active_map_instruction(self, f, n):
        end_time_file_path = os.path.join(self.tempdata_dir, self.get_start_date(os.path.basename(f.name)[:10], -1)  + "i.txt")
        start_time_file_path = os.path.join(self.tempdata_dir, self.get_start_date(os.path.basename(f.name)[:10], n-1) +"i.txt")
        print(start_time_file_path)
        with open(end_time_file_path, write_append(end_time_file_path)) as fe, \
                open(start_time_file_path, write_append(start_time_file_path)) as fs:
            for line in f:
                linelist = line.split()
                if self.classifier.checkout_match(linelist[0],linelist[2]):
                    #print(line)
                    fe.write("-" + linelist[5] + "_" + linelist[0] + "\n")
                    fs.write(linelist[5] + "_" + linelist[0] + "\n")

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

def get_hour(ss2k):
    return (ss2k%86400)%24


def get_ss2k(date_in_string):
    return (datetime.strptime(date_in_string, '%Y%m%d') - datetime.strptime("19991231", '%Y%m%d')).seconds

def runCommand(command):
    grep = subprocess.Popen(command, shell= True)
    grep.communicate()

