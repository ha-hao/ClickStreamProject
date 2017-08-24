import os
from classifier import classifier
from demographicsMap import demographicsMap
from datetime import datetime, timedelta
from tld import get_tld
import glob
import gzip
import subprocess
import time
import math
from activeIDMap import activeIDMap
import numpy as np
import csv


def showTime(lastEnd):
    newTime = time.time()
    print(newTime - lastEnd)
    return newTime

class preProcessor:
    def __init__(self):
        self.classifier = classifier()
        self.start_time = ""
        self.end_time = ""
        self.start_period = ""
        self.end_period = ""
        self.data_dir = ""
        self.tempdata_dir = ""
        self.result_dir = ""

    def __init__(self, classifier, start_date, end_date, n_start, n_end, data_dir):
        self.classifier = classifier
        self.start_time = start_date
        self.end_time = end_date
        self.start_period = n_start
        self.end_period = n_end
        self.data_dir = data_dir
        self.tempdata_dir = data_dir + "/temp_data"
        self.result_dir = data_dir + "/result"
        if not os.path.exists(self.tempdata_dir):
            os.makedirs(self.tempdata_dir)
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def get_relevant_data_all_files(self, overwrite):
        for current_date in daterange(self.start_time, self.end_time):
            newTime = time.time()
            print "Get Relevant Data of " + current_date.strftime("%Y%m%d") + ": ",
            filepath = os.path.join(os.path.join(self.data_dir,  current_date.strftime("%Y%m")),current_date.strftime("%Y%m%d"))
            filepath += "_raw_qa.bcp.gz"
            output_path = get_relevant_file_path(self.tempdata_dir, current_date)
            if (not os.path.exists(output_path)) or overwrite:
                self.get_relevant_data(filepath, output_path)
            printTime(newTime)

    def get_relevant_data(self, filepath, output_path):
        with gzip.open(filepath, "r") as f:
            with open(output_path, "w") as o:
                lastcheckout = ""
                lastid = ""
                for line in f:
                    linelist = line.split("\t")
                    try:
                        linelist[0] = get_tld(linelist[0], fix_protocol=True)
                    except:
                        linelist[0] = ""
                    linelist[0] = linelist[0].lower()
                    if self.classifier.in_relevant_site(linelist[0]):
                        linelist[1] = linelist[1].lower()
                        linelist[2] = linelist[2].lower()
                        output = "\t".join(linelist)
                        if self.classifier.checkout_match(linelist[0],linelist[1], linelist[2]):
                            if not lastid == linelist[6]:
                                o.write(lastcheckout)
                                lastid = linelist[6]
                            lastcheckout = output
                        else:
                            o.write(output)
                o.write(lastcheckout)
            o.close()
        f.close()


    def update_checkout(self):
        for i in glob.glob(get_checkout_path(self.tempdata_dir, "*")):
            os.remove(i)

        for current_date in daterange(self.start_time, self.end_time): # for each date
            newTime = time.time()
            print "Extract Checkout Data: " + current_date.strftime("%Y%m%d") + ": ",
            # put (id, host, date) of checkout into a list
            with open(get_relevant_file_path(self.tempdata_dir, current_date), "r") as f:
                with open(get_checkout_path(self.tempdata_dir, current_date), "w") as o:
                    for line in f:
                        linelist = line.split("\t")
                        if self.classifier.checkout_match(linelist[0],linelist[1], linelist[2]):
                            o.write(linelist[6] +"\t" + linelist[0] + "\t" + ss2k_to_date(linelist[4]).strftime("%Y%m%d%H%M%S") + "\t" + "\n")
            f.close()
            o.close()
            printTime(newTime)

    def create_instructions(self):

        for i in glob.glob(get_instruction_path(self.tempdata_dir, "*", self.start_period, self.end_period)):
            os.remove(i)

        for current_date in daterange(self.start_time, self.end_time): # for each date
            newTime = time.time()
            print "Construct Checkout Instructions: " + current_date.strftime("%Y%m%d") + ": ",
            checkout_list = []
            with open(get_checkout_path(self.tempdata_dir, current_date), "r") as f:
                for line in f:
                    linelist = line.split("\t")
                    linelist[2] = datetime.strptime(linelist[2], "%Y%m%d%H%M%S")
                    checkout_list.append(linelist)
            f.close()

            datelist = [i for i in daterange(current_date - timedelta(hours= self.start_period), current_date - timedelta(hours= self.end_period))]
            n_days = int(math.ceil((self.start_period - self.end_period) / 24.0))
            # extract checkout data into files (start/end date of checkout for each site)
            for n in range(n_days + 1):
                output_string = ""
                for i in checkout_list:
                    default_start = datelist[n].replace(hour=0,minute=0,second=0)
                    default_end = datelist[n].replace(hour=23,minute=59,second=59)
                    if n == 0:
                        default_start = i[2] - timedelta(hours = self.start_period)
                    if n == n_days:
                        default_end = i[2] - timedelta(hours = self.end_period)

                    output_string += "\t".join([i[0], i[1], default_start.strftime("%Y%m%d%H%M%S"),
                                            default_end.strftime("%Y%m%d%H%M%S"), current_date.strftime("Y%m"), "\n"])

                # write output into a file
                with open(get_instruction_path(self.tempdata_dir, datelist[n], self.start_period, self.end_period ), "a") as o:
                    o.write(output_string)
                o.close()
            printTime(newTime)



    def summarize_checkout(self):
        # generate empty file with header
        for i in glob.glob(get_cs_path(self.result_dir, "*" )):
            os.remove(i)

        for current_date in daterange(self.start_time, self.end_time): # for each date
            newTime = time.time()
            print "Summarize Checkout: " + current_date.strftime("%Y%m%d") + ": ",
            checkout_list = []
            with open(get_checkout_path(self.tempdata_dir, current_date), "r") as f:
                for line in f:
                    linelist = line.split("\t")
                    linelist[2] = datetime.strptime(linelist[2], "%Y%m%d%H%M%S")
                    checkout_list.append(linelist)
            f.close()

            cs_name = get_cs_path(self.result_dir, current_date)
            if not os.path.exists(cs_name):
                with open(cs_name, "a") as f:
                    headers = ["Month", "ID", "Host", "Category", "Age", "Gender", "Household_Income", "Household_Size","Houesehold_Education","Children", "Race", "Ethnicity\n"]
                    f.write("\t".join(headers))
                f.close()

            # generate demo_map
            demographics_month = (current_date.year - 2013) *12 + (current_date.month - 1) + 157
            demographics_file = os.path.join(os.getcwd(), "Demographic/demographics_" + str(demographics_month) + "m.txt")
            demo_map = demographicsMap()
            demo_map.update_demographics_map_from_file(demographics_file)

            # write summarized info into files
            output = ""
            for i in checkout_list:
                #output += "\t".join([i[2].strftime("%Y%m%d%H%M%S"), i[0], i[1], self.classifier.get_category(i[1])] + demo_map.get_demographics(i[0]) + ["\n"])
                output += "\t".join([current_date.strftime("%Y%m"), i[0], i[1], self.classifier.get_category(i[1])] + demo_map.get_demographics(i[0]) + ["\n"])
            with open(cs_name, "a") as o:
                o.write(output)
            o.close()

            printTime(newTime)

    def get_relevant_active_lines(self):
        for i in glob.glob(get_relevant_active_file_path(self.tempdata_dir, "*", self.start_period, self.end_period)):
             os.remove(i)

        for current_date in daterange(self.start_time, self.end_time - timedelta(hours = self.start_period)):
            newTime = time.time()
            print "Get Relevant Data of Active ID: " + current_date.strftime("%Y%m%d") + ": ",

            instruction_path = get_instruction_path(self.tempdata_dir, current_date, self.start_period, self.end_period)
            activeID = activeIDMap(instruction_path, self.classifier)

            data_path = get_relevant_file_path(self.tempdata_dir, current_date)
            output_path = get_relevant_active_file_path(self.tempdata_dir, current_date, self.start_period, self.end_period)
            with open(data_path, "r") as f:
                with open(output_path, "w") as o:
                    for line in f:
                        linelist = line.split("\t")
                        if activeID.is_active_id(linelist[6]):
                            o.write("\t".join([linelist[0],linelist[1],linelist[2],linelist[4],linelist[6],"\n"]))
                o.close()
            f.close()
            printTime(newTime)


    def calculate_n(self):
        confident_start_time = self.start_time
        confident_end_time = self.end_time - timedelta(hours = self.start_period)
        confident_start_month = self.start_time.year * 12 + self.start_time.month
        confident_end_month = self.end_time.year * 12 + self.end_time.month

        total_output = np.zeros((confident_end_month - confident_start_month + 1, 8), dtype=np.int)
        #naive_output = np.zeros((confident_end_month - confident_start_month + 1, 6), dtype=np.int)

        for current_date in daterange(confident_start_time, confident_end_time):
            row = current_date.year * 12 + current_date.month - confident_start_month

            print("Calculate " + current_date.strftime("%Y%m%d"))
            id_file = get_instruction_path(self.tempdata_dir, current_date, self.start_period, self.end_period)
            id_map = activeIDMap(id_file, self.classifier)

            data_file = get_relevant_active_file_path(self.tempdata_dir, current_date, self.start_period, self.end_period)
            with open(data_file, "r") as f:
                for line in f:
                    linelist = line.split("\t")
                    current_id_n, next_id_n = id_map.get_id_n(linelist[4], linelist[3])


                    if self.classifier.in_target_site(linelist[0]):
                        current_domain_n, next_domain_n = id_map.get_id_domain_n(linelist[4], linelist[0], linelist[3])
                        current_cat_n, next_cat_n = id_map.get_id_category_n(linelist[4], linelist[0], linelist[3], self.classifier)
                    else:
                        current_domain_n, next_domain_n = 0
                        current_cat_n, next_cat_n = 0
                    current_cat, next_cat = self.classifier.get_category_vector(linelist[0], linelist[1], linelist[2])
                    total_output[row] += create_row_input(current_cat, current_id_n, current_domain_n, current_cat_n)
                    total_output[row + 1] += create_row_input(next_cat, next_id_n, next_domain_n, next_cat_n)
            f.close()

        outputpath = get_csv_path(self.result_dir, self.start_time, self.end_time, self.start_period, self.end_period)
        output_file = open(outputpath, 'wb')
        writer = csv.writer(output_file)
        writer.writerow(["Checkout", "Same Site All", "Same Site Product", "Competitor Site All", "Competitor Site Product",
                         "Coupon", "Review", "Social Media"])
        for i in total_output:
            writer.writerow(i)
        output_file.close()


def get_relevant_file_path(dir, date):
    return dir + "/" + date.strftime("%Y%m%d") + "r"

def get_checkout_path(dir, date):
    if date == "*": return dir + "/" + "*" + "_c"
    else: return dir + "/" + date.strftime("%Y%m%d") + "_c"

def get_instruction_path(dir, date, start, end):
    if date == "*": return dir + "/" + "*" + "_" +str(start) + "_" + str(end)+ "_i"
    else: return dir + "/" + date.strftime("%Y%m%d") + "_" + str(start) + "_" + str(end) + "_i"


def get_relevant_active_file_path(dir, date, start, end):
    if date == "*": return dir + "/" + "*" + "_" + str(start) + "_" + str(end)+ "_ra"
    else: return dir + "/" + date.strftime("%Y%m%d") + "_" + str(start) + "_" + str(end) + "_ra"


def get_cs_path(dir, date):
    if date == "*": return dir + "/" + "*" + "cs"
    return dir + "/" + date.strftime("%Y%m") + "cs"

def get_csv_path(dir, startdate, enddate, start, end):
    return dir + "/" + startdate.strftime("%Y%m%d") + "_" + enddate.strftime("%Y%m%d") + "_" + str(start) +"_" + str(end) + "_result.csv"


def daterange(start_date, end_date):
    d = int(math.ceil((end_date - start_date).days + (end_date - start_date).seconds/86400.0))
    for n in range(d+1):
        yield start_date + timedelta(n)

def get_hour(ss2k):
    return (ss2k%86400)%24


def get_ss2k(date_in_string):
    return (datetime.strptime(date_in_string, '%Y%m%d') - datetime.strptime("19991231", '%Y%m%d')).seconds

def ss2k_to_date(ss2k):
    return datetime(1999, 12, 31, 00, 00) + timedelta(seconds=int(ss2k))

def runCommand(command):
    grep = subprocess.Popen(command, shell= True)
    return grep.communicate()

def printTime(newTime):
    print(str(int(time.time() - newTime)) + " seconds")

def create_row_input(current_cat, current_id_n, current_domain_n, current_cat_n):
    return [current_cat[1], current_cat[0] * current_domain_n, current_cat[2] * current_domain_n,
            current_cat[0] * (current_cat_n - current_domain_n), current_cat[2] * (current_cat_n - current_domain_n),
            current_cat[3] * current_id_n, current_cat[4] * current_id_n, current_cat[5] * current_id_n]


