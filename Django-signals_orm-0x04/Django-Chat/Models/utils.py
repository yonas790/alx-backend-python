def get_threaded_replies(message):
    """
    Recursively build nested replies structure.
    """
    replies = []
    for reply in message.replies.all():
        replies.append({
            'message': reply,
            'replies': get_threaded_replies(reply)
        })
    return replies
