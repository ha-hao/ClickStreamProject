import os, sys
from classifier import classifier
from activeMap import activeMap
from preProcessor import preProcessor
from datetime import datetime, timedelta
import time

def showTime(lastEnd):
    newTime = time.time()
    print(newTime - lastEnd)
    return newTime


start_time = "20120101"
end_time = "201201031"
start_time = datetime.strptime(start_time, '%Y%m%d')
end_time = datetime.strptime(end_time, '%Y%m%d')


timing = time.time()

print("setup")
c = classifier(os.path.join(os.getcwd(), "Lexicons"))
wd = os.getcwd() #change this to the data's dir
p = preProcessor(c,start_time ,end_time , wd, True)
timing = showTime(timing)


print("get relevant sites")
p.get_relevant_active_lines()
timing = showTime(timing)

print("construct checkout instruction")
p.update_checkout()
timing = showTime(timing)

print("get behaviors of id with future checkout")
p.get_relevant_active_lines()
timing = showTime(timing)
