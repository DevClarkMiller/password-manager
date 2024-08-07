const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3');
const cookieParser = require('cookie-parser');
require('dotenv').config();
const app = express();

const port = process.env.PORT;
const DB_PATH = process.env.DB_PATH;

app.use(cookieParser());
app.use(cors());
app.use(express.json());

// Open connection with the database
const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE, (err) =>{
    if(err) return console.error(err);
    console.log('✅ database successfully connected!');
});

// Apply the routes here with the database and app as parameters 
require('./src/routes/accountRoute')(db, app);
require('./src/routes/passwordRoute')(db, app);

app.listen((port), () =>{
    console.log(`✅ server up on port: ${port}`);
});