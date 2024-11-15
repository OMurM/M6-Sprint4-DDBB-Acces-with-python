import mysql.connector

def fetch_data():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        database='ping'
    )
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ping")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"ID: {row[0]}, Message: {row[1]}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    fetch_data()
