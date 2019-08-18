import json
import urllib
from urllib.parse import urlparse
import pandas as pd
import httplib2 as http #External library
from pandas.io.json import json_normalize
import time
import datetime
import sys

def eta_time(x):
    x = str(x)
    x = x.replace(" ", "")
    x = x.split("0", maxsplit=1)[1]
    x = x.split("+", maxsplit=1)[0]
    x = datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%S')
    x = str(x).split(" ", maxsplit=1)[1]
    return x

def sec_to_hours(seconds):
    a=str(seconds//3600)
    b=str(round((seconds%3600)//60))
    c=str(round((seconds%3600)%60))
    d="{} mins {} seconds".format(b, c)
    return d

def ttnb (x):
    x = str(x)
    x = x.replace(" ", "")
    x = x.split("0", maxsplit=1)[1]
    x = x.split("+", maxsplit=1)[0]
    x = datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%S')
    if (x - datetime.datetime.now()).total_seconds() > 0:
        x = (x - datetime.datetime.now()).total_seconds()
        x = sec_to_hours(x)
        return x
    else:
        x = str(data['NextBus2.EstimatedArrival'])
        x = x.replace(" ", "")
        x = x.split("0", maxsplit=1)[1]
        x = x.split("+", maxsplit=1)[0]
        x = datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%S')
        x = (x - datetime.datetime.now()).total_seconds()
        x = sec_to_hours(x)
        return x

while True:
    try:
         timenow = datetime.datetime.now()
         timenow = str(timenow).split(".", maxsplit=1)[0]      
         print('-------------------')  
         print('Current Time now: {}'.format(timenow))
         if __name__=="__main__":
         #Authentication parameters
            headers = { 'AccountKey' : 'INPUT API KEY HERE',#Input your API
            'accept' : 'application/json'} 
            
            
            busstop = '44099' #Define the bus-stop, quickest way is to use google maps to find out the 'stopID'
            busid = '172' #Define the bus number that you want to track 
            
            uri = 'http://datamall2.mytransport.sg/'
            path = '/ltaodataservice/BusArrivalv2?'
            target = urlparse(uri + path +'BusStopCode='+busstop)
            method = 'GET'
            body = ''
            h = http.Http()
            response, content = h.request(target.geturl(),method,body,headers)

            jsonObj = json.loads(content)
            data= jsonObj['Services']
            data = pd.DataFrame(json_normalize(data))
            data = data[data['ServiceNo']==busid]
            print('-------------------')
            print('Time to next {} @ {}: {} \nArriving at {}'.format(busid,busstop,
                                                    ttnb(data['NextBus.EstimatedArrival']),
                                                    eta_time(data['NextBus.EstimatedArrival'])))
         time.sleep(30) # waits for 30 seconds before loopings
    except KeyboardInterrupt:
        sys.exit()
