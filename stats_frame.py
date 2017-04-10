import pandas as pd
from dateutil.relativedelta import relativedelta
import datetime

result = []

start_date = datetime.strptime(start_month, '%Y%m%d')
end_date = datetime.strptime(end_month, '%Y%m%d')

while current <= today:
    result.append(current)
    current += relativedelta(months=1)

def construct_frame:
    a = pd.DataFrame(0,index = ["1","2"],columns=["2,3"])
    print(a)