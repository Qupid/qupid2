from multiprocessing.pool import ThreadPool as Pool
import pandas as pd
# headers all

#pool_size = 5  # your "parallelness"
from multiprocessing import Process
from goose3 import Goose
from textblob import TextBlob
from textatistic import Textatistic
#import urllib
#from urllib.request import urlopen
import urllib.request
import re
import pandas as pd
import requests
from urllib.parse import urlsplit
import time
import os
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

from gensim import corpora, models
import gensim


#from datetime import datetime

def conv(s):
    try:
       return int(s)
    except ValueError:
       return s

df=pd.read_csv('enk.csv')
query = df["url"].values
print(query)
#query =["https://en.wikipedia.org/wiki/Vaccine" , "https://en.wikipedia.org/wiki/Vaccine"]
for i in range(len(query)):
    try:
        g = Goose ( )
        article = g.extract ( url=query[i] )
        text = article.cleaned_text
        blob = TextBlob ( text )
        s = Textatistic ( text )
        vals = requests.get ( query[i] , timeout=4 , allow_redirects=False ).elapsed.total_seconds ( )
        st = "/&callback=process&key=57bf606e01a24537ac906a86dc27891f94a0f587"
        # zz = urlopen ( url )
        quez = 'http://api.mywot.com/0.4/public_link_json2?hosts=' + query[i] + st
        stt = urllib.request.urlopen ( quez ).read ( )
        stt = str ( stt )
        wot = re.findall ( '\d+' , stt )
        ##z=[[conv(s) for s in line.split()] for line in wot]
        z = [ conv ( s ) for s in wot ]
        high = (z[ 1 ])
        low = (z[ 2 ])
        zz = "{0.scheme}://{0.netloc}/".format ( urlsplit ( query[i] ) )
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
            'url': [ query[i] ]}
        df = pd.DataFrame.from_dict ( cols )
        if not os.path.isfile('ft3.csv'):
             df.to_csv('ft3.csv', index=False)
        else: # else it exists so append without writing the header
             df.to_csv('ft3.csv',mode = 'a',header=False, index=False)
    except:
        pass

#na bestanden
#b = pd.read_csv("ft.csv")#labels
#a = pd.read_csv("twit.csv")#features moet headers hebben
#merged = a.merge(b, on='url', how='inner')
#del merged['urlz']
#merged.to_csv("final_output.csv", index=False)
