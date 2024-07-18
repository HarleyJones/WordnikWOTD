import asyncio
import requests
from twikit import Client
import os
import base64
import json

# Initialize client with locale
client = Client('en-US')
wordnik_url = f'http://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={os.getenv("WORDNIK_API_KEY")}'

async def main():
    try:
        # Decode the cookies.json content from the environment variable
        cookies_json_content = os.getenv('COOKIES_JSON')
        if not cookies_json_content:
            raise ValueError("COOKIES_JSON environment variable is not set")

        cookies_json = base64.b64decode(cookies_json_content).decode('utf-8')

        # Save the decoded content to a temporary file
        with open('cookies.json', 'w') as file:
            file.write(cookies_json)
        
        client.load_cookies('cookies.json')

        # Get the word of the day from Wordnik
        response = requests.get(wordnik_url)
        response.raise_for_status()  # Ensure we notice bad responses
        data = response.json()

        word_of_the_day = data['word']
        definition = data['definitions'][0]['text']

        # Format the tweet
        tweet = f"📚 Word of the day: {word_of_the_day}\n\nDefinition: {definition}"

        # Create a tweet with the provided text
        await client.create_tweet(text=tweet)
        print("Tweet posted successfully!")

    except requests.RequestException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(main())
