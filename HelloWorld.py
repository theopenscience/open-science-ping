import requests
import tweepy
import os
import time

# Load from environment
bearer_token = os.environ['BEARER_TOKEN']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']

client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

tweeted_ids = set()

def fetch_recent_registrations():
    url = 'https://api.osf.io/v2/registrations/?sort=-date_created&page[size]=5'
    response = requests.get(url)
    data = response.json()
    return data.get('data', [])

def format_tweet(registration):
    title = registration['attributes']['title']
    date = registration['attributes']['date_created'][:10]
    link = registration['links']['html']
    return f"📢 New OSF Registration!\n📝 {title}\n📅 {date}\n🔗 {link} #OpenScience #OSF"

def tweet_new_registrations():
    registrations = fetch_recent_registrations()
    for reg in registrations:
        reg_id = reg['id']
        if reg_id not in tweeted_ids:
            tweet_text = format_tweet(reg)
            try:
                client.create_tweet(text=tweet_text)
                print(f"Tweeted: {tweet_text}")
                tweeted_ids.add(reg_id)
                time.sleep(2)
            except Exception as e:
                print(f"Error tweeting: {e}")

def main():
    print("Checking for new OSF registrations to tweet...")
    tweet_new_registrations()
    print("Done.")

if __name__ == "__main__":
    main()
