import requests
from bs4 import BeautifulSoup
import json
import tweepy
import keys

tweet_text="This is a new test tweet from the OSF link scraper script.";
client = tweepy.Client(keys.bearer_token
                       , keys.consumer_key
                       , keys.consumer_secret
                       , keys.access_token
                       , keys.access_token_secret)


def get_links_from_osf():
    """
    Fetches all links from the OSF website.
    """
    # Define the URL to scrape
    url = 'https://osf.io/'  # Replace with your target URL

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for a_tag in soup.find_all('a', href=True):
        links.append(a_tag['href'])

    for link in links:
        print(link)


# Post to Twitter
def tweet(text: str):
    client.create_tweet(text=text)    



def main():
    """
    Main function to execute the script.
    """
    print("Starting the script...")
    tweet(tweet_text)
    print("Script completed.")

if __name__ == "__main__":
    main()