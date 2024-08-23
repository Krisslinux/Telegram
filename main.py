import telebot
import requests
import schedule
import time
import random

# Replace with your bot's API token
bot = telebot.TeleBot('7403216844:AAHSGHQswu-6OKOhiH8k8qGONnGfkp__Fhw')

# List of Telegram channel usernames
channels = ['theDankest_memes', 'unfilteredHumor', 'dev_meme', 'programmerjokes']

# Rate limiting parameters
max_requests_per_minute = 30  # Adjust as needed
min_delay_seconds = 60 / max_requests_per_minute

def fetch_photos(channel):
    offset = None
    photos = []

    while len(photos) < 20:
        try:
            updates = bot.get_updates(offset=offset)

            for update in updates:
                if 'message' in update and 'photo' in update['message']:
                    photo = update['message']['photo'][-1]['file_id']
                    file_path = bot.get_file(photo).file_path
                    url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'
                    response = requests.get(url)
                    with open(f'photo_{len(photos)}.jpg', 'wb') as f:
                        f.write(response.content)
                    photos.append(photo)
                    offset = update['update_id'] + 1

                    # Introduce a random delay to avoid hitting rate limits
                    time.sleep(random.uniform(min_delay_seconds / 2, min_delay_seconds))
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error fetching updates: {e}")
            time.sleep(60)  # Wait for a minute before retrying

def main():
    for channel in channels:
        fetch_photos(channel)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Bot is running! 🤖")

# Schedule the main function to run daily
schedule.every().day.at('00:00').do(main)

# Start the bot
bot.polling()
