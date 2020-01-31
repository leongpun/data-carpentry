import pandas as pd
import glob
import re
import datetime

def Trans_date(date):
    """
    2013年03月19日07时 转为 2013-03-19 07:00:00
    """
    assert isinstance(date,str),"input date must be a string!"

    pat_year = re.compile('：.+?年')
    year = pat_year.findall(date)[0][1:-1]
    pat_month = re.compile('年.+?月')
    month = pat_month.findall(date)[0][1:-1]
    pat_day = re.compile('月.+?日')
    day = pat_day.findall(date)[0][1:-1]
    pat_hour = re.compile('日.+?时')
    hour = pat_hour.findall(date)[0][1:-1]
    return(pd.to_datetime(year+'-'+month+'-'+day+' '+hour+':00:00'))

colsnames = ["height", "elapstime", 'temperature', 'pressure', 'humidity',
             'dewpoint', 'diffdew', 'virtemp', 'wd', 'ws', 'difflat', 'difflon']
profiledata=pd.DataFrame()
for filename in glob.glob('./data/resolution50m/*.txt'):
    
    date = pd.read_table(filename, sep='\t',
                         encoding='gb2312', skiprows=11, nrows=1, header=None)
    result = pd.read_table(filename, sep='\s+',
                           encoding='gb2312', skiprows=16, nrows=61, header=None, names=colsnames)
    date=Trans_date(str(date))
    result['date']=date
    profiledata=pd.concat([result,profiledata],axis=0)

profiledata.to_csv(".\data\profiledata.csv")