import psycopg2

conn = psycopg2.connect(
        database='postgres_db',
        user='root',
        password='root',
        host='localhost',
        port='5432'
        )

# Create a cursor - this is a special object that makes
# queries and receives their results

cursor = conn.cursor()

# HERE WILL BE OUR DATABASE WORK CODE
# Do not forget to close the database connection

conn.close()