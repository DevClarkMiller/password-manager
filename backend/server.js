const path = require('path');
const dotenv = require('dotenv');
const env = process.env.NODE_ENV || "development";
const envFile = `.env.${env}`;
dotenv.config({ path: path.resolve(process.cwd(), envFile) });

const express = require('express');
const ipCheck = require('./src/middleware/ipCheck');
const cors = require('cors');
const sqlite3 = require('sqlite3');
const cookieParser = require('cookie-parser');

const app = express();

const port = process.env.PORT;
const DB_PATH = process.env.DB_PATH;

const corsConfig = {
    origin: process.env.ALLOWED_ORIGIN,
    credentials: true
}

app.use(ipCheck);
app.use(cors(corsConfig));
app.use(cookieParser());
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