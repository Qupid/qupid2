#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://github.com/mbr/flask-bootstrap.git
form to Database
Vanaf 70 naar multi
"""
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing
from flask import Flask, send_from_directory
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
import urllib
from MagicGoogle import MagicGoogle
from multiprocessing import Pool, cpu_count
from queue import Queue
from threading import Thread
import time
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing
from flask import Flask, send_from_directory
from multiprocessing import Process
import functools

def conv(s):
    try:
       return int(s)
    except ValueError:
       return s

def most_common(lst):
    return max(set(lst), key=lst.count)

app = Flask(__name__)
app.secret_key = 'ThisIsSecret'

def countLetters(word):
    count = 0
    for c in word:
        count += 1
    return count


def f1(q, url):
    try:
    #print("Start: %s" % time.ctime())
    # Instead of returning the result we put it in shared queue.
    #     st = "/&callback=process&key=57bf606e01a24537ac906a86dc27891f94a0f587"
    #     # zz = urlopen ( url )
    #     quez = 'http://api.mywot.com/0.4/public_link_json2?hosts=' + url + st
    #     stt = urllib.request.urlopen(quez).read()
    #     stt = str(stt)
    #     wot = re.findall('\d+', stt)
    #     ##z=[[conv(s) for s in line.split()] for line in wot]
    #     z = [conv(s) for s in wot]
    #     high = (z[1])
    #     low = (z[2])
    #     # print ( high , low )
        # WAYBACK
        zz = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        zurlz = "https://web.archive.org/web/0/" + str(zz)
        r = requests.get(zurlz, allow_redirects=False)
        data = r.content
        years = re.findall('\d+', str(data))
        years = [conv(s) for s in years]
        years = (years[0])
        years = int(str(years)[:4])
        cols = {'yeararchive': [years],
                # 'lowwot': [low],
                # 'highwot': [high],
                #'reponsetime': [vals],
                'url': [str(url)]}
        dfb = pd.DataFrame.from_dict(cols)
        #print(dfb)
        #print("Start: %s" % time.ctime())
        q.put(dfb)
    except:
        cols = {'yeararchive': [str('err')],
                # 'lowwot': [low],
                # 'highwot': [high],
                # 'reponsetime': [vals],
                'url': [str(url)]}
        dfb = pd.DataFrame.from_dict(cols)
        # print(dfb)
        # print("Start: %s" % time.ctime())
        q.put(dfb)
    #     pass

def f2(q, url):
    try:
    #print("Start: %s" % time.ctime())
        #vals = requests.get(url, timeout=4, allow_redirects=False).elapsed.total_seconds()
        g = Goose()
        article = g.extract(url=url)
        text = article.cleaned_text
        blob = TextBlob(text)
        # taal = blob.detect_language()
        # if taal == ('en'):
        #     try:
        s = Textatistic(text)
        cols = {
                        'wordcount': [s.word_count],
                        #'reponsetime': [vals],
                        'subjectivity': [blob.sentiment.subjectivity],
                        'polarity': [blob.sentiment.polarity],
                        'fleschscore': [s.flesch_score],
                        # 'kw': [ kw ] ,
                        'url': [str(url)]}
        dfa = pd.DataFrame.from_dict(cols)
                #print(dfa)
                #print("Start: %s" % time.ctime())
        q.put(dfa)
            # except:
    except:
        #s = Textatistic(text)
        cols = {
                        'wordcount': [str('err')],
    #                    'reponsetime': [str('err')],
                        'subjectivity': [str('err')],
                        'polarity': [str('err')],
                        'fleschscore': [str('err')],
                        # 'kw': [ kw ] ,
                        'url': [str(url)]}
        dfa = pd.DataFrame.from_dict(cols)
                #print(dfa)
                #print("Start: %s" % time.ctime())
        q.put(dfa)
        #pass
            #     pass
    #pass


def f3(q, url):
    try:
    #print("Start: %s" % time.ctime())
    # Instead of returning the result we put it in shared queue.
        st = "/&callback=process&key=57bf606e01a24537ac906a86dc27891f94a0f587"
        # zz = urlopen ( url )
        quez = 'http://api.mywot.com/0.4/public_link_json2?hosts=' + url + st
        stt = urllib.request.urlopen(quez).read()
        stt = str(stt)
        wot = re.findall('\d+', stt)
        ##z=[[conv(s) for s in line.split()] for line in wot]
        z = [conv(s) for s in wot]
        high = (z[1])
        low = (z[2])
        # print ( high , low )
        # WAYBACK
        # zz = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        # zurlz = "https://web.archive.org/web/0/" + str(zz)
        # r = requests.get(zurlz, allow_redirects=False)
        # data = r.content
        # years = re.findall('\d+', str(data))
        # years = [conv(s) for s in years]
        # years = (years[0])
        # years = int(str(years)[:4])
        cols = {#'yeararchive': [years],
                'lowwot': [low],
                'highwot': [high],
                #'reponsetime': [vals],
                'url': [str(url)]}
        dfc = pd.DataFrame.from_dict(cols)
        #print(dfb)
        #print("Start: %s" % time.ctime())
        q.put(dfc)
    except:
        pass
        cols = {  # 'yeararchive': [years],
            'lowwot': [str('err')],
            'highwot': [str('err')],
            # 'reponsetime': [vals],
            'url': [str(url)]}
        dfc = pd.DataFrame.from_dict(cols)
        # print(dfb)
        # print("Start: %s" % time.ctime())
        q.put(dfc)

def f4(q, url):
    try:
        vals = requests.get(url, timeout=4, allow_redirects=False).elapsed.total_seconds()
        # try:
        #print("Start: %s" % time.ctime())
        # Instead of returning the result we put it in shared queue.
        cols = {#'yeararchive': [years],
                    #'lowwot': [low],
                    #'highwot': [high],
                    'reponsetime': [vals],
                    'url': [str(url)]}
        dfd = pd.DataFrame.from_dict(cols)
            #print(dfb)
            #print("Start: %s" % time.ctime())
        q.put(dfd)
    except:
        cols = {  # 'yeararchive': [years],
            # 'lowwot': [low],
            # 'highwot': [high],
            'reponsetime': [str('err')],
            'url': [str(url)]}
        dfd = pd.DataFrame.from_dict(cols)
        pass


def tmpFunc(df):
    delayed_results = []
    for row in df.itertuples():
        #try:
            url=row.url
            result_queue = Queue()

            # One Thread for response time
            t1 = Thread(target=f1, args=(result_queue, url))
            t2 = Thread(target=f2, args=(result_queue, url))
            t3 = Thread(target=f3, args=(result_queue, url))
            t4 = Thread(target=f4, args=(result_queue, url))
            # Starting threads...
            #print("Start: %s" % time.ctime())
            t1.start()
            t2.start()
            t3.start()
            t4.start()

            # Waiting for threads to finish execution...
            t1.join(4)
            t2.join(4)
            t3.join(4)
            t4.join(4)
    #t.join()
            #print("End:   %s" % time.ctime())

            # After threads are done, we can read results from the queue.
            if not result_queue.empty():
                try:
                    r2 = result_queue.get(f2)
                    r1 = result_queue.get(f1)
                    r3 = result_queue.get(f3)
                    r4 = result_queue.get(f4)
                    #r4 = result_queue.get(f4)
                    #print('slot 1')
                        #print(r1)
                        #print(r1)
                    #print('Slot2')
                        #print(r2)
                    #mergen
                    #try:
                    #df=pd.merge(r1, r2, on='url')
                    dfs = [r1, r2, r3, r4]
                    df = functools.reduce(lambda left, right: pd.merge(left, right, on='url'), dfs)
                    #df = df[['mean', 4, 3, 2, 1]]
                    #print('dss')
                    #print(dss)
                    #print('struct')

                    df = df[['fleschscore', 'highwot', 'lowwot', 'polarity', 'reponsetime', 'subjectivity', 'url', 'wordcount', 'yeararchive']]
                    #print (df)
                #return df
                except:

                    pass
                #print('df')
    return df



def applyParallel(dfGrouped, func):
    retLst = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(func)(group) for name, group in dfGrouped)
    return pd.concat(retLst)
# def applyParallel(dfGrouped, func):
#     with Pool(cpu_count()) as p:
#         #retLst = p.map(func, [group for name, group in dfGrouped])
#         retLst = p.map(func, [group for name, group in dfGrouped])
#     return pd.concat(retLst)

@app.route('/getterm', methods=['POST', 'GET'])
def get_term():
    if request.method == 'POST':
        tag = request.form['srch-term']
        tt = tag

        mg = MagicGoogle()
        lijst = []
        #tt = 'Donald Trump'
        search = str(tt+' language:english file:html')
        for url in mg.search_url(query=search):
            lijst.append(url)

        df = pd.DataFrame({'url': lijst})
        #print('parallel versionOzzy: ')
        dff = ((applyParallel(df.groupby(df.index), tmpFunc)))
        dff = dff.query('wordcount != "err" & reponsetime != "err" & highwot != "err" & yeararchive != "err"')
        #dff = dff[dff.wordcount != 'err' ]
        #dfeat = dff
        # dfeat =del dff['url']
        newX = dff.values
        # newX=np.delete(newX, [1, 3], axis=1)
        newX = np.delete(newX, [6], axis=1)
        # print(newX)
        #newX = newX[~np.isnan(newX).any(axis=1)]
        #newX = newX.as_matrix().astype(np.float)
        pickle_fname = 'pickle.model'
        pickle_model = pickle.load(open(pickle_fname, 'rb'))
        result = pickle_model.predict(newX)  # print (result)
        px2 = result.reshape((-1, 8))
        dffres = pd.DataFrame(
            {'OverallQuality': px2[:, 0], 'accuracy': px2[:, 1], 'completeness': px2[:, 2], 'neutrality': px2[:, 3],
             'relevance': px2[:, 4], 'trustworthiness': px2[:, 5], 'readability': px2[:, 6], 'precision': px2[:, 7]})

    return render_template('mp.html', dataframe=dff.to_html(index=False), res=dffres.to_html(index=False))


@app.route('/')
def home():
	return render_template('index.html')	
	
@app.route('/pres')
def pres():
    return redirect(url_for('static', filename='pres.html'))
    
@app.route('/getscore',methods=['POST','GET'])
def get_score():
    if request.method=='POST':
        tag = request.form['query']
        url=tag
        g = Goose ( )
        article = g.extract ( url=url )
        text = article.cleaned_text
        blob = TextBlob ( text )
        s = Textatistic ( text )
        vals = requests.get ( url , timeout=4 , allow_redirects=False ).elapsed.total_seconds ( )
        st = "/&callback=process&key=57bf606e01a24537ac906a86dc27891f94a0f587"
        # zz = urlopen ( url )
        quez = 'http://api.mywot.com/0.4/xpublic_link_json2?hosts=' + url + st
        stt = urllib.request.urlopen ( quez ).read ( )
        stt = str ( stt )
        wot = re.findall ( '\d+' , stt )
        ##z=[[conv(s) for s in line.split()] for line in wot]
        z = [ conv ( s ) for s in wot ]
        high = (z[ 1 ])
        low = (z[ 2 ])
        #print ( high , low )
        # WAYBACK
        zz = "{0.scheme}://{0.netloc}/".format ( urlsplit ( url ) )
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
                'url': [ url ]}
        dfeat = pd.DataFrame.from_dict ( cols )
        #df.to_csv ( 'ft.csv' , index=False , sep=',' , encoding='utf-8' )
        del dfeat[ 'url' ]
        #print (df)
        newX = dfeat.values
        pickle_fname = 'pickle.model'
        pickle_model = pickle.load ( open ( pickle_fname , 'rb' ) )
        result = pickle_model.predict ( newX )        #print (result)
        px2 = result.reshape((-1,8))
        dfres = pd.DataFrame({'OverallQuality':px2[:,0],'accuracy':px2[:,1],'completeness':px2[:,2],'neutrality':px2[:,3],'relevance':px2[:,4],'trustworthiness':px2[:,5],'readability':px2[:,6],'precision':px2[:,7]})
        tp = str(keywords(text, words=2))
        # comm = re.compile ( r"https?://(www\.)?" )
        # new_url = comm.sub ( '' , url ).strip ( ).strip ( '/' )
        # print (new_url)
        twtext = list ( )
        polar = list ( )
        datum = list ( )
        for tweet in query_tweets ( tp , 10 ):
            try:
                txt = tweet.text
                txt = re.sub ( r"http\S+" , "" , txt )
                dat = tweet.timestamp
                tblob = TextBlob ( txt )
                tpol = tblob.sentiment.polarity
                tal = tblob.detect_language()
                if tal == ('en'):
                    twtext.append ( txt )
                    polar.append ( tpol )
                    datum.append ( dat )
                else:
                    pass
            except:
                pass
    
    
        df = pd.DataFrame ( {'tweet': twtext , 'timestamp': datum , 'polarity': polar} )
        df[ 'timestamp' ] = pd.to_datetime ( df[ 'timestamp' ] )
        oldest = df[ 'timestamp' ].min ( )
        newest = df[ 'timestamp' ].max ( )
        total = (oldest - newest).total_seconds ( )
        gem = total / len ( df.index )
        #df.to_csv ( 'sentiment.csv' , index=False , sep=',' , encoding='utf-8' )
        tmean = df[ "polarity" ].mean ( )
        tsd = df[ "polarity" ].std ( )
        tkur = df[ "polarity" ].kurtosis ( )
        #topics
        # compile sample documents into a list
        tokenizer = RegexpTokenizer ( r'\w+' )
        stop = set ( stopwords.words ( 'english' ) )
        p_stemmer = PorterStemmer ( )
        doc_set = twtext
        texts = [ ]
    
        for i in doc_set:
            raw = i.lower ( )
            tokens = tokenizer.tokenize ( raw )
            stopped_tokens = [ i for i in tokens if not i in stop ]
            stemmed_tokens = [ p_stemmer.stem ( i ) for i in stopped_tokens ]
            texts.append ( stemmed_tokens )
        dictionary = corpora.Dictionary ( texts )
        corpus = [ dictionary.doc2bow ( text ) for text in texts ]
    
        ldamodel = gensim.models.ldamodel.LdaModel ( corpus , num_topics=1 , id2word=dictionary, minimum_phi_value=0.05)
        topic = ldamodel.print_topics ( num_topics=1, num_words = 1 )
        ctweets = {'meansentiment': [ tmean ] ,
                'sdpolarity': [ tsd ] ,
                'kurtosispolarity': [ tkur ] ,
                'tweetrate': [ gem ] ,
                'tweetcount': [ len ( df.index ) ] ,
                'topic': [ topic ] ,
                'url': [ url ]}
        dftwit = pd.DataFrame.from_dict ( ctweets )
        #entit
        my_sent = article.cleaned_text
        parse_tree = nltk.ne_chunk ( nltk.tag.pos_tag ( my_sent.split ( ) ) , binary=True )  # POS tagging before chunking!
        named_entities = [ ]
        for t in parse_tree.subtrees ( ):
            if t.label ( ) == 'NE':
                named_entities.append ( t )
        z = named_entities
        my_count = pd.Series ( z ).value_counts ( )
        df = pd.DataFrame ( my_count )
        df.columns = [ 'Count' ]
        df[ 'entity' ] = df.index
        za = df.assign ( entity=[ ', '.join ( [ x[ 0 ] for x in r ] ) for r in df.entity ] )
        df[ 'entities' ] = pd.DataFrame ( za[ 'entity' ] )
        del df[ 'entity' ]
        var_input = article.cleaned_text
        var_input = re.sub ( r'[\W\s\d]' , ' ' , var_input )
        input_tokenized = word_tokenize ( var_input , "english" )
        filtered_words = [ word for word in input_tokenized if word not in stopwords.words ( 'english' ) ]
    
        emotion_count = [ ]
    
        for i in range ( 0 , len ( filtered_words ) ):
            with open ( 'em.txt' ) as f:
                for line in f:
                    finaline = line.strip ( )
                    keym = re.search ( "'" + filtered_words[ i ] + "':\s'" , finaline )
                    if keym:
                        # print(keym)
                        valuem = re.findall ( ":\s'.*" , finaline )
                        newstr = str ( valuem )
                        finalvalue = re.sub ( r'[\W\s]' , ' ' , newstr )
                        emotion_count.append ( finalvalue.strip ( ) )
    
        emo = most_common ( emotion_count )
        # tp = str ( keywords ( var_input , words=2 ) )
        tijd = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        col2 = {'emotions': [ emo ] ,
                'topics': [ tp ] ,
                 'tittle': [ article.title ] ,
                 'published': [ article.publish_date ] ,
                 'authors': [ article.authors ] ,
                 'timestamp(gmtime)': [ tijd ] ,
                'url': [ url ]}
        df2 = pd.DataFrame.from_dict ( col2 )
    return render_template('tabs.html', dataframe=dfeat.to_html(index=False) , res=dfres.to_html(index=False), twit=dftwit.to_html(index=False), ent=df.to_html(index=False), des=df2.to_html(index=False))

    
#@app.route('/article')
#def article():
	#return tory(app.root_path + '/../static/', filename)    



#
@app.route('/article') # this is a job for GET, not POST
def article():
	return send_file('static/notfinalized.pdf',
                     mimetype='application/pdf',
                     attachment_filename='notfinalized.pdf',
                     as_attachment=True)	


@app.route('/feedback')
def index():
    OverallQuality_list = ['1', '2', '3', '4', '5']
    accuracy_list = ['1', '2', '3', '4', '5']
    completeness_list = ['1', '2', '3', '4', '5']
    neutrality_list = ['1', '2', '3', '4', '5']
    precision_list = ['1', '2', '3', '4', '5']
    readibility_list = ['1', '2', '3', '4', '5']
    relevance_list = ['1', '2', '3', '4', '5']
    trustworthiness_list = ['1', '2', '3', '4', '5']
    
    return render_template('feedback.html', OverallQuality_list=OverallQuality_list, accuracy_list=accuracy_list, completeness_list=completeness_list, neutrality_list=neutrality_list, precision_list=precision_list, readibility_list=readibility_list, relevance_list=relevance_list, trustworthiness_list=trustworthiness_list)

@app.route('/create', methods=['POST'])
def create_user():
    if request.form['name'] == '':
        flash('Name cannot be blank', 'nameError')
        return redirect('/feedback')
    if request.form['comment'] == '':
        flash('Comment cannot be blank', 'commentError')
        return redirect('//feedback')
    session['comment'] = request.form['comment']
    comment = countLetters(session['comment'])
    print (comment)
    if comment > 120:
        flash('Not more than 120 characters please', 'commentError')
        return redirect('//feedback')

    session['name'] = request.form['name']
    session['OverallQuality'] = request.form['OverallQuality']
    session['accuracy'] = request.form['accuracy']
    session['completeness'] = request.form['completeness']
    session['neutrality'] = request.form['neutrality']
    session['precision'] = request.form['precision']
    session['readibility'] = request.form['readibility']
    session['relevance'] = request.form['relevance']
    session['trustworthiness'] = request.form['trustworthiness']
    tijd = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
       # tijd = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    col2 = {'OverallQuality': (session['OverallQuality']),
             'accuracy': (session['accuracy']) ,
             'completeness': (session['completeness']) ,
             'neutrality':(session['neutrality']) ,
             'precision': (session['precision']) ,
             'readibility': (session['readibility']) ,
             'relevance': (session['relevance']) ,
             'trustworthiness': (session['trustworthiness']),
             'comment': (session['comment']),             
                'timestamp(gmtime)': [ tijd ]}
    fe = pd.DataFrame.from_dict ( col2 )
    if not os.path.isfile('feed.csv'):
        fe.to_csv('feed.csv', index=False)
    else: # else it exists so append without writing the header
        fe.to_csv('feed.csv',mode = 'a',header=False, index=False)
    return redirect('/process')



        

if __name__ == '__main__':
#~ #    app.run(debug=True)
#    app.run(threaded=True, host="0.0.0.0", port=80)
#s	app.run(processes=3)

#    app.run(host='0.0.0.0', port=80)   #app.run()


        

#if __name__ == '__main__':
#    app.run(debug=True)
#    app.run(threaded=True)
    app.run(host='127.0.0.1')
    #app.run(host='0.0.0.0')



