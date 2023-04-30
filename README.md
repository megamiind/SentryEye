# SentryEye
This is a Python script that can be used to download logs from a specific Telegram channel. The tool will start scraping logs from a specified channel, starting from the most recent message and working backwards in time or the opposite based on your time value. When it finds a message containing a rar file attachment, it will download the file.

## Requirements

-   Python 3.x
-   `configparser` module (can be installed via pip)
-   `telethon` module (can be installed via pip)
-   `colorama` module (can be installed via pip)
-   `pytz` module (can be installed via pip)

## Getting started
1.  Clone the repository or download the files.
2.  Install the required dependencies by running `pip install -r requirements.txt`.
3.  Replace the `api_id`, `api_hash`, and `channel_name` variables in `config.ini` with your own Telegram API credentials and the name of the channel you want to scrape.
## Configuring the `config.ini` file

The `config.ini` file should be in the following format:



	[Telegram]
	api_id = <your_api_id>
	api_hash = <your_api_hash>
	channel_name = <logs_channel_name>
	days_back = <how_many_days_back>
	waiting_time = <monitor_sleep_seconds>

 

-   `<your_api_id>` and `<your_api_hash>` should be replaced with your own Telegram API credentials. You can obtain these credentials by following the instructions at [https://my.telegram.org/](https://my.telegram.org/).
-   `<logs_channel_name>` should be replaced with the name of the logs channel you want to download logs from.
- `<how_many_days_back>` should be replaced with the number of days you want to go back in time. If you set days_back to 0, it will only download the files that were sent on the current day.
- `<monitor_sleep_seconds>` should be replaced with the how many waiting time between monitoring intervals (in seconds)

Note: Please do not include any quotes in the `config.ini` file.
## Usage

1.  Run the script by typing `python sentry.py` in the command line.
2.  The script will connect to the Telegram API using the credentials in the `config.ini` file.
3.  The script will download all new logs from the specified channel.

Note: Maybe Telegram will ask you to type your number and then the verification code that's normal.

# Demo

I made a small demo and made the script to break after downloading the file to be able to exit from asciinema.

[![asciicast](https://asciinema.org/a/I1FGw5rObgch5o2WypGMKYYOV.svg)](https://asciinema.org/a/I1FGw5rObgch5o2WypGMKYYOV)

## Contributing

Contributions to the script are welcome. If you find any bugs or have any suggestions for improvement, please open an issue or submit a pull request.
