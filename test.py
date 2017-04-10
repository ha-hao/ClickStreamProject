import os, sys
from classifier import classifier
from activeMap import activeMap
#from preProcessor import preProcessor
from datetime import datetime, timedelta
import time



b = datetime.strptime("20010101","%Y%m%d")
a = datetime.strptime("20010102010101","%Y%m%d%H%M%S")
c = b -a

print( c.days , c.seconds//3600 , (c.seconds//60)%60)