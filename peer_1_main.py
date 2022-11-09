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
        return 'The hours were successfully inserted into the timetable'
    except (Exception, psycopg2.DatabaseError) as error:
        return f'The hour were not inserted into the timetable, {error}'
    finally:
        if con is not None:
            con.close()



if __name__ == "__main__":
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
                print(f"Invalid time format. Insert: (yy-mm-dd)")
                continue
            
            start_time = input("Please insert the start time (00:00:00): ")
            try:
                validtime = datetime.strptime(start_time, "%H:%M:%S")
            except ValueError:
                print(f"Invalid time format. Insert: (00:00:00)")
                continue
            
            end_date = input("Please insert the ending date (yy-mm-dd): ")
            try:
                validtime = datetime.strptime(end_date, "%y-%m-%d")
            except ValueError:
                print(f"Invalid time format. Insert: (yy-mm-dd)")
                continue
            if datetime.strptime(end_date, "%y-%m-%d") < datetime.strptime(start_date, "%y-%m-%d"):
                print("End date cannot be before start date. Please insert the ending date again.")
                continue
            
            end_time = input("Please insert the end time (00:00:00): ")
            try:
                validtime = datetime.strptime(end_time, "%H:%M:%S")
            except ValueError:
                print(f"Invalid time format. Insert: (00:00:00)")
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


        

            






