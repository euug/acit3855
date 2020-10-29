import mysql.connector

db_conn = mysql.connector.connect(host="kafka-acit3855.eastus2.cloudapp.azure.com", user="user", password="password", database="tennisclub")

db_cursor = db_conn.cursor()

db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS court_booking
            (id INT NOT NULL AUTO_INCREMENT,
            member_id VARCHAR(250) NOT NULL,
            member_id_2 VARCHAR(250) NOT NULL,
            club_id VARCHAR(250) NOT NULL,
            court_num INTEGER NOT NULL,
            booking_time VARCHAR(100) NOT NULL,
            duration INTEGER NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            CONSTRAINT court_booking_pk PRIMARY KEY (id))
            ''')

db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS event_booking
            (id INT NOT NULL AUTO_INCREMENT, 
            member_id VARCHAR(250) NOT NULL,
            club_id VARCHAR(250) NOT NULL,
            event_id VARCHAR(250) NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            CONSTRAINT event_booking_pk PRIMARY KEY (id))
            ''')

db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS events
            (id INT NOT NULL AUTO_INCREMENT, 
            payload VARCHAR(250) NOT NULL,
            CONSTRAINT events_pk PRIMARY KEY (id)
            )
            ''')

db_conn.commit()
db_conn.close()
