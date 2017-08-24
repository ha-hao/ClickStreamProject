import os, sys
from classifier import classifier
from activeIDMap import activeIDMap
from preProcessor import preProcessor
from demographicsMap import demographicsMap
from enumerator import enumerator
from datetime import datetime, timedelta
from dateutil import relativedelta
import numpy as np
import time
import math

def calculate_n():

    total_output = np.zeros((confident_end_month - confident_start_month + 1, 8), dtype=np.int)
    naive_output = np.zeros((confident_end_month - confident_start_month + 1, 6), dtype=np.int)

        for current_date in daterange(confident_start_time, confident_end_time):
            row = current_date.year * 12 + current_date.month - confident_start_month

            print("Calculate " + current_date.strftime("%Y%m%d"))
            id_file = os.path.join(wd, "temp_data/" + current_date.strftime("%Y%m%d") + "i")
            id_map = activeIDMap(id_file, c)

            data_file = wd + "/temp_data/" + current_date.strftime('%Y%m%d') + "ra"
            with open(data_file, "r") as f:
                for line in f:
                    linelist = line.split("\t")
                    id_n = id_map.get_id_n(linelist[4], linelist[3])
                    id_domain_n = id_map.get_id_category_n(linelist[4], linelist[0], linelist[3])
                    id_category_n = id_map.get_id_category_n(linelist[4], linelist[0], linelist[3], c)

                    category = c.get_category_vector(linelist[0], linelist[2])
                    total_output[row] += [category[1], category[0] * id_domain_n, category[2] * id_domain_n,
                                          category[0] * (id_n - id_domain_n), category[2] * (id_n - id_domain_n),
                                          category[3] * id_n, category[4] * id_n, category[5] * id_n]
                    naive_output[row] += category

            f.close()

def daterange(start_date, end_date):
    d = int(math.ceil((end_date - start_date).days + (end_date - start_date).seconds/86400.0))
    for n in range(d+1):
        yield start_date + timedelta(n)