import schedule
import time
from api_func.live_stream import now_on_air
from api_func.get_channel_info_from_url import get_channel_info
from plyer import notification
import csv
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

# .envファイルの読み込み
load_dotenv()
API_KEY = os.getenv('YOUTUBE_DATA_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)

CHECK_SPAN = 300


def main():
    notification.notify(
        title="配信通知アラート:",
        message="配信通知ツールを起動します",
        app_name="Live alert"
    )

    # 指定時間ごとにjobを実行（今回は5秒ごと）
    schedule.every(CHECK_SPAN).seconds.do(live_alert_tool)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            notification.notify(
                title="配信通知アラート:",
                message="配信通知ツールを停止します",
                app_name="Live alert"
            )
            break


def live_alert_tool():
    live_list = []
    with open('url_list.csv', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        # url
        for row in csv_reader:
            channel_info = get_channel_info(row[0], youtube=youtube)
            if 'error' not in channel_info:
                target_live = now_on_air(
                    channel_info['channel_id'], youtube=youtube)
                if 'error' not in target_live:
                    live_list.append(target_live["item"]["title"])

            for live in live_list:
                notification.notify(
                    title="配信中:",
                    message=live,
                    app_name="Live alert"
                )


if __name__ == "__main__":
    main()
