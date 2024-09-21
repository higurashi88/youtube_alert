from PIL import Image, ImageDraw

# アイコン用の画像を取得する関数


def get_icon_image():
    # 色を設定 (color1: 背景色, color2: 四角形の色)
    color1 = "white"   # 背景色
    color2 = "black"   # 四角形の色

    # 画像を作成 (64x64ピクセル)
    image = Image.new('RGB', (64, 64), color1)
    d = ImageDraw.Draw(image)

    # 四角形を描画 (中央に配置)
    d.rectangle([16, 16, 48, 48], fill=color2)

    return image
