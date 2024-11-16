import mysql.connector

def connect_db():
    """Establece la conexión con la base de datos."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        database='ping'
    )

def fetch_data():
    """Leer todos los datos de la tabla ping."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ping")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def insert_data(ip_address, status):
    """Insertar un nuevo registro en la tabla ping."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ping (ip_address, status) VALUES (%s, %s)", (ip_address, status))
    conn.commit()
    cursor.close()
    conn.close()

def update_data(id, ip_address, status):
    """Actualizar un registro existente."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE ping SET ip_address=%s, status=%s WHERE id=%s", (ip_address, status, id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_data(id):
    """Eliminar un registro por ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ping WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "fetch"

    if action == "fetch":
        data = fetch_data()
        for row in data:
            print(f"ID: {row[0]}, IP Address: {row[1]}, Status: {row[2]}")
    elif action == "insert":
        ip_address = input("Enter IP Address: ")
        status = input("Enter Status: ")
        insert_data(ip_address, status)
        print("Data inserted successfully.")
    elif action == "update":
        id = int(input("Enter ID to update: "))
        ip_address = input("Enter new IP Address: ")
        status = input("Enter new Status: ")
        update_data(id, ip_address, status)
        print("Data updated successfully.")
    elif action == "delete":
        id = int(input("Enter ID to delete: "))
        delete_data(id)
        print("Data deleted successfully.")
