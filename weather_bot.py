import tweepy
import requests
from config import *
from constance import *
import schedule

bot_api_client = tweepy.Client(bearer_token = BEARER_TOKEN,
                       consumer_key = TWITTER_API_KEY,
                       consumer_secret = TWITTER_API_SECRET_KEY,
                       access_token = TWITTER_ACCESS_TOKEN,
                       access_token_secret = TWITTER_ACCESS_TOKEN_SECRET)

def get_weather(city):
    WEATHER_URL = WEATHER_URL_TEMPLATE.format(key=WEATHER_API_KEY, city=city)
    response = requests.get(WEATHER_URL)
    if response.status_code == 200:
        return response.json()

    print(f"Error fetching weather data for {city}: Status Code {response.status_code}")
    return None

def create_weather_info_text(city):
    weather_data = get_weather(city)
    if weather_data:
        current = weather_data.get('current', {})
        condition = current.get('condition', {})
        text = condition.get('text', 'Unknown')
        temp_c = current.get('temp_c', 'Unknown')
        my_tweet = f"Today's weather in {city}: {temp_c}°C, {text}."
        return my_tweet
    else:
        return f"Could not retrieve weather data for {city}."



def tweet_post(tweet_text):
    if tweet_text:
        try:
            bot_api_client.create_tweet(text=tweet_text)
            print("Tweet posted successfully!")
        except tweepy.errors as err:
            print(f"Error posting weather tweet: {err}")
    else:
        print("Failed to create weather tweet.")

tweet_post(create_weather_info_text('istanbul'))