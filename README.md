# mirror2media
Platform using NLP techniques to get the insights of famous journalists and media personalities eg. their alignments, bias etc. 

## Getting Started
* Install Pthon 3.7+ in your virtual environment


### To Scrap Tweets
* Go to the folder scrap-tweets
```
cd scrap-tweets
```
* Install Dependencies
```
pip install -r requirements.txt
```
* Run Script after changing the hard coded twitter handle in the function call. It will write twitter data to csv files after every 2000+ tweets. Search Range is from 2006-3-21 till current date. 
```
python twitter_scrapper.py
```


## Acknowledgments
* Twitter Scrap - https://github.com/taspinar/twitterscraper