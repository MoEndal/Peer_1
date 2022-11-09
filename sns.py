import boto3

def create_topic_1(topic_name):
    client = boto3.client('sns')
    response = client.create_topic(
    Name=topic_name)

    return response['TopicArn']

def subscribe_to_topic_2(topicarn, email):
    client = boto3.client('sns')
    response = client.subscribe(
    TopicArn=topicarn,
    Protocol='email',
    Endpoint=email)
    return response['SubscriptionArn']

def publish_message(topicarn, message):
    client = boto3.client('sns')
    response = client.publish(
        TopicArn=topicarn,
        Message=message)
    message_id = response['MessageId']
    return message_id

this_topic = 'time_table_report'
# create_topic_1(this_topic)
# subscribe_to_topic_2('arn:aws:sns:us-east-1:341014156608:time_table_report', 'katri.palmroth@brightstraining.com')
publish_message('arn:aws:sns:us-east-1:341014156608:time_table_report', "this is a test message on topic")