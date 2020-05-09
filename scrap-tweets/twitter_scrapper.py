from twitterscraper.query import query_single_page,query_tweets
from twitterscraper.ts_logger import logger
import datetime as dt
import pandas as pd
INIT_URL = 'https://twitter.com/search?f=tweets&vertical=default&q={q}&l={lang}'
RELOAD_URL = 'https://twitter.com/i/search/timeline?f=tweets&vertical=' \
             'default&include_available_features=1&include_entities=1&' \
             'reset_error_state=false&src=typd&max_position={pos}&q={q}&l={lang}'
INIT_URL_USER = 'https://twitter.com/{u}'
RELOAD_URL_USER = 'https://twitter.com/i/profiles/show/{u}/timeline/tweets?' \
                  'include_available_features=1&include_entities=1&' \
                  'max_position={pos}&reset_error_state=false'
PROXY_URL = 'https://free-proxy-list.net/'

def query_tweets_from_user(user, limit=None):
    pos = None
    tweets = []
    try:
        while True:
           new_tweets, pos = query_single_page(user, lang='', pos=pos, from_user=True)
           if len(new_tweets) == 0:
               logger.info("Got {} tweets from username {}".format(len(tweets), user))
               return tweets

           tweets += new_tweets

           if limit and len(tweets) >= limit:
               logger.info("Got {} tweets from username {}".format(len(tweets), user))
               return tweets

    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Returning tweets gathered "
                     "so far...")
    except BaseException:
        logger.exception("An unknown error occurred! Returning tweets "
                          "gathered so far.")
    logger.info("Got {} tweets from username {}.".format(
        len(tweets), user))
    return tweets

def get_user_tweets(user):
    try:
        #do something
        origin_date=dt.date(2006, 3, 21)
        #end_date = dt.date.today()
        end_date = dt.date(2014,9,9)
        timedelta=dt.timedelta(days=7)
        start_date = end_date-timedelta
        query = 'from:'+user
        tweets=[]
        counter=18
        while(start_date>=origin_date):
            new_tweets= query_tweets(query, begindate=start_date, enddate=end_date)
            if(len(new_tweets)>0):
                tweets+=new_tweets
            
            if(len(tweets)>2000):
                counter=counter+1
                filename=user+'-tweetfile-'+str(counter)
                store_user_tweets_to_csv(tweets, user, filename)
                tweets=[]
            
            start_date=start_date-timedelta
            end_date=end_date-timedelta

            if(start_date<origin_date and end_date>origin_date):
                start_date=origin_date

        if(len(tweets)>0):
            counter=counter+1
            filename=user+'-tweetfile-'+str(counter)
            store_user_tweets_to_csv(tweets, user, filename)
            tweets=[]

    except Exception as ex:
        print(ex)

def store_user_tweets_to_csv(tweets,user, filename):
    df = pd.DataFrame(tweet.__dict__ for tweet in tweets)
    df = df[df['screen_name'] == user]
    df['text'] = df['text'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    df['text'] = df['text'].apply(lambda x: x.lower())
    df['message_text_only'] = df['text'].apply(lambda x: remove_url_from_text(x))
    df['url_links'] = df['text'].apply(lambda x: get_url_from_text(x))
    df.to_csv(filename + '.csv',index=False)
    print(filename+'.csv'+ ' Successfully Created')

def get_url_from_text(text):
    text_arr = text.split(' ')
    for t in text_arr:
        if("https://") in t: 
            return t[t.find('https://'):]
    return 'NA'

def remove_url_from_text(text):
    t = get_url_from_text(text)
    return text.replace(t,'')
#tweets = query_tweets_from_user('anshulkarasi')
#print(len(tweets))
get_user_tweets('sardesairajdeep')

#get_user_info()
