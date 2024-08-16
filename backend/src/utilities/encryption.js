const fs = require('fs');
const crypto = require('crypto');
const bcrypt = require('bcryptjs');
const CRYPTO_ALGORITHM = process.env.CRYPTO_ALGORITHM;  
let key, iv, keyData = "", ivData = "";
const keyFilePath = './key.txt';
const ivFilePath = './iv.txt';

const genAndSaveKeyIv = () =>{
    key = crypto.randomBytes(32);
    iv = crypto.randomBytes(16);

    const keyBase64 = key.toString('base64');
    const ivBase64 = iv.toString('base64');

    fs.writeFileSync(keyFilePath, keyBase64, 'utf8');
    fs.writeFileSync(ivFilePath, ivBase64, 'utf8');
}

const checkKeyIvExist = () =>{
    if(fs.existsSync(keyFilePath) && fs.existsSync(ivFilePath)){
        keyData = fs.readFileSync(keyFilePath, { encoding: 'utf8' });
        ivData = fs.readFileSync(ivFilePath, { encoding: 'utf8' });
    }

    if(!keyData || !ivData){ 
        genAndSaveKeyIv();
    }else{
        key = Buffer.from(keyData, 'base64');
        iv = Buffer.from(ivData, 'base64');
    }
}

checkKeyIvExist();

const encrypt = (input) =>{
    try{
        const cipher = crypto.createCipheriv(CRYPTO_ALGORITHM, key, iv);
        let encrypted = cipher.update(input, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        return encrypted;
    }catch(err){
        console.error(err);
        return undefined;
    }
}

const decrypt = (input) =>{
    try{
        const decipher = crypto.createDecipheriv(CRYPTO_ALGORITHM, key, iv);
        let decrypted = decipher.update(input, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        return decrypted;
    }catch(err){
        console.error(err)
        return undefined;
    }
}

const decryptSources = (sources) =>{
    let decryptedSources = [];
    for(const source of sources){ 
        const decryptedSource = {
            username: decrypt(source.username),
            pass: decrypt(source.pass),
            note: decrypt(source.note),
            site: source.site
        }
        if(decryptedSource && decryptedSource.username){ decryptedSources.push(decryptedSource); }
    }
    return decryptedSources;
}

const verifyPassword = async (pass, hashedPass) =>{
    try{
        const match = await bcrypt.compare(pass, hashedPass);
        return match;
    }catch(err){
        return false;
    }
}

module.exports = {encrypt, decrypt, verifyPassword, decryptSources };