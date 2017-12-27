from newspaper import Article
from textblob import TextBlob
from textatistic import Textatistic
import urllib.request
import re
import pandas as pd
import requests
from urllib.parse import urlsplit
import time
import os

def conv(s):
    try:
       return int(s)
    except ValueError:
       return s

df=pd.read_csv('enk.csv')
query = df["url"].values
#query =["https://en.wikipedia.org/wiki/Vaccine" , "https://en.wikipedia.org/wiki/Vaccine"]
for i in range(len(query)):
    try:
        article = Article(query[i])
        article.download()
        article.parse()
        text = article.text
        blob = TextBlob ( text )
        s = Textatistic ( text )
        afb = len(article.images)
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
            'pictures': [afb],
            #'kw': [ kw ] ,
            'url': [ query[i] ]}
        df = pd.DataFrame.from_dict ( cols )
        #df.to_csv('ozzy.csv', index=False)

        if not os.path.isfile('ft.csv'):
            df.to_csv('ft.csv', index=False)
        else:  # else it exists so append without writing the header
            df.to_csv('ft.csv', mode='a', header=False, index=False)

        time.sleep(2)
    except:
        pass

#na bestanden
b = pd.read_csv("ft.csv")#labels
a = pd.read_csv("lab.csv")#features moet headers hebben
merged = a.merge(b, on='url', how='inner')
#del merged['urlz']
merged.to_csv("mjoined.csv", index=False)
