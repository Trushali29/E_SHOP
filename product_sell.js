const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('D:/Eshop-main/GroceryManagement.db');

// query the table and retrieve data
db.all('SELECT * FROM products', [], (err, rows) => {
  if (err) {
    throw err;
  }
  rows.forEach(row => {
    console.log(row.product); // output each row to the console
  });
});

// close the database
db.close();