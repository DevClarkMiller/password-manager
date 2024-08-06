const crypto = require('crypto');
const bcrypt = require('bcryptjs');
const CRYPTO_ALGORITHM = process.env.CRYPTO_ALGORITHM;

const encrypt = (input) =>{
    const key = crypto.randomBytes(32);
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(CRYPTO_ALGORITHM, key, iv);

    input = cipher.update(input, 'utf8', 'hex') += cipher.final('hex');
    return input;
}

const decrypt = (input) =>{
    const decipher = crypto.createDecipheriv(CRYPTO_ALGORITHM, key, iv);
    input = decipher.update(encrypted, 'hex', 'utf8') += decipher.final('utf8');
    return input;
}

const verifyPassword = async (pass, hashedPass) =>{
    try{
        const match = await bcrypt.compare(pass, hashedPass);
        return match;
    }catch(err){
        return false;
    }
}

module.exports = {encrypt, decrypt, verifyPassword};