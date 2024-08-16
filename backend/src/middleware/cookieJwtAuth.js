module.exports = (db) => {
    const jwt = require('jsonwebtoken');

    const cookieJwtAuth = async (req, res, next) =>{
        // Sets the token based off of the query if given or the req cookies
        const token = req.cookies?.token;

        try{
            if(!token) throw new Error("Token not found");
            const decodedToken = await jwt.verify(token, process.env.JWT_SECRET);
            const { account } = decodedToken;
    
            const nowUNIX = Math.floor(new Date().getTime() / 1000);    //Get current time in unix format
            const timeLeft = decodedToken.exp - nowUNIX;
    
            if(timeLeft <= 300){ //If users token has less than 5 minutes left, sign a new one
                const newToken = jwt.sign({account: account}, process.env.JWT_SECRET, {expiresIn: "900s"});
                
                // Puts a token into the request header if a token was recieved in the query
                res.cookie("token", newToken, {
                    httpOnly: true, //Prevents browser javascript from seeing the cookies
                });
                console.log('Users token has been refreshed!');
            }
            
            req.account = account;
            next();
        }catch(err){
            //console.error(err);
            console.error("User token expired or doesn't exist");
            res.clearCookie("token");

            return res.status(403).send("User token expired or doesn't exist");
        }
    }

    return cookieJwtAuth;
}