#!/usr/bin/env python

import siteMapping

import Queue, os, sys, time
import threading
from threading import Thread
import urllib2

import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

import stomp

from pprint import pprint

#global messages
#messages=[]

allhosts=[]
allhosts.append([('128.142.36.204',61513)])
allhosts.append([('188.185.227.50',61513)])
topic = '/topic/perfsonar.histogram-owdelay'

siteMapping.reload()

#MAKE on_message add the message to a queue and make queue 10 deep
#MAKE a separate thread that uploads ???


class MyListener(object):
    def on_error(self, headers, message):
        print 'received an error %s' % message
    def on_message(self, headers, message):
        q.put(message)

def eventCreator():
    aLotOfData=[]
    while(True):
        d=q.get()
        m=json.loads(d)
        
        d = datetime.now()
        ind="network_weather_dev-"+str(d.year)+"."+str(d.month)+"."+str(d.day)
        data = {
            '_index': ind,
            '_type': 'latency'
        }
        
        source=m['meta']['source']
        destination=m['meta']['destination']
        data['MA']=m['meta']['measurement_agent']
        data['src']=source
        data['dest']=destination
        so=siteMapping.getPS(source)
        de=siteMapping.getPS(destination)
        if so!= None:
            data['srcSite']=so[0]
            data['srcVO']=so[1]
        if de!= None:
            data['destSite']=de[0]
            data['destVO']=de[1]
        su=m['summaries']
        for s in su:
            if s['summary_window']=='300' and s['summary_type']=='statistics':
                results=s['summary_data']
                # print results
                for r in results:
                    data['timestamp']=r[0]*1000
                    data['delay_mean']=r[1]['mean']
                    data['delay_median']=r[1]['median']
                    data['delay_sd']=r[1]['standard-deviation']
                    #print data
                    aLotOfData.append(data)
        q.task_done()
        if len(aLotOfData)>100:
            res = helpers.bulk(es, aLotOfData)
            print res
            aLotOfData=[]

passfile = open('/afs/cern.ch/user/i/ivukotic/ATLAS-Hadoop/.passfile')
passwd=passfile.read()



print "make sure we are connected right..."
import requests
res = requests.get('http://cl-analytics.mwt2.org:9200')
print(res.content)

es = Elasticsearch([{'host':'cl-analytics.mwt2.org', 'port':9200}])


q=Queue.Queue()
#start eventCreator threads
for i in range(3):
     t = Thread(target=eventCreator)
     t.daemon = True
     t.start()

for host in allhosts:
    conn = stomp.Connection(host, user='psatlflume', passcode=passwd.strip() )
    conn.set_listener('MyConsumer', MyListener())
    conn.start()
    conn.connect()
    conn.subscribe(destination = topic, ack = 'auto', id="1", headers = {})

while(True):
    print "qsize:", q.qsize()
    time.sleep(60)