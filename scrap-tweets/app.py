from get_username_from_user import get_username_from_user
from twitter_scrapper import get_user_info, save_datasets,get_user_tweets
import os
import pandas as pd

if __name__ == "__main__":
    user_list = get_username_from_user()
    
    for user in user_list:
        if(get_user_info(user) == None):
            df = pd.DataFrame({'USER DOES NOT EXIST':[]})
            df.to_csv(os.path.join(save_datasets(user), user + '.csv' ))
        else:
            get_user_tweets(user)