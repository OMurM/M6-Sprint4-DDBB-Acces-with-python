from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='jmh'
    )

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)

@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO items (nombre, descripcion) VALUES (%s, %s)',
        (new_item['nombre'], new_item['descripcion'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_item = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE items SET nombre = %s, descripcion = %s WHERE id = %s',
        (updated_item['nombre'], updated_item['descripcion'], item_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(updated_item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)
