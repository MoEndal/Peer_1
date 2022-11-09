from datetime import datetime
import psycopg2
import boto3
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

def turn_into_datetime(given_date, given_time):
    datetime_str = given_date + " " + given_time
    datetime_object = datetime.strptime(datetime_str, '%y-%m-%d %H:%M:%S')

    return datetime_object

def insert_into_timetable(start_date, start_time, end_date, end_time, project, tasks):
    con = None
    try:
        database_secrets = eval(get_secret())
        con = psycopg2.connect(host=database_secrets['host'], database=database_secrets['database'], port=database_secrets['port'], user=database_secrets['user'], password=database_secrets['password'])
        cursor = con.cursor()
        cursor.execute("""
        INSERT INTO timetable (starting, ending, project, tasks) VALUES (%s, %s, %s, %s)
        """,
        (turn_into_datetime(start_date, start_time), turn_into_datetime(end_date, end_time), project, tasks))
        con.commit()
        # print 
        cursor.close()
        return 'The hours were successfully inserted into the timetable'
    except (Exception, psycopg2.DatabaseError) as error:
        return 'The hour were not inserted into the timetable'
    finally:
        if con is not None:
            con.close()



if __name__ == "__main__":
    # insert_into_timetable('22-11-09', '09:00:00', '22-11-09', '12:00:00', 'project 1', 'db secrets')
    while True:
        print ("""
        1.Insert work hours into the timetable
        2.Exit/Quit
        """)
        ans=input("What would you like to do? ") 
        if ans=="1": 
            print("\nAdd work hours")

            start_date = input("Please insert the start date (yy-mm-dd): ")
            try:
                validtime = datetime.strptime(start_date, "%y-%m-%d")
            except ValueError:
                print("Invalid time format. Insert: (yy-mm-dd)")
                continue
            
            start_time = input("Please insert the start time (00:00:00): ")
            try:
                validtime = datetime.strptime(start_time, "%H:%M:%S")
            except ValueError:
                print("Invalid time format. Insert: (00:00:00)")
                continue
            
            end_date = input("Please insert the ending date (yy-mm-dd): ")
            try:
                validtime = datetime.strptime(end_date, "%y-%m-%d")
            except ValueError:
                print("Invalid time format. Insert: (yy-mm-dd)")
                continue
            if datetime.strptime(end_date, "%y-%m-%d") < datetime.strptime(start_date, "%y-%m-%d"):
                print("End date cannot be before start date. Please insert the ending date again.")
                continue
            
            end_time = input("Please insert the end time (00:00:00): ")
            try:
                validtime = datetime.strptime(end_time, "%H:%M:%S")
            except ValueError:
                print("Invalid time format. Insert: (00:00:00)")
                continue

            project = input("Please insert the project the work is aimed at: ")
            
            tasks = input("Please insert the tasks worked on: ")

            print('')

            print(insert_into_timetable(start_date, start_time, end_date, end_time, project, tasks))

        elif ans=="2":
            print("\nGoodbye") 
            break
        elif ans !="":
            print("\n Not Valid Choice Try again") 


        

            






