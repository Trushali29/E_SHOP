const sqlite3 = require('sqlite3').verbose();
const sell_id = [];
const customer = [];
const date = [];
const product = [];
const price = [];
const quantity = [];


// open the database
let db = new sqlite3.Database('D:/Eshop-main/GroceryManagement.db');
// query the table and retrieve data
db.all('SELECT * FROM sell', [], (err, rows) => {
  if (err) {
    throw err;
  }
  rows.forEach(row => {
    sell_id.push(row.id);
    customer.push(row.customer);
    date.push(row.date);
    product.push(row.product);
    price.push(row.price);
    quantity.push(row.quantity);
  });
console.log(sell_id.toString());
console.log(customer.toString());
console.log(date.toString());
console.log(product.toString());
console.log(price.toString());
console.log(quantity.toString());
});

// close the database
db.close();