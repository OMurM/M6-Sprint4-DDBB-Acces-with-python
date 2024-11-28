from flask import Flask, render_template, redirect, url_for, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_mysql')
def test_mysql():
    try:
        result = subprocess.run(['python', 'appconselect.py', 'fetch'], capture_output=True, text=True)
        output = result.stdout.strip()

        records = []
        if output:
            for line in output.splitlines():
                parts = line.split(", ")
                if len(parts) == 3:
                    record = (int(parts[0].split(": ")[1]), parts[1].split(": ")[1], parts[2].split(": ")[1])  # Parse ID, IP, and Status
                    records.append(record)

        return render_template('test_mysql.html', records=records)

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

@app.route('/add', methods=['POST'])
def add():
    ip_address = request.form.get('ip_address')
    status = request.form.get('status')
    subprocess.run(['python', 'appconselect.py', 'insert'], input=f"{ip_address}\n{status}\n", text=True)
    return redirect(url_for('test_mysql'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    subprocess.run(['python', 'appconselect.py', 'delete'], input=f"{id}\n", text=True)
    return redirect(url_for('test_mysql'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        ip_address = request.form.get('ip_address')
        status = request.form.get('status')
        subprocess.run(['python', 'appconselect.py', 'update'], input=f"{id}\n{ip_address}\n{status}\n", text=True)
        return redirect(url_for('test_mysql'))
    else:
        return render_template('update.html', id=id)

if __name__ == '__main__':
    app.run(debug=True)
