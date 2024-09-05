const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// MySQL bağlantı havuzu
const pool1 = mysql.createPool({
  host: 'mupeks.com',
  user: 'mupeksco_data',
  password: '664Gmm//*/',
  database: 'mupeksco_data',
  port: 3306
});

// MySQL bağlantı havuzu for sarem
const pool = mysql.createPool({
    host: 'saremelektromekanik.com',
    user: 'saremele_data',
    password: '664Gmm//*/',
    database: 'saremele_data',
    port: 3306
  });

// Bağlantı havuzunu kontrol et
pool.getConnection((err, connection) => {
  if (err) throw err;
  console.log('Connected to the database.');
  connection.release(); // Bağlantıyı serbest bırak
});

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// API endpoint for adding data
app.post('/add-data', (req, res) => {
  const { number, chrctr, text } = req.body;
  const sql = 'INSERT INTO base (number, chrctr, text) VALUES (?, ?, ?)';
  pool.query(sql, [number, chrctr, text], (err, results) => {
    if (err) throw err;
    res.redirect('/'); // Redirect back to the table view
  });
});

// API endpoint for editing data
app.post('/edit-data', (req, res) => {
    const { id, number, chrctr, text } = req.body;
    const sql = 'UPDATE base SET number = ?, chrctr = ?, text = ? WHERE id = ?';
    pool.query(sql, [number, chrctr, text, id], (err, results) => {
      if (err) throw err;
      res.send('Data updated successfully!');
    });
  });
  

// Root route
app.get('/', (req, res) => {
    const sql = 'SELECT * FROM base';
    pool.query(sql, (err, results) => {
      if (err) throw err;
      const ipAddress = 'mupeks.com'; // Eğer IP adresiniz farklıysa burayı değiştirin

      // HTML içeriği oluşturma
      let html = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Data Table</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
                .edit-button, .delete-button, .save-button, .cancel-button {
                    cursor: pointer;
                    color: blue;
                    text-decoration: underline;
                    border: none;
                    background: none;
                }
                .insert-form {
                    margin-top: 20px;
                }
                .editable {
                    display: none;
                }
                .info {
                    margin-bottom: 20px;
                    font-size: 16px;
                }
            </style>
        </head>
        <body>
            <div class="info">
                <h1>Database: mupeksco_data</h1>
                <p>User: mupeksco_data - Host: ${ipAddress}:3306</p>
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
                <tbody>`;
  
      // Verileri tabloya ekleme
      results.forEach(row => {
        html += `
          <tr id="row-${row.id}">
              <td>${row.id}</td>
              <td class="number-td" data-id="${row.id}">${row.number}</td>
              <td class="chrctr-td" data-id="${row.id}">${row.chrctr}</td>
              <td class="text-td" data-id="${row.id}">${row.text}</td>
              <td>
                <button class="edit-button" onclick="editRow(${row.id})">Edit</button>
                <button class="delete-button" onclick="deleteRow(${row.id})">Delete</button>
                <button class="save-button editable" onclick="saveRow(${row.id})">Save</button>
                <button class="cancel-button editable" onclick="cancelEdit(${row.id})">Cancel</button>
              </td>
          </tr>`;
      });
  
      // HTML içeriğini tamamla
      html += `
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
            <script>
              function editRow(id) {
                const row = document.getElementById('row-' + id);
                const numberCell = row.querySelector('.number-td');
                const chrctrCell = row.querySelector('.chrctr-td');
                const textCell = row.querySelector('.text-td');
                const editButton = row.querySelector('.edit-button');
                const deleteButton = row.querySelector('.delete-button');
                const saveButton = row.querySelector('.save-button');
                const cancelButton = row.querySelector('.cancel-button');
                
                numberCell.innerHTML = \`<input type="text" id="edit-number-\${id}" value="\${numberCell.innerText}"> \`;
                chrctrCell.innerHTML = \`<input type="text" id="edit-chrctr-\${id}" value="\${chrctrCell.innerText}"> \`;
                textCell.innerHTML = \`<input type="text" id="edit-text-\${id}" value="\${textCell.innerText}"> \`;
                
                editButton.style.display = 'none';
                deleteButton.style.display = 'none';
                saveButton.style.display = 'inline';
                cancelButton.style.display = 'inline';
              }
  
              function saveRow(id) {
                const number = document.getElementById('edit-number-' + id).value;
                const chrctr = document.getElementById('edit-chrctr-' + id).value;
                const text = document.getElementById('edit-text-' + id).value;
  
                fetch('/edit-data', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ id, number, chrctr, text }),
                })
                .then(response => response.text())
                .then(() => {
                  location.reload(); // Refresh the page to show updated data
                });
              }
  
              function cancelEdit(id) {
                const row = document.getElementById('row-' + id);
                row.querySelector('.number-td').innerHTML = row.querySelector('#edit-number-' + id).value;
                row.querySelector('.chrctr-td').innerHTML = row.querySelector('#edit-chrctr-' + id).value;
                row.querySelector('.text-td').innerHTML = row.querySelector('#edit-text-' + id).value;
  
                row.querySelector('.save-button').style.display = 'none';
                row.querySelector('.cancel-button').style.display = 'none';
                row.querySelector('.edit-button').style.display = 'inline';
                row.querySelector('.delete-button').style.display = 'inline';
              }
  
              function deleteRow(id) {
                if (confirm('Are you sure you want to delete this row?')) {
                  fetch('/delete-data', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id }),
                  })
                  .then(response => response.text())
                  .then(() => {
                    location.reload(); // Refresh the page to remove deleted data
                  });
                }
              }
            </script>
        </body>
        </html>`;
  
      // HTML içeriği döndür
      res.send(html);
    });
  });
  
  
  
  
  
// API endpoint for deleting data
app.post('/delete-data', (req, res) => {
    const { id } = req.body;
    const sql = 'DELETE FROM base WHERE id = ?';
    pool.query(sql, [id], (err, results) => {
      if (err) throw err;
      res.redirect('/'); // Redirect back to the table view
    });
  });
  


// Sunucuyu başlat
app.listen(port, '0.0.0.0',() => {
  console.log(`Server is running on http://allipaddresses from this port  ${port}`);
});
