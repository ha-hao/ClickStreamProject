import os, sys
from classifier import classifier
from activeMap import activeMap
from preProcessor import preProcessor
from datetime import datetime, timedelta
import time

import sys
#sys.path.append('/Users/haotianli/anaconda/lib/python2.7/site-packages')



start = time.time()

wd = os.getcwd()
c = classifier(os.path.join(wd, "Lexicons"))

end = time.time()
print(end - start)
start = end

p = preProcessor(c, "20130101", "20130102", wd)

end = time.time()
print(end - start)
start = end

p.split_files_by_hours()

end = time.time()
print(end - start)
start = end

p.construct_instructions(3)

end = time.time()
print(end - start)
start = end