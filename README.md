```markdown
# Twitter Daily Stats Bot / 推特每日统计机器人

This Python script collects daily statistics from a specified Twitter account and sends the results to a specified Telegram group using a bot. The script runs daily at a specified time and logs all activities.

这个Python脚本从指定的推特账户收集每日统计信息，并使用机器人将结果发送到指定的Telegram群组。脚本每天在指定时间运行，并记录所有活动。

## Features / 特点

- Collects daily Twitter statistics (impressions, likes, retweets, replies, quotes).
- Calculates the change in follower count.
- Sends the statistics to a specified Telegram group using Markdown format.
- Logs all activities and errors.
- Configurable via `config.ini` file.

- 收集每日推特统计信息（浏览量、点赞、转推、回复、引用）。
- 计算关注者数量的变化。
- 使用Markdown格式将统计信息发送到指定的Telegram群组。
- 记录所有活动和错误。
- 通过 `config.ini` 文件进行配置。

## Installation / 安装

1. **Clone the repository / 克隆仓库:**

    ```sh
    git clone https://github.com/cecats/analyticstwitter
    cd analyticstwitter
    ```

2. **Create and activate a virtual environment / 创建并激活虚拟环境:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages / 安装所需的包:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `config.ini` file / 创建 `config.ini` 文件:**

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

## Usage / 使用

Run the script:

运行脚本:

```sh
python twitter_daily_stats.py
```

The script will:

脚本将会:

1. Wait until the specified `query_time`.
2. Fetch the daily statistics for the specified Twitter account.
3. Calculate the changes in statistics compared to the previous day.
4. Send the statistics to the specified Telegram group.
5. Log all activities and errors.

1. 等待到指定的 `query_time`。
2. 获取指定推特账户的每日统计信息。
3. 计算与前一天相比的统计变化。
4. 将统计信息发送到指定的Telegram群组。
5. 记录所有活动和错误。

## Configuration / 配置

The `config.ini` file should contain the following sections:

`config.ini` 文件应包含以下部分:

- **Twitter API Configuration / 推特API配置:**
  
    ```ini
    [Twitter]
    bearer_token = YOUR_BEARER_TOKEN_HERE
    username = TARGET_USERNAME_HERE
    initial_followers = 1000
    query_time = 08:00  # Time to run the query each day (24-hour format, HH:MM)
    ```

- **Telegram Bot Configuration / Telegram机器人配置:**
  
    ```ini
    [Telegram]
    bot_token = YOUR_TELEGRAM_BOT_TOKEN_HERE
    chat_id = YOUR_TELEGRAM_CHAT_ID_HERE
    ```

## Example / 示例

An example of the log message sent to Telegram:

发送到Telegram的日志消息示例:

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

## Logging / 日志记录

The script logs all activities and errors to `twitter_stats.log`.

脚本将所有活动和错误记录到 `twitter_stats.log` 文件中。

## Contributing / 贡献

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

欢迎fork此仓库并提交pull request。如有重大更改，请先提交issue以讨论您想做的更改。

## License / 许可

This project is licensed under the MIT License.

本项目根据MIT许可证授权。
```
