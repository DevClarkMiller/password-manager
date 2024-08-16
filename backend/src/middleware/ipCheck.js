const ipCheck = (req, res, next) =>{
    require('dotenv').config();

    const allowed_origin = process.env.PROXY_IP;
    const headers = req.headers;
    const NO_ACCESS_MSG = "Access denied, requests must come through the official channels only";

    // Allows access if the x-real-ip isn't present, this means that the request is coming from local host
    // which is okay for development, but not good for production
    if (!headers['x-real-ip']){
        //console.log(headers)
        console.log('x-real-ip not found, this means request is coming from localhost');
        if (process.env.LOCAL_ACCESS === "true")
            return next();
        return res.status(403).send(NO_ACCESS_MSG);
    }
   
    if (headers['x-real-ip'] === allowed_origin){
        console.log("User has been properly proxied, access granted!")
        return next();
    }
    console.log("IP DOESN'T MATCH!");
    res.status(403).send(NO_ACCESS_MSG);
}

module.exports = ipCheck