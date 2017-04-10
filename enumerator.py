import numpy as np
import pandas as pd
import os, sys
from classifier import classifier
from datetime import datetime, timedelta


class enumerator:
    def __init__(self):
        self.classifier = classifier()

    def __init__(self, classifier, start_time, end_time):
        self.classifier = classifier

        date = []
        for single_date in daterange(start_time, end_time):
            date.append(datetime.strftime(single_date,"%Y%m%d"))
        self.df = pd.DataFrame(np.zeros(shape=()), index = date, columns={"Page Visited", "Total Checkout", "Social Media"})

    # def update_df(self, linelist):
    #     if self.classifier.checkout_match(linelist[0],linelist[2]): df[0,1] += 1
    #

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
