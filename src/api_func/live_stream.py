

def now_on_air(channel_id=None, youtube=None):
    context = {}
    if channel_id is not None:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            eventType='live',
            type='video'
        )
        response = request.execute()
        if response['items']:
            context['item'] = {
                "title": response['items'][0]['snippet']["title"]
            }
    if len(context) == 0:
        context["error"] = {
            "not_found": "Live not found."
        }
    return context
