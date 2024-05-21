import requests
import datetime
import configparser
import csv
import os
import time
import logging

# 设置日志配置
logging.basicConfig(filename='twitter_stats.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取配置文件中的值
BEARER_TOKEN = config['Twitter']['bearer_token']
USERNAME = config['Twitter']['username']
INITIAL_FOLLOWERS = int(config['Twitter']['initial_followers'])
QUERY_TIME = config['Twitter']['query_time']
CSV_FILE = 'followers.csv'

# 获取Telegram配置文件中的值
TELEGRAM_BOT_TOKEN = config['Telegram']['bot_token']
TELEGRAM_CHAT_ID = config['Telegram']['chat_id']

def create_headers(bearer_token):
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    return headers

def get_user_id(username, headers):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logging.error(f"Error fetching user ID: {response.status_code} {response.text}")
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
    return response.json()['data']['id']

def get_user_tweets(user_id, start_time, end_time, headers):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "start_time": start_time,
        "end_time": end_time,
        "tweet.fields": "public_metrics"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"Error fetching user tweets: {response.status_code} {response.text}")
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
    return response.json()

def get_user_metrics(user_id, headers):
    url = f"https://api.twitter.com/2/users/{user_id}?user.fields=public_metrics"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logging.error(f"Error fetching user metrics: {response.status_code} {response.text}")
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
    return response.json()

def read_followers_from_csv(file_path):
    if not os.path.exists(file_path):
        return None, None
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            return int(row[0]), row[1]
    return None, None

def write_followers_to_csv(file_path, followers_count):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([followers_count, datetime.datetime.utcnow().isoformat()])

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        logging.error(f"Error sending message to Telegram: {response.status_code} {response.text}")

def main():
    try:
        headers = create_headers(BEARER_TOKEN)
        
        # 获取用户ID
        user_id = get_user_id(USERNAME, headers)
        
        # 获取昨天的日期
        end_time = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = end_time - datetime.timedelta(days=1)
        
        # 转换时间格式为ISO 8601/RFC 3339格式
        start_time_str = start_time.isoformat() + 'Z'
        end_time_str = end_time.isoformat() + 'Z'
        
        # 获取昨天的推文
        tweets = get_user_tweets(user_id, start_time_str, end_time_str, headers)
        
        total_impressions = 0
        total_likes = 0
        total_retweets = 0
        total_replies = 0
        total_quotes = 0
        
        if 'data' in tweets:
            for tweet in tweets['data']:
                metrics = tweet['public_metrics']
                total_impressions += metrics.get('impression_count', 0)
                total_likes += metrics.get('like_count', 0)
                total_retweets += metrics.get('retweet_count', 0)
                total_replies += metrics.get('reply_count', 0)
                total_quotes += metrics.get('quote_count', 0)
        
        # 获取用户的关注者数据
        user_metrics = get_user_metrics(user_id, headers)
        current_followers = user_metrics['data']['public_metrics']['followers_count']
        
        # 读取CSV文件中的总关注者数量
        previous_followers, last_recorded_time = read_followers_from_csv(CSV_FILE)
        if previous_followers is None:
            previous_followers = INITIAL_FOLLOWERS
        
        # 计算新增关注者
        new_followers = current_followers - previous_followers
        
        # 输出统计数据
        log_message = (f"*Statistics for yesterday for user: {USERNAME}*\n"
                       f"Time period: from {start_time_str} to {end_time_str}\n\n"
                       f"*Total impressions:* {total_impressions}\n"
                       f"*Total likes:* {total_likes}\n"
                       f"*Total retweets:* {total_retweets}\n"
                       f"*Total replies:* {total_replies}\n"
                       f"*Total quotes:* {total_quotes}\n\n"
                       f"*New followers:* {new_followers}\n"
                       f"*Total followers:* {current_followers}")
        logging.info(log_message)
        print(log_message)
        
        # 发送Telegram消息
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, log_message)
        
        # 更新CSV文件中的总关注者数量
        write_followers_to_csv(CSV_FILE, current_followers)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def wait_until_query_time(query_time_str):
    query_time = datetime.datetime.strptime(query_time_str, '%H:%M').time()
    now = datetime.datetime.now()
    query_datetime = datetime.datetime.combine(now.date(), query_time)
    if now > query_datetime:
        query_datetime += datetime.timedelta(days=1)
    wait_seconds = (query_datetime - now).total_seconds()
    wait_message = f"Waiting for next query time ({query_time_str}). Next check at: {query_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
    print(wait_message)
    time.sleep(wait_seconds)

if __name__ == "__main__":
    while True:
        wait_until_query_time(QUERY_TIME)
        main()
        # 计算下一次查询的时间
        now = datetime.datetime.now()
        query_time = datetime.datetime.strptime(QUERY_TIME, '%H:%M').time()
        next_query_time = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), query_time)
        next_query_message = f"Next query will be at: {next_query_time.strftime('%Y-%m-%d %H:%M:%S')}"
        logging.info(next_query_message)
        print(next_query_message)
        # 直接等待到下一次查询时间
        wait_seconds = (next_query_time - now).total_seconds()
        time.sleep(wait_seconds)