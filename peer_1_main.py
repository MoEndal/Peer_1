from datetime import datetime
import psycopg2
from config import config

def turn_into_datetime(given_date, given_time):
    datetime_str = given_date + " " + given_time
    datetime_object = datetime.strptime(datetime_str, '%y-%m-%d %H:%M:%S')

    return datetime_object

def insert_into_timetable(start_date, start_time, end_date, end_time, project, tasks):
    con = None
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor()
        cursor.execute("""
        INSERT INTO timetable (starting, ending, project, tasks) VALUES (%s, %s, %s, %s)
        """,
        (turn_into_datetime(start_date, start_time), turn_into_datetime(end_date, end_time), project, tasks))
        con.commit()
        # print 
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()




if __name__ == "__main__":
        # start_date = input("Please insert the start date (yyyy-mm-dd): ")
        # start_time = input("Please insert the start time (00:00:00): ")
        # end_date = input("Please insert the ending date (yyyy-mm-dd): ")
        # end_time = input("Please insert the end time (00:00:00): ")
        # project = input("Please insert the project the work is aimed at: ")
        # tasks = input("Please insert the tasks worked on: ")

        insert_into_timetable('22-08-11', '09:00:00', '22-08-11', '12:00:00', 'project 1', 'github')






