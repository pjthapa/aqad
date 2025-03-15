def parseTopicChangeRequest(request_param):
    user_id = request_param["userId"]
    topic_id = request_param["topicId"]
    return user_id, topic_id
