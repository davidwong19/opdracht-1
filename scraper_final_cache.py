#!/usr/bin/env python
# coding: utf-8

# In[5]:


from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import time
import pymongo as mongo
import timedelta
import redis


# In[6]:


client = mongo.MongoClient("mongodb://127.0.0.1:27017")
## Make new DB
crypto_db = client["crypto"]

 ## Make new collections
col_crypto = crypto_db["hash"]


# In[7]:


hash =[]
timez =[]
btc = []
usd = []
high =[]
hash_store =[]
time_store =[]
high_store = []
high_store_history = []
usd_store = []
highNOsort =[]
redis_client = redis.Redis ()


# In[8]:


import time
start_time = time.time()
# seconds = 60 time before the data from redis is send to mongodb
seconds = 60
try:
    while True:
            #put in time till next scrape time. sleep(3 = 3s)
            hash.clear()
            timez.clear()
            btc.clear()
            usd.clear()
            high.clear()
            highNOsort.clear()
            r3 = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
            soup = BeautifulSoup(r3.text,features ="html.parser")
            #hash
            oke = soup.find_all('a',{ "class" : "sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK"})
            for ok in oke:
                s = ok.text.strip()
                hash.append(s)
            #time
            oke = soup.find_all('span',{ "class" : "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC"})
            k= 3
            for ok in oke:
                s = ok.text.strip()
                if k%3 == 0:
                    s1 = s.split(':')
                    s2 = int(s1[0])+1
                    s3 = str(s2) +':'+s1[1]
                    timez.append(s3)
                k = k + 1
            #btc
            oke = soup.find_all('span',{ "class" : "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC"})
            k= 2
            for ok in oke:
                s = ok.text.strip()
                if k%3 == 0:
                    btc.append(s)
                k = k + 1
            #this is btc only in numbers without BTC
            high =[]
            highNOsort =[]
            for ok in btc:
                ok2 = ok.replace('BTC', '')
                ok3 = ok2.replace(' ','')
                high.append(float(ok3))
                highNOsort.append(float(ok3))
            #usd
            oke = soup.find_all('span',{ "class" : "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC"})
            k= 1
            for ok in oke:
                s = ok.text.strip()
                if k%3 == 0:
                    usd.append(s)
                k = k + 1
            #check btc
            high.sort(reverse=True)
            for ok in high:
                s = ok
                break        
            z = 0 
            #store highest btc transaction 
            #btc list with no sort(hishnosort)
            # f and s are btc here
            #hish_store check if we dont have them already
            for f in highNOsort:
                if f == s:                
                  if s not in high_store:
                        high_store.append(s)
                        high_store.sort(reverse=True)
                        # check if previos hash transaction was higher than store in redis
                        if s >= high_store[0]:
                                redis_client.set('hash',hash[z])
                                redis_client.set('time',timez[z])
                                redis_client.set('btc',highNOsort[z])
                                redis_client.set('crypto',usd[z])
                                
                
                        break
                z = z+1
            #if 1 min passes store redis key in mongodb
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > seconds:
                high_store.clear() 
                start_time = time.time()
                hash1 =  redis_client.get('hash')
                time1 =  redis_client.get('time')
                highNOsort1 = redis_client.get('btc')
                usd1 = redis_client.get('crypto')
                mycrypto = {"hash": hash1.decode("utf-8"), "time": time1.decode("utf-8"), "btc": highNOsort1.decode("utf-8"), "usd": usd1.decode("utf-8")}
                #insert
                x = col_crypto.insert_one(mycrypto)
                redis_client.delete('crypto')
                redis_client.delete('hash')
                redis_client.delete('time')
                redis_client.delete('btc')
                redis_client.delete('crypto')
except:
    print('scraper has been stopped')  
            
      

