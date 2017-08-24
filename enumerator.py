import numpy as np
import pandas as pd
import os, sys
from classifier import classifier
from datetime import datetime, timedelta
from demographicsMap import demographicsMap
from activeIDMap import activeIDMap
import subprocess


class enumerator:
    def __init__(self):
        self.classifier = classifier()
        self.column_name = ["site", "product_category", "is_checkout", "is_product","target_n", "total_n"]

    def __init__(self, classifier):
        self.classifier = classifier
        self.column_name = ["site", "product_category", "is_checkout", "is_product", "target_n", "total_n"]

        # date = []
        # for single_date in daterange(start_time, end_time):
        #     date.append(datetime.strftime(single_date,"%Y%m%d"))

    def update_df(self, path, demo_map, id_map):
        # print("here")
        grep = subprocess.Popen("wc -l " + path + " | awk '{print $1}'", shell= True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        nrow, err = grep.communicate()
        # print(nrow)
        # result = np.zeros(shape=(int(nrow.split(" ")[0]),len(self.column_name)))
        result = []
        count = 0
        with open(path, "r") as f:
            for line in f:
                linelist = line.split("\t")
                row_list = self.classifier.examine_category(linelist[0],linelist[2]) + list(demo_map.get_demographics(linelist[4])) \
                       + [id_map.get_id_category_n(linelist[4], linelist[0], linelist[3]), id_map.get_id_n(linelist[4], linelist[3])]
                result.append(self.create_dict(row_list))
                # print(row_list)
                count+=1
                if count == 1000:
                    break

        f.close()
        df = pd.DataFrame(result)


        return df

    def create_dict(self, row_list):
        row_dict = {}
        for i in range(len(row_list)):
            row_dict[self.column_name[i]] = row_list[i]
        return row_dict



    # def examine_info(self, line, demo_map, id_map):
    #     linelist = line.split("\t")
    #     return self.classifier.examine_category(linelist[0],linelist[2]) + list(demo_map.get_demographics(linelist[4])) \
    #            + [id_map.get_id_domain_n(linelist[4], linelist[0]), id_map.get_id_n(linelist[0])]

    def summarize_data(self, df, path):
        writer = pd.ExcelWriter(path)
        df.to_excel(writer,'Sheet1')
        writer.save()






def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
