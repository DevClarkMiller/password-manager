const express = require('express');
const cors = require('cors');
require('dotenv').config();
const app = express();

const port = process.env.PORT;

app.use(cors());
app.use(express.json());


app.listen((port), () =>{
    console.log(`✅ server up on port: ${port}`);
});