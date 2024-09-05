from flask import Flask, request, redirect, render_template_string
import mysql.connector
from mysql.connector import pooling

app = Flask(__name__)
port = 3001

# MySQL bağlantı havuzu (mupeks)
pool1 = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mupeks_pool",
    pool_size=5,
    host='mupeks.com',
    user='mupeksco_data',
    password='664Gmm//*/',
    database='mupeksco_data',
    port=3306
)

# MySQL bağlantı havuzu (sarem)
pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="sarem_pool",
    pool_size=5,
    host='saremelektromekanik.com',
    user='saremele_data',
    password='664Gmm//*/',
    database='saremele_data',
    port=3306
)

# API endpoint for adding data
@app.route('/add-data', methods=['POST'])
def add_data():
    number = request.form['number']
    chrctr = request.form['chrctr']
    text = request.form['text']
    sql = 'INSERT INTO base (number, chrctr, text) VALUES (%s, %s, %s)'
    
    conn = pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (number, chrctr, text))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

# API endpoint for editing data
@app.route('/edit-data', methods=['POST'])
def edit_data():
    id = request.json['id']
    number = request.json['number']
    chrctr = request.json['chrctr']
    text = request.json['text']
    sql = 'UPDATE base SET number = %s, chrctr = %s, text = %s WHERE id = %s'
    
    conn = pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (number, chrctr, text, id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return 'Data updated successfully!'

# Root route
@app.route('/')
def index():
    conn = pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM base')
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    ip_address = 'mupeks.com'
    
    # HTML template
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Table</title>
        <style>
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .edit-button, .delete-button, .save-button, .cancel-button {
                cursor: pointer; color: blue; text-decoration: underline; border: none; background: none;
            }
            .insert-form { margin-top: 20px; }
            .editable { display: none; }
            .info { margin-bottom: 20px; font-size: 16px; }
        </style>
    </head>
    <body>
        <div class="info">
            <h1>Database: mupeksco_data</h1>
            <p>User: mupeksco_data - Host: {{ ip_address }}:3306</p>
        </div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Number</th>
                    <th>Character</th>
                    <th>Text</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
            {% for row in results %}
                <tr id="row-{{ row['id'] }}">
                    <td>{{ row['id'] }}</td>
                    <td class="number-td" data-id="{{ row['id'] }}">{{ row['number'] }}</td>
                    <td class="chrctr-td" data-id="{{ row['id'] }}">{{ row['chrctr'] }}</td>
                    <td class="text-td" data-id="{{ row['id'] }}">{{ row['text'] }}</td>
                    <td>
                        <button class="edit-button" onclick="editRow({{ row['id'] }})">Edit</button>
                        <button class="delete-button" onclick="deleteRow({{ row['id'] }})">Delete</button>
                        <button class="save-button editable" onclick="saveRow({{ row['id'] }})">Save</button>
                        <button class="cancel-button editable" onclick="cancelEdit({{ row['id'] }})">Cancel</button>
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
        <div class="insert-form">
            <h2>Insert New Entry</h2>
            <form method="post" action="/add-data">
                <label for="number">Number:</label>
                <input type="text" id="number" name="number" required>
                <label for="chrctr">Character:</label>
                <input type="text" id="chrctr" name="chrctr" required>
                <label for="text">Text:</label>
                <input type="text" id="text" name="text" required>
                <button type="submit">Insert</button>
            </form>
        </div>
    </body>
    </html>
    '''

    return render_template_string(html, results=results, ip_address=ip_address)

# API endpoint for deleting data
@app.route('/delete-data', methods=['POST'])
def delete_data():
    id = request.json['id']
    sql = 'DELETE FROM base WHERE id = %s'
    
    conn = pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

# Sunucuyu başlat
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
