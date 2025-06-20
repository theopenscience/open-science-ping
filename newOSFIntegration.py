import requests
import tweepy
import keys
import time

# Initialize Twitter client
client = tweepy.Client(
    keys.bearer_token,
    keys.consumer_key,
    keys.consumer_secret,
    keys.access_token,
    keys.access_token_secret
)

# Optional: store already tweeted IDs to avoid duplicates (simple cache in memory for now)
tweeted_ids = set()

def fetch_recent_registrations():
    """
    Fetch the latest registrations from OSF via the public API.
    """
    url = 'https://api.osf.io/v2/registrations/?sort=-date_created&page[size]=5'
    response = requests.get(url)
    data = response.json()
    return data.get('data', [])

def format_tweet(registration):
    """
    Format the tweet text from a registration object.
    """
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
                time.sleep(2)  # avoid rate limits
            except Exception as e:
                print(f"Error tweeting: {e}")

def main():
    print("Checking for new OSF registrations to tweet...")
    tweet_new_registrations()
    print("Done.")

if __name__ == "__main__":
    main()
