import os, sys
from classifier import classifier
from activeMap import activeMap
from preProcessor import preProcessor
from datetime import datetime, timedelta
import time

import sys
#sys.path.append('/Users/haotianli/anaconda/lib/python2.7/site-packages')

def showTime(lastEnd):
    newTime = time.time()
    print(newTime - lastEnd)
    return newTime


start_time = "20120101"
end_time = "20120102"

end = time.time()

wd = os.getcwd()
c = classifier(os.path.join(wd, "Lexicons"))
end = showTime(end)

p = preProcessor(c,start_time ,end_time , wd, True)

print("rel")
p.get_relevant_lines_all_files(False)
end = showTime(end)

print("sample")
p.sample_files(10, False)
end = showTime(end)

print("split")
p.split_files_by_hours()
end = showTime(end)

print("consturct")
p.construct_instructions(3)
end = showTime(end)

start_date = datetime.strptime(start_time, '%Y%m%d')
end_date = datetime.strptime(end_time, '%Y%m%d')

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

count = 0
effective_page = 0
check_out = 0
social_media = 0
am = activeMap()
for single_date in daterange(start_date,end_date):
    for i in range(0,24):
        data_path = wd + "/temp_data/" + single_date.strftime("%Y%m%d") + format(i, '02d') + "s"
        instruction_path = wd + "/temp_data/" + single_date.strftime("%Y%m%d") + format(i, '02d') + "i.txt"
        if os.path.exists(instruction_path):
            with open(instruction_path, "r") as instr:
                am.update_maps_from_file(instr)
            instr.close()
        with open(data_path, "r") as data:
            for line in data:
                count+=1
                linelist = line.split("\t")
                host = linelist[0]
                url = linelist[1]
                id = linelist[5]
                n = am.getIDNum(id)
                if n != 0:
                    effective_page += n
                    if c.checkout_match(host, url):
                        check_out+= n
                    if c.is_socialmedia(host):
                        social_media += n

        data.close()
        instr.close()
        print(single_date.strftime("%Y%m%d") + format(i, '02d'))

        print(count)
        print(effective_page)
        print(check_out)
        print(social_media)


