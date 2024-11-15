from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/jmh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{'id': item.id, 'nombre': item.nombre, 'descripcion': item.descripcion} for item in items]
    return jsonify(items_list)

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Item(nombre=data['nombre'], descripcion=data.get('descripcion'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id, 'nombre': new_item.nombre, 'descripcion': new_item.descripcion}), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    item = Item.query.get_or_404(item_id)
    item.nombre = data['nombre']
    item.descripcion = data.get('descripcion')
    db.session.commit()
    return jsonify({'id': item.id, 'nombre': item.nombre, 'descripcion': item.descripcion})

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)
