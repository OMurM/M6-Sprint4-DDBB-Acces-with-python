from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_mysql')
def test_mysql():
    try:
        result = subprocess.run(['python', 'appconselect.py'], capture_output=True, text=True)
        output = result.stdout
        return render_template('test_mysql.html', output=output)
    except Exception as e:
        return f"An error occurred while running the MySQL test: {e}"

@app.route('/test_orm')
def test_orm():
    try:
        result = subprocess.run(['python', 'appconobject.py'], capture_output=True, text=True)
        output = result.stdout
        return render_template('test_orm.html', output=output)
    except Exception as e:
        return f"An error occurred while running the ORM test: {e}"

if __name__ == '__main__':
    app.run(debug=True)
