import schedule
import time
from api_func.live_stream import now_on_air
from api_func.get_channel_info_from_url import get_channel_info
from plyer import notification
import csv
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from pystray import Icon, MenuItem, Menu
from app_func.get_icon_image import get_icon_image
from app_func.get_menu_motion import get_menu_motion
import threading

# .envファイルの読み込み
load_dotenv()
API_KEY = os.getenv('YOUTUBE_DATA_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)

CHECK_SPAN = 300
stop_alert = threading.Event()


def main():
    # アプリ開始通知
    notification.notify(
        title="配信通知アラート:",
        message="配信通知ツールを起動します",
        app_name="Live alert"
    )

    schedule_thread = threading.Thread(target=start_live_alert)
    schedule_thread.start()

    start_ingecator()

    stop_alert.set()
    schedule_thread.join()

    notification.notify(
        title="配信通知アラート:",
        message="配信通知ツールを停止します",
        app_name="Live alert"
    )


def start_ingecator():
    # インジケータの制御
    icon_image = get_icon_image()
    menu = Menu(
        MenuItem("終了", get_menu_motion)
    )
    icon = Icon("test_icon", icon_image, menu=menu)
    icon.run()


def start_live_alert():
    # 指定時間ごとにjobを実行（今回は5分ごと）
    schedule.every(CHECK_SPAN).seconds.do(live_alert_tool)
    while not stop_alert.is_set():
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
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
