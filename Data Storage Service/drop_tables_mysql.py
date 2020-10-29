import mysql.connector

db_conn = mysql.connector.connect(host="kafka-acit3855.eastus2.cloudapp.azure.com", user="user", password="password", database="tennisclub")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          DROP TABLE court_booking, event_booking, events
          ''')

db_conn.commit()
db_conn.close()
