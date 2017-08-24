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




def main():
    start_time = "20130104"
    end_time = "20130105"
    start_time = datetime.strptime(start_time, '%Y%m%d')
    end_time = datetime.strptime(end_time, '%Y%m%d')

    start_period_rng = [3, 6, 9]
    end_period_rng = [0, 3, 6]
    for i in range(3):
        start_period = start_period_rng[i]
        end_period = end_period_rng[i]
        timing = time.time()
        print("setup")
        c = classifier(os.path.join(os.getcwd(), "Lexicons"))
        wd = os.path.join(os.path.dirname(os.getcwd()),"ClickStreamData")
        print(wd)
        p = preProcessor(c,start_time ,end_time, start_period, end_period, wd)

        timing = showTime(timing)
        if i == 0:
            print("Get Relevant Data")
            p.get_relevant_data_all_files(False)
            timing = showTime(timing)

            print("Extract and Summarize Checkout Data")
            p.update_checkout()
            timing = showTime(timing)

            print("Summarize Checkout Data")
            p.summarize_checkout()
            timing = showTime(timing)


        print("Construct Checkout Instructions")
        p.create_instructions()
        timing = showTime(timing)

        print("Ger Relevant Data of Active ID")
        p.get_relevant_active_lines()
        timing = showTime(timing)

        print("Calc")
        p.calculate_n()
        timing = showTime(timing)


def ss2k_to_int_time(ss2k):
    return int(datetime.strftime(datetime(1999, 12, 31, 00, 00) + timedelta(seconds=int(ss2k)),"%Y%m%d%H%M%S"))

def daterange(start_date, end_date):
    d = int(math.ceil((end_date - start_date).days + (end_date - start_date).seconds/86400.0))
    for n in range(d+1):
        yield start_date + timedelta(n)

def showTime(lastEnd):
    newTime = time.time()
    print "Total "+ str(int(newTime - lastEnd)) + " seconds" + "\n"
    return newTime

if __name__ == '__main__':
    main()
# histograms, other product pages