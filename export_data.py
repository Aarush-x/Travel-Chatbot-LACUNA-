import os
import csv
import mysql.connector
from mysql.connector import Error

DB_USER = os.environ.get('DB_USER', 'travelbot')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password123')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'TravelBot')


def connect_db():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8'
        )
    except Error as err:
        print(f"Database connection error: {err}")
        return None


def export_table(table_name, out_file):
    conn = connect_db()
    if conn is None:
        return False
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        with open(out_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)
        print(f"Exported {len(rows)} rows to {out_file}")
        return True
    except Error as err:
        print(f"Error exporting {table_name}: {err}")
        return False
    finally:
        conn.close()


if __name__ == '__main__':
    export_table('Places', 'Places.csv')
    export_table('Hotels', 'Hotels.csv')
