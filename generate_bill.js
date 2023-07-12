const sqlite3 = require('sqlite3').verbose();
const product = [];
const price = [];
const quantity = [];
const customer= process.argv[2];
const date = process.argv[3];

// open the database
let db = new sqlite3.Database('D:/Eshop-main/GroceryManagement.db');
// query the table and retrieve data
db.all('SELECT * FROM sell WHERE Customer = ? AND Date = ?', [customer,date], (err, rows) => {
  if (err) {
    throw err;
  }
  rows.forEach(row => {
    product.push(row.product);
    price.push(row.price);
    quantity.push(row.quantity);
  });

console.log(product.toString());
console.log(price.toString());
console.log(quantity.toString());
});

// close the database
db.close();