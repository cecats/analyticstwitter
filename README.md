```markdown
# analytics twitter

This Python script collects daily statistics from a specified Twitter account and sends the results to a specified Telegram group using a bot. The script runs daily at a specified time and logs all activities.

## Features

- Collects daily Twitter statistics (impressions, likes, retweets, replies, quotes).
- Calculates the change in follower count.
- Sends the statistics to a specified Telegram group using Markdown format.
- Logs all activities and errors.
- Configurable via `config.ini` file.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/twitter-daily-stats-bot.git
    cd twitter-daily-stats-bot
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `config.ini` file:**

    ```ini
    [Twitter]
    bearer_token = YOUR_BEARER_TOKEN_HERE
    username = TARGET_USERNAME_HERE
    initial_followers = 1000
    query_time = 08:00  # 查询的时间（24小时制，HH:MM）

    [Telegram]
    bot_token = YOUR_TELEGRAM_BOT_TOKEN_HERE
    chat_id = YOUR_TELEGRAM_CHAT_ID_HERE
    ```

## Usage

Run the script:

```sh
python twitter_daily_stats.py
```

The script will:

1. Wait until the specified `query_time`.
2. Fetch the daily statistics for the specified Twitter account.
3. Calculate the changes in statistics compared to the previous day.
4. Send the statistics to the specified Telegram group.
5. Log all activities and errors.

## Configuration

The `config.ini` file should contain the following sections:

- **Twitter API Configuration:**
  
    ```ini
    [Twitter]
    bearer_token = YOUR_BEARER_TOKEN_HERE
    username = TARGET_USERNAME_HERE
    initial_followers = 1000
    query_time = 08:00  # Time to run the query each day (24-hour format, HH:MM)
    ```

- **Telegram Bot Configuration:**
  
    ```ini
    [Telegram]
    bot_token = YOUR_TELEGRAM_BOT_TOKEN_HERE
    chat_id = YOUR_TELEGRAM_CHAT_ID_HERE
    ```

## Example

An example of the log message sent to Telegram:

```
*Statistics for yesterday for user: TARGET_USERNAME*
Time period: from 2023-05-20T00:00:00Z to 2023-05-21T00:00:00Z

*Total impressions:* 12345
*Total likes:* 678
*Total retweets:* 90
*Total replies:* 12
*Total quotes:* 34

*New followers:* 56
*Total followers:* 7890
```

## Logging

The script logs all activities and errors to `twitter_stats.log`.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
```
