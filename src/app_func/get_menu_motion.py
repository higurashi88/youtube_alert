from pystray import Icon, MenuItem, Menu
# メニューのアクション


def get_menu_motion(icon, item):
    if str(item) == "終了":
        icon.stop()
