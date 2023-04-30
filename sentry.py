from telethon.sync import TelegramClient
from colorama import Style
from telethon import types
from colorama import Fore
import configparser
import datetime
import pytz
import os
import time

config = configparser.ConfigParser()
config.read('config.ini') # reading the config.ini file
api_id = config.getint('Telegram', 'api_id') # replace with your own api_id in `config.ini`
api_hash = config.get('Telegram', 'api_hash') # replace with your own api_hash in `config.ini`
channel_name = config.get('Telegram', 'channel_name') # replace with your specific logs channel name in `config.ini`
logs_dir = config.get('Telegram', 'logs_dir') # replace with the folder name you want to save files in it
days_back = config.getint('Telegram', 'days_back') # replace with the number of days you want to go back in time in `config.ini`
monitor_seconds = config.getint('Telegram', 'waiting_time') # replace with how many seconds you want the script to wait until to check again

if logs_dir == "":
    logs_dir = "Saved_Logs"

class SentryEye:
    def __init__(self, api_id: int, api_hash: str, channel_name: str, logs_dir: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.channel_name = channel_name
        self.logs_dir = logs_dir

    def progress_callback(self, current, total):
        print(f"{Fore.GREEN}Downloaded: {Fore.YELLOW}{current / 1024 / 1024:.2f}MB / {total / 1024 / 1024:.2f}MB{Fore.WHITE} ({current * 100 / total:.1f}%)")

    def download_logs(self):
        client = TelegramClient('scraping_session', self.api_id, self.api_hash)
        with client:
            tz = pytz.utc # set timezone to UTC
            last_message_date = datetime.datetime.now(tz=tz) # start from today
            if days_back <= 0:
                # set last_message_date to start from the beginning of today
                last_message_date = last_message_date.replace(hour=0, minute=0, second=0, microsecond=0)
                print(f"{Fore.YELLOW}You chossed to download today's messages.\n========================\n{Fore.WHITE}")
            else:
                # set last_message_date to start from the specified number of days ago
                last_message_date = last_message_date - datetime.timedelta(days=days_back)
                print(f"{Fore.YELLOW}You chossed to download messages for the past {days_back} days.\n========================{Fore.WHITE}")

            while True:
                messages = client.iter_messages(self.channel_name, offset_date=last_message_date, reverse=True)
                found_new_logs = False # initialize to false
                for message in messages:
                    if isinstance(message, types.Message) and message.file and message.file.name and message.file.name.endswith('.rar'):
                        logs_filename = message.file.name
                        if not os.path.exists(f'{self.logs_dir}/{logs_filename}'):
                            found_new_logs = True # found new logs file
                            print(f"{Fore.GREEN}Found New Logs file: {Fore.YELLOW}{logs_filename}{Fore.WHITE}")
                            message.download_media(file=os.path.join(self.logs_dir, logs_filename), progress_callback=self.progress_callback)
                        else:
                            print(f"{Fore.RED}Skipped {logs_filename} already exists")
                    last_message_date = message.date.astimezone(tz) # make the datetime aware of the timezone
                    if days_back <= 0:
                        # stop after downloading today's messages
                        if last_message_date.date() < datetime.datetime.now(tz=tz).date():
                            break
                    else:
                        # stop after the specified number of days
                        if last_message_date < datetime.datetime.now(tz=tz) - datetime.timedelta(days=days_back):
                            break
                if not found_new_logs:

                    print(f"{Fore.YELLOW}Last File was {Fore.WHITE}[{Fore.GREEN}{logs_filename}{Fore.WHITE}].")
                    print(f"{Fore.YELLOW}No new logs found.{Fore.WHITE}")
                    print(f"{Fore.CYAN}Waiting {monitor_seconds}.{Fore.WHITE}")

                time.sleep(monitor_seconds) # sleep for 5 minutes before checking for new logs again

sentry_downloader = SentryEye(api_id, api_hash,channel_name, logs_dir)
sentry_downloader.download_logs()
