module.exports = (db) =>{
    const path = require('path');
    const fs = require('fs');
    const { getAccountSQL, postAccountSQL, activateAccountSQL } = require('../sql.json');
    const { verifyPassword } = require('../utilities/encyrption');
    const bcrypt = require('bcryptjs');
    const salt = bcrypt.genSaltSync(5);
    const jwt = require('jsonwebtoken');
    const handlebars = require('handlebars');

    const mailer = require('../utilities/mailing');

    const html_activation_path = './src/email-templates/account_confirmation.html'

    const accountAuth = async (req, res) =>{
        console.log('Hit isUserAuth controller');    

        let account = req.account;

        if(!account) return res.status(403).send("User isn't authorized");
        delete account.id;  //Removes the id from the return value of this function
        delete account.password;

        res.json(account);
    }

    const login = async (req, res) =>{
        console.log('Hit login controller');

        const { email, password, is_non_browser} = req.body;

        try{
            db.get(getAccountSQL, [email], async function (err, row){
                if(err){
                    console.error(err);
                    return res.status(404).send("User not found");
                }

                if(!row || !row?.password|| row?.status === "not-active") 
                    return res.status(404).send("User not found, or account isn't activated!");

                const passMatches = await verifyPassword(password, row.password);
                if(!passMatches) return res.status(403).send(`Your login details seem to be incorrect`);

                // If non browser, send the token in the json instead of as a cookie
                const token = jwt.sign({account: row}, process.env.JWT_SECRET, {expiresIn: "900s"});
                const account = {
                    email: row.email,
                    first_name: row.first_name,
                    last_name: row.last_name,
                    status: row.status,
                    type: row.type
                };

                if(is_non_browser == "true"){
                    res.json({
                        account: account,
                        token: token
                    });
                }else{
                    res.cookie("token", token, {
                        httpOnly: true,
                    });

                    res.json(account);
                }
            });

        }catch(err){
            console.error(err);
            res.status(400).send(err.message);
        }
    }

    const activateAccount = async (req, res) =>{
        console.log('Hit activateAccount controller');
        const token = req.query.token;

        if(!token) return res.status(404).send('Account token not provided!');

        try{
            const { account } = await jwt.verify(token, process.env.JWT_SECRET);

            if(!account || !account?.id) {
                console.error('Link for account authentication has expired!');
                return res.status(410).send('Link for account authentication has expired!');   //NOTE - GIVE USERS ABILITY TO GENERATE A NEW LINK!}
            }

            db.run(activateAccountSQL, [account.id], function(err){
                if(err){
                    res.status(404).send("Couldn't find account or something went wrong when trying to authenticate!");
                }else{
                    console.log('Users account has now been verified');
                    res.status(200).send("Your account has been successfully activated");
                }
            });
        }catch(err){
            res.status(400).send('Token is malformed!');
        }
    }

    const postAccount = async (req, res) =>{
        console.log('Hit postAccount controller');
        const { email, password, firstname, lastname } = req.body;

        if(!email || !password || !firstname || !lastname) return res.status(500).send("One or more crucial fields weren't provided");

        // Create account 
        try{
            //1. Hash + Salt password
            const hashedPass = await bcrypt.hash(password, salt);
            const params = [email, firstname, lastname, hashedPass, "not-active", 1];
            
            //2. Run query
            db.run(postAccountSQL, params, async function(err){
                if(err){
                    console.error(err);
                    return res.status(500).send("Error encountered with creating account");
                }

                console.log(`USER WITH EMAIL: ${email} HAS BEEN CREATED WITH AN ID OF: ${this.lastID}`);

                const account = {
                    id: this.lastID,
                    email: email,
                    password: hashedPass,
                    first_name: firstname,
                    last_name: lastname,
                    status: "not-active",
                    type: "Basic"
                };

                const token = jwt.sign({account: account}, process.env.JWT_SECRET, {expiresIn: "900s"});
                console.log('NEW TOKEN CREATED');

                // Send activation email
                const BASE_URL = process.env.ACTIVATE_BASE_URL;

                const queryParams = new URLSearchParams({
                    token: token
                });
                
                const fullUrl = `${BASE_URL}?${queryParams.toString()}`;

                fs.readFile(path.resolve(html_activation_path), {encoding: 'utf-8'}, (err, html) =>{
                    if(err) {
                        console.log(path.resolve(html_activation_path));
                        console.log(err);
                    }else{
                        const template = handlebars.compile(html);
                        const confirmation_html = template({confirmation_url: fullUrl});

                        // Send the email
                        mailer.mailActivation(email, confirmation_html);
                        res.status(200).send("Email confirmation sent!");
                    }
                });
            });

        }catch(err){
            console.error(err);
            res.status(500).send("Something went wrong while creating account :/");
        }
    }

    const putAccount = async (req, res) =>{
        
    }

    const deleteAccount = async (req, res) =>{
        
    }

    return{
        accountAuth,
        login,
        postAccount,
        putAccount,
        deleteAccount,
        activateAccount
    };
}