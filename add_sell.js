const product_name = process.argv[2];
const price = parseInt(process.argv[3]);
const quantity = parseInt(process.argv[4]);
const customer = process.argv[5];
var date = new Date();
var month = date.getMonth()+1;
//to get last two digits of year
var year = date.getFullYear().toString().slice(-2);
var current_date = month+"/"+date.getDate()+"/"+year;
// get number of 3 digits between 111 to 999
var sell_id = Math.floor(Math.random() * (999-111+1)) + 111;
//console.log(product_name,price,quantity);

const sqlite3 = require('sqlite3').verbose();

// Open a SQLite database
const db = new sqlite3.Database('D:/Eshop-main/GroceryManagement.db');

// Create a table
db.run('CREATE TABLE IF NOT EXISTS sell (id TEXT, customer TEXT, date TEXT, product TEXT, price INTEGER, quantity INTEGER)');

// Insert a value into the table
db.run('INSERT INTO sell (id, customer, date, product, price, quantity) VALUES (?, ?, ?, ?, ?, ?)', ["S"+sell_id,customer,current_date,product_name,price,quantity], function(err) {
  if (err) {
    console.log(err.message);
  } else {
    console.log(`A row has been inserted with rowid ${this.lastID}`);
  }
});
// Close the database connection
db.close();