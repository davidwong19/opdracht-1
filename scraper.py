#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import time
import pymongo as mongo


# In[2]:


client = mongo.MongoClient("mongodb://127.0.0.1:27017")
## Make new DB
crypto_db = client["crypto"]

 ## Make new collections
col_crypto = crypto_db["hash"]






# In[3]:


hash =[]
timez =[]
btc = []
usd = []
high =[]
hash_store =[]
time_store =[]
high_store = []
usd_store = []
highNOsort =[]


# In[4]:


import time
a = 1 
try:
    while  a < 6:
            #put in time till next scrape time. sleep(3 = 3s)
            time.sleep(60)
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
            for f in highNOsort:
                if f == s:

                  #old storing method
                  
                  if s not in high_store:
                    #hash_store.append(hash[z]) 
                    #time_store.append(timez[z])
                    #high_store.append(highNOsort[z]) 
                    #usd_store.append(usd[z])
                    #crypto_df = pd.DataFrame({'hash':hash_store,'time':time_store,'btc':high_store,'usd':usd_store})
                    #crypto_df.to_csv('crypto.csv',index=False)
                    #break
                    high_store.append(s)
                    # data
                    mycrypto = {"hash": hash[z], "time": timez[z], "btc": highNOsort[z], "usd": usd[z]}
                    #insert
                    x = col_crypto.insert_one(mycrypto)
                    print('add new value to mongodb')
                    break
                z = z+1
              
except:
    print('scraper has been stopped')
            

