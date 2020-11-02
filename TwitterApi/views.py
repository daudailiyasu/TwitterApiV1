"""
@Authors: Vidhi Shah, Sithara Krishna Murthy, Reetika Goel, Pragya Gautam
@Purpose: Views.py contains calls to 8 different Twitter APIs. It then passes responses to respective HTML pages to show on UI
"""

from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
import requests
import tweepy #https://github.com/tweepy/tweepy
import csv
import os
import json
#from tqdm import tqdm
from time import sleep
import oauth2 as oauth
from django.template import loader
from .apps import TwitterapiConfig
from django.http import HttpResponseServerError
from .forms import Twitter_Api,Twitter_Api_Hashtags

twitter_exception="<html><body background=#dddddd font-family:sans-serif><h1> Something is not happening!</h1></body></html>"
name = 'TwitterApi'
thisdict = {
  "consumer_key": "0",
  "consumer_secret": "0",
  "access_token":"0",
  "access_token_secret":"0"
}

#consumer_key:"QXrNpWVbUyYdiXVoUGtbZlDJL"
#consumer_secret:"lREYmZMZrm5tsWZfV9iChhmBSU8BtabIcQYeEuvI2hhu2AI2Lm"
#access_token:"105053184-1JHgKk8fxR6o7TljN5Sh1iQjEJXtiHtVGo2wyMvl"
#access_token_secret:"1LocIjNfQViocOhdkLiplUUiXeRD0mIGnH3vTBrUODCSw"
#consumer_key = "QXrNpWVbUyYdiXVoUGtbZlDJL"
#consumer_secret = "lREYmZMZrm5tsWZfV9iChhmBSU8BtabIcQYeEuvI2hhu2AI2Lm"
#access_token = "105053184-1JHgKk8fxR6o7TljN5Sh1iQjEJXtiHtVGo2wyMvl"
#access_token_secret = "1LocIjNfQViocOhdkLiplUUiXeRD0mIGnH3vTBrUODCSw"

def index(request):
    form = Twitter_Api(request.POST)
    if request.method=='POST':
        try:
            if form.is_valid():
                consumer_key = request.POST.get('consumer_key')
                consumer_secret = request.POST.get('consumer_secret')
                access_token = request.POST.get('access_token')
                access_token_secret = request.POST.get('access_token_secret')
                searchtag=request.POST.get('Hashtags')
                sincedate=request.POST.get('since_Date')
                untildate=request.POST.get('until_Date')
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                #auth.set_access_token(access_token, access_token_secret)
                #api = tweepy.API(auth)
                # Open/create a file to append data t
                api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True )
                public_tweet =tweepy.Cursor(api.search,
                                        q = searchtag,
                                        since = sincedate,
                                        until = untildate,
                                        lang = "en").items(100)

                filename=os.path.join(os.environ["HOMEDRIVE"],os.environ["HOMEPATH"], "Downloads","pythonscsv.csv")
                with open(filename,"a", encoding="utf-8") as f:
                    csvWriter = csv.writer(f)
                    csvWriter.writerow(['CREATED_AT', 'TWEET ID','LIKES COUNT','RETWEETS COUNT','USER ID','USER_LOCATION','USER_SCREEN_NAME' ,'SOURCE','TWEETS'])
                    for tweet in public_tweet:
                        #sleep(0.25)
                    # Write a row to the CSV file. I use encode UTF-8
                    #if (not tweet.retweeted) and ('RT @' not in tweet.text):
                        csvWriter.writerow([tweet.created_at,tweet.id,tweet.favorite_count, tweet.retweet_count, tweet.user.id,tweet.user.location,tweet.user.screen_name,tweet.source,tweet.text])
                        #print (tweet.created_at, tweet.text)
                    return redirect("sucex")
            else:
                form = Twitter_Api()

        except Exception as e:
            return redirect("loginmsg")
            print(e)
        
    return render(request, 'TwitterApi/home.html', {"form":form})

def callindex(request):
    if 'consumer_key' not in request.session and 'consumer_secret' not in request.session:
        return redirect("loginmsg")
    else:

        consumer_key=thisdict["consumer_key"]
        consumer_secret=thisdict["consumer_secret"]
        access_token=thisdict["access_token"]
        access_token_secret=thisdict["access_token_secret"]
        #consumer_key = request.session.get('consumer_key')
        #consumer_secret = request.session.get('consumer_secret')
        #access_token = request.session.get('access_token')
        #access_token_secret = request.session.get('access_token_secret')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        #auth.set_access_token(access_token, access_token_secret)
        form = Twitter_Api_Hashtags(request.POST)
        if request.method=='POST':
            if form.is_valid():
                searchtag=request.POST.get('Hashtags')
                sincedate=request.POST.get('since_Date')
                untildate=request.POST.get('until_Date')
                #auth.set_access_token(access_token, access_token_secret)
                #api = tweepy.API(auth)
                # Open/create a file to append data t
                api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True )
                public_tweet =tweepy.Cursor(api.search,
                                        q = searchtag,
                                        since = sincedate,
                                        until = untildate,
                                        lang = "en").items(10)

                filename=os.path.join(os.environ["HOMEDRIVE"],os.environ["HOMEPATH"], "Downloads","pythonscsv.csv")
                with open(filename,"a", encoding="utf-8") as f:
                    csvWriter = csv.writer(f)
                    csvWriter.writerow(['CREATED_AT', 'TWEET ID','LIKES COUNT','RETWEETS COUNT','USER ID','USER_LOCATION','USER_SCREEN_NAME' ,'SOURCE','TWEETS'])
                    for tweet in public_tweet:
                        #sleep(0.25)
                    # Write a row to the CSV file. I use encode UTF-8
                    #if (not tweet.retweeted) and ('RT @' not in tweet.text):
                        csvWriter.writerow([tweet.created_at,tweet.id,tweet.favorite_count, tweet.retweet_count, tweet.user.id,tweet.user.location,tweet.user.screen_name,tweet.source,tweet.text])
                        #print (tweet.created_at, tweet.text)
                    return redirect("sucex")
            else:
                form = Twitter_Api()
            
    
    return render(request, 'TwitterApi/ddd.html', {"form":form, "consumer_key":consumer_key,"access_token":access_token})

def succes(request):
    return render(request, 'TwitterApi/sucess.html')

def loginmsg(request):
    return render(request, 'TwitterApi/loginmsg.html')

    
# @Author: Sithara Krishna Murthy
# Authorize tokens and call api
def call_twitter_api(endpoint):
    oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    oauth_token = oauth.Token(key=access_token, secret=access_token_secret)
    client = oauth.Client(oauth_consumer, oauth_token)
    response, data = client.request(endpoint)
    return response, json.loads(data)

# @Author: Vidhi Shah
# Get Status User Timeline
def get_user_tweets(request):

    timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=Seekers Tweet&count=20"
    resp, tweets = call_twitter_api(timeline_endpoint)
    context = {'tweet': tweets}
    if resp.status != 200:
        print("status exception get_user_tweets", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        print("status working get_user_tweets", resp.status)
        return render(request, 'TwitterApi/getusertweet.html', context)

# @Author: Sithara Krishna Murthy
# Get Status Mention Timeline
def get_mention_tweets(request):
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/mentions_timeline.json?count=20"
    resp, mentions = call_twitter_api(timeline_endpoint)
    context = {'usermention': mentions}
    # for usermention in mentions:
    #     print('Mention id : ', usermention['id'], 'Mention Text :', usermention['text'])
    if resp.status != 200:
        print("status exception get_mention_tweets", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        print("status working get_mention_tweets", resp.status)
        return render(request, 'TwitterApi/getmentionstweet.html', context)

# @Author: Reetika Goel
# Get Status Based On Tweet Id
def get_id_based_tweets(request):
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/show.json?id=1049869614321000448"
    resp, id_tweets = call_twitter_api(timeline_endpoint)

    # print('\nTweet Id : ', id_tweets['id'], '\nTweet : ', id_tweets['text'], '\nTweet ScreenName : ',
    #       id_tweets['user']['screen_name'], '\nTweet Created At : ', id_tweets['user']['created_at'])
    context = {'id_tweet': id_tweets}
    if resp.status != 200:
        print("status exception get_id_based_tweets", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        print("status working get_id_based_tweets", resp.status)
        return render(request, 'TwitterApi/getidbasedtweet.html', context)

# @Author: Sithara Krishna Murthy
# Get Friends list
def get_friends(request):
    timeline_endpoint = "https://api.twitter.com/1.1/friends/list.json?cursor=-1&screen_name=Seekers " \
                        "Tweet&skip_status=true&include_user_entities=false "
    resp, friends_list = call_twitter_api(timeline_endpoint)

    # for friends in friends_list['users']:
    #     print('\nid : ', friends['id'], '\nName : ', friends['name'], '\nScreen Name : ', friends['screen_name'],
    #           '\nLocation : ', friends['location'], '\nFollowers Count : ', friends['followers_count'],
    #           '\nFriends Count : ', friends['friends_count'], '\nListed Count : ', friends['listed_count'],
    #           '\nFavourites Count : ', friends['favourites_count'])

    context = {'friends': friends_list['users']}
    if resp.status != 200:
        print("status exception get_friends", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        print("status working get_friends", resp.status)
        return render(request, 'TwitterApi/getfriends.html', context)

# @Author: Vidhi Shah
# Get Followers list
def get_followers(request):
    timeline_endpoint = "https://api.twitter.com/1.1/followers/list.json?cursor=-1&screen_name=Seekers " \
                        "Tweet&skip_status=true&include_user_entities=false "
    resp, followers_list = call_twitter_api(timeline_endpoint)

    # for followers in followers_list['users']:
    #     print('\nid : ', followers['id'], '\nName : ', followers['name'], '\nScreen Name : ', followers['screen_name'],
    #           '\nLocation : ', followers['location'], '\nFollowers Count : ', followers['followers_count'],
    #           '\nFriends Count : ', followers['friends_count'], '\nListed Count : ', followers['listed_count'],
    #           '\nFavourites Count : ', followers['favourites_count'])

    context = {'followers': followers_list['users']}
    if resp.status != 200:
        print("status exception get_followers", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        print("status working get_followers", resp.status)
        return render(request, 'TwitterApi/getfollowers.html', context)

# @Author: Pragya Gautam
# Get Account Settings
def get_account_settings(request):
    timeline_endpoint = "https://api.twitter.com/1.1/account/settings.json"
    resp, account_settings_list = call_twitter_api(timeline_endpoint)
    # print('\n','Screen Name : ',account_settings_list['screen_name'],
    #       '\n Geo Enabled : ',account_settings_list['geo_enabled'],'\n Language :', account_settings_list['language'],
    #       '\n Discoverable_by_email :', account_settings_list['discoverable_by_email'],
    #       '\n Discoverable_by_mobile_phone :', account_settings_list['discoverable_by_mobile_phone'])

    context = {'account_settings': account_settings_list}
    if resp.status != 200:
        print("status exception get_account_settings", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        print("status working get_account_settings", resp.status)
        return render(request, 'TwitterApi/getaccountsettings.html', context)

# @Author: Reetika Goel
# Get Twitters Privacy Policy
def get_privacy_policy(request):
    timeline_endpoint = "https://api.twitter.com/1.1/help/privacy.json"
    resp, privacy_policy_list = call_twitter_api(timeline_endpoint)
    # print("Twitter Privacy Policy\n", privacy_policy_list['privacy'])
    context = {'privacy_policy': privacy_policy_list}
    if resp.status != 200:
        print("status exception get_privacy_policy", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        print("status working get_privacy_policy", resp.status)
        return render(request, 'TwitterApi/getprivacypolicy.html', context)

# @Author: Pragya Gautam
# Get Twitters Terms of Service
def get_terms_of_service(request):
    timeline_endpoint = "https://api.twitter.com/1.1/help/tos.json"
    resp, terms_of_service_list = call_twitter_api(timeline_endpoint)
    # print("Twitter Terms of Service\n", terms_of_service_list['tos'])
    context = {'terms_of_service': terms_of_service_list}
    if resp.status != 200:
        print("status exception get_terms_of_service", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        print("status working get_terms_of_service", resp.status)
        return render(request, 'TwitterApi/gettermsofservice.html', context)