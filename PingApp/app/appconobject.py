from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/ping'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Ping(db.Model):
    __tablename__ = 'ping'  # Ensure the table name is 'ping'
    
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the table
    ip_address = db.Column(db.String(255), nullable=False)  # IP address column
    status = db.Column(db.String(50), nullable=True)  # Status column, can be NULL
    timestamp = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())  # Timestamp with default

    def __repr__(self):
        return f'<Ping {self.id}: {self.ip_address} - {self.status} - {self.timestamp}>'

def fetch_data():
    pings = Ping.query.all()
    
    print("Fetching all pings from the database:")
    for ping in pings:
        print(f"ID: {ping.id}, IP Address: {ping.ip_address}, Status: {ping.status}, Timestamp: {ping.timestamp}")
    
    return pings

@app.route('/test_orm')
def test_orm():
    try:
        pings = fetch_data()
        return render_template('test_orm.html', pings=pings)
    except Exception as e:
        return f"An error occurred while running the ORM test: {e}"

if __name__ == '__main__':
    app.run(debug=True)
