import boto3
import psycopg2
from botocore.exceptions import ClientError

def get_secret():

    secret_name = "Peer_1_secrets"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return secret

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

def retrive_message_total_hours_worked():
    con = None
    try:
        database_secrets = eval(get_secret())
        con = psycopg2.connect(host=database_secrets['host'], database=database_secrets['database'], port=database_secrets['port'], user=database_secrets['user'], password=database_secrets['password'])
        cursor = con.cursor()
        SQL = 'SELECT sum(ending-starting) from timetable;'
        cursor.execute(SQL)
        wanted_data = cursor.fetchall()
        cursor.close()
        return wanted_data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

def retrive_message_all_inclusions():
    con = None
    try:
        database_secrets = eval(get_secret())
        con = psycopg2.connect(host=database_secrets['host'], database=database_secrets['database'], port=database_secrets['port'], user=database_secrets['user'], password=database_secrets['password'])
        cursor = con.cursor()
        SQL = 'SELECT * from timetable;'
        cursor.execute(SQL)
        wanted_data = cursor.fetchall()
        cursor.close()
        return wanted_data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

def format_message(total_hours, worked_hours):
    forwarded_message= ''
    forwarded_message = 'Total time spent: ' + str(total_hours[0][0]) + ' hours:minutes:seconds' + '\n' + '\n' + 'All logged hours:' + '\n'
    for i in range (0, len(worked_hours)):
        forwarded_message = forwarded_message + '\n'
        forwarded_message = forwarded_message + '* ' + 'From ' + str(worked_hours[i][1]) + ' To ' + str(worked_hours[i][2]) + ' Worked on project: ' + str(worked_hours[i][3]) + ' on tasks: ' + str(worked_hours[i][4])

    return forwarded_message



# this_topic = 'time_table_report'
# create_topic_1(this_topic)
# subscribe_to_topic_2('arn:aws:sns:us-east-1:341014156608:time_table_report', 'katri.palmroth@brightstraining.com')
publish_message('arn:aws:sns:us-east-1:341014156608:time_table_report', format_message(retrive_message_total_hours_worked(), retrive_message_all_inclusions()))