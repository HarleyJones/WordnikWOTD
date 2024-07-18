import asyncio
import requests
from twikit import Client

# Initialize client
client = Client('en-US')
wordnik_url = 'http://api.wordnik.com/v4/words.json/wordOfTheDay?api_key=1380d58b8b5c33325130c0e8f340be6bc6fba6f7bb65bfc6f'

async def main():
    client.load_cookies('cookies.json')
    
    # Get the word of the day from Wordnik
    response = requests.get(wordnik_url)
    data = response.json()
    word_of_the_day = data['word']
    definition = data['definitions'][0]['text']

    # Format the toot
    tweet = f"📚 Word of the day: {word_of_the_day}\n\nDefinition: {definition}"

    # Create a tweet with the provided text and attached media
    await client.create_tweet(
        text=tweet,
    )

asyncio.run(main())