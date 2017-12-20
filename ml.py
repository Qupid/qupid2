#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 07:38:43 2017
https://stackoverflow.com/questions/26243993/operations-on-every-row-in-pandas-dataframe
https://stackoverflow.com/questions/43619896/python-pandas-iterate-over-rows-and-access-column-names
@author: ozzy
"""

import pandas as pd
from joblib import Parallel, delayed
import multiprocessing
import pandas as pd
from multiprocessing import Process
from goose3 import Goose
from textblob import TextBlob
from textatistic import Textatistic
import urllib.request
import re
import os
import time
import glob
import pandas as pd
import requests
from urllib.parse import urlsplit
from twitterscraper import query_tweets
from gensim.summarization import keywords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import pickle
import numpy
from gensim import corpora, models
import gensim
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
import os.path
import time
import json
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_file, request, render_template
import os
import unicodedata
import pandas as pd
import time
from flask import send_file
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib
from MagicGoogle import MagicGoogle
from itertools import islice

def conv(s):
    try:
       return int(s)
    except ValueError:
       return s

def most_common(lst):
    return max(set(lst), key=lst.count)

def tmpFunc(df):
    #vals=requests.get ( df.url , timeout=4 , allow_redirects=False ).elapsed.total_seconds ( )
    #vals=requests.get ( df.url , allow_redirects=False ).elapsed.total_seconds ( )
    for row in df.itertuples():
        try:
            g = Goose ( )
            article = g.extract ( url=row.url )
            text = article.cleaned_text
            blob = TextBlob ( text )
            s = Textatistic ( text )
            vals = requests.get ( row.url , timeout=4 , allow_redirects=False ).elapsed.total_seconds ( )
            st = "/&callback=process&key=57bf606e01a24537ac906a86dc27891f94a0f587"
            # zz = urlopen ( url )
            quez = 'http://api.mywot.com/0.4/public_link_json2?hosts=' + row.url + st
            stt = urllib.request.urlopen ( quez ).read ( )
            stt = str ( stt )
            wot = re.findall ( '\d+' , stt )
            ##z=[[conv(s) for s in line.split()] for line in wot]
            z = [ conv ( s ) for s in wot ]
            high = (z[ 1 ])
            low = (z[ 2 ])
            #print ( high , low )
            # WAYBACK
            zz = "{0.scheme}://{0.netloc}/".format ( urlsplit ( row.url ) )
            zurlz = "https://web.archive.org/web/0/" + str ( zz )
            r = requests.get ( zurlz , allow_redirects=False )
            data = r.content
            years = re.findall ( '\d+' , str ( data ) )
            years = [ conv ( s ) for s in years ]
            years = (years[ 0 ])
            years = int ( str ( years )[ :4 ] )
            cols = {'yeararchive': [ years ] ,
            		'lowwot': [ low ] ,
            		'highwot': [ high ] ,
            		'reponsetime': [ vals ] ,
            		'wordcount': [ s.word_count ] ,
            		'subjectivity': [ blob.sentiment.subjectivity ],
            		'polarity': [ blob.sentiment.polarity ] ,
            		'fleschscore': [ s.flesch_score ],
            		#'kw': [ kw ] ,
            		'url': [ row.url ]}
            #vals=requests.get ( row.url , timeout=4 , allow_redirects=False ).elapsed.total_seconds ( )
            #cols = {'vals': [ vals ] , 'url': [ row.url ]}
            df = pd.DataFrame.from_dict ( cols ) 
            return df
        except:
            pass
        
        
        
    		#~ 'lowwot': [ low ] ,
    		#~ 'highwot': [ high ] ,
    		#~ 'reponsetime': [ vals ] ,
    		#~ 'wordcount': [ s.word_count ] ,
    		#~ 'subjectivity': [ blob.sentiment.subjectivity ],
    		#~ 'polarity': [ blob.sentiment.polarity ] ,
    		#~ 'fleschscore': [ s.flesch_score ],
    		#~ #'kw': [ kw ] ,
    		   #'url': [ url ]}
        #df = pd.DataFrame({'vals': vals})
        return df
    #df = pd.DataFrame({'vals': vals})

def applyParallel(dfGrouped, func):
    retLst = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(func)(group) for name, group in dfGrouped)
    return pd.concat(retLst)

if __name__ == '__main__':
    mg = MagicGoogle()
    lijst=[]
    tt='Donald Trump'
    search=str(tt)
    for url in mg.search_url(query=search):
        lijst.append(url)
        
    #iterator = islice(lijst, 2)
    df = pd.DataFrame({'url': lijst})
	#print (df)
	#print (df.index)
    #print (df)
    print ('parallel versionOzzy: ')
    dff=((applyParallel(df.groupby(df.index), tmpFunc)))
    dfeat=dff
    del dfeat['url']
    newX = dfeat.values
    pickle_fname = 'pickle.model'
    pickle_model = pickle.load(open(pickle_fname, 'rb'))
    result = pickle_model.predict(newX)  # print (result)
    px2 = result.reshape((-1, 8))
    dfres = pd.DataFrame(
        {'OverallQuality': px2[:, 0], 'accuracy': px2[:, 1], 'completeness': px2[:, 2], 'neutrality': px2[:, 3],
         'relevance': px2[:, 4], 'trustworthiness': px2[:, 5], 'readability': px2[:, 6], 'precision': px2[:, 7]})
    dfres.to_csv('rr.csv')
    dff.to_csv('rr.csv')

#    print ('regular version: ')
#    print (df.groupby(df.index).apply(tmpFunc))

#    print ('ideal version (does not work): ')
#    print (df.groupby(df.index).applyParallel(tmpFunc))
    
#from multiprocessing import Pool, cpu_count
#
#def applyParallel(dfGrouped, func):
#    with Pool(cpu_count()) as p:
#        ret_list = p.map(func, [group for name, group in dfGrouped])
#    return pandas.concat(ret_list)

