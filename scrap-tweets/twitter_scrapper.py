from twitterscraper.query import query_single_page,query_tweets, query_user_info
from twitterscraper.ts_logger import logger
from get_username_from_user import get_username_from_user
import datetime as dt
import pandas as pd
import os

INIT_URL = 'https://twitter.com/search?f=tweets&vertical=default&q={q}&l={lang}'
RELOAD_URL = 'https://twitter.com/i/search/timeline?f=tweets&vertical=' \
             'default&include_available_features=1&include_entities=1&' \
             'reset_error_state=false&src=typd&max_position={pos}&q={q}&l={lang}'
INIT_URL_USER = 'https://twitter.com/{u}'
RELOAD_URL_USER = 'https://twitter.com/i/profiles/show/{u}/timeline/tweets?' \
                  'include_available_features=1&include_entities=1&' \
                  'max_position={pos}&reset_error_state=false'
PROXY_URL = 'https://free-proxy-list.net/'

def save_datasets(user):
    '''
    function to save datasets in a separate and organised location
    you will just need to pass user name to create a separate sections

    this function will follow '.. /.. /datasets/{user}'
    '''
    current_wd = os.getcwd()
    parent_wd = os.path.dirname(current_wd)
    user = user.lower()

    if not os.path.isdir(os.path.join(parent_wd,'datasets',user)):
        os.makedirs(os.path.join(parent_wd,'datasets',user))

    return os.path.join(parent_wd,'datasets',user)

def get_user_info(username):
    '''
    this function extracts user info such as total tweets and date of twitter account created
    this function returns user join date
    '''
    user_info = query_user_info(username)
    if(user_info == None):
        return None

    # convert twitter object into dictionary object
    user_info = user_info.__dict__
    
    total_tweets = user_info['tweets']
    
    user_joined_date = user_info['date_joined']
    user_joined_date = dt.datetime.strptime(user_joined_date, '%I:%M %p - %d %b %Y').date()

    user_info_dict = {
        'join_date': user_joined_date,
        'total_tweets': total_tweets
    }
    return user_info_dict

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
        user_info = get_user_info(user)
        count = user_info['total_tweets']
        origin_date = user_info['join_date']

        #origin_date= dt.date(2006, 3, 21)
        end_date = dt.date.today()
        #end_date = dt.date(2014,9,9) # This is for when you want to resume from a certain date

        timedelta=dt.timedelta(days=7)
        start_date = end_date-timedelta
        query = 'from:'+user
        tweets=[]
        counter=0
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

    # get file path
    filename = os.path.join(save_datasets(user), filename + '.csv' )

    # save file
    df.to_csv(filename,index=False)
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

#get_user_info()