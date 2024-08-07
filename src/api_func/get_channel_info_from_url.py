
def get_channel_info(url, youtube=None):
    # URLからチャンネル名部分を抽出
    context = {}
    channel_name = url.split('/')[-1]
    channel_id = None

    if url is not None:
        # チャンネルを検索
        request = youtube.search().list(
            part='snippet',
            q=channel_name,
            type='channel'
        )
        response = request.execute()
        # 検索結果からチャンネルIDを取得
        if response['items']:
            channel_id = response['items'][0]['id']['channelId']
            channel_name = response['items'][0]['snippet']['title']
            context["channel_id"] = channel_id
            context["channel_name"] = channel_name
    if len(context) == 0:
        context['error'] = {
            'not_found': "Channel not found."
        }
    return context
