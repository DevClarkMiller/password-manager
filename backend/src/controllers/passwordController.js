module.exports = (db) =>{
    const { encrypt, decrypt, decryptSources } = require('../utilities/encryption');
    const { blankNulls } = require('../utilities/misc');
    const { getAllPassSQL, getPassSQL, postPassSQL, putPassSQL, deletePassSQL } = require('../sql.json');

    const getAllPass = async (req, res) =>{
        console.log('Hit getAllPass controller');
        const { id } = req.account;

        db.all(getAllPassSQL, [id], function (err, rows) {
            if(err || !rows) {
                console.error(err);
                return res.status(404).send('User or source data not found');
            }

            // Need to decrypt the data before returning it to the user
            const decryptedSources = decryptSources(rows);

            if(decryptedSources.length > 0){
                res.json(decryptedSources);
            }else{
                console.log('No user passwords found, or issue with decrypting them');
                res.status(500).send('No user passwords found');
            }
        });
    }

    const getPass = async (req, res) =>{
        console.log('Hit getPass controller');
        const { site } = req.body;
        const { id } = req.account;

        db.get(getPassSQL, [id, site], function (err, row) {
            if(err || !row) {
                console.error(err);
             
                return res.status(404).send('User or source data not found');
            }
            // Need to decrypt the data before returning it to the user
            let { username, pass, note } = row;
            username = decrypt(username);
            pass = decrypt(pass);
            note = decrypt(note);
            res.json({ username: username, pass: pass, note: note, site: site });
        });
    }

    const postPass = async (req, res) =>{
        console.log('Hit postPass controller');
        let { username, pass, note, site } = req.body;
        const { id } = req.account;

        // Check if the req body data is undefined
        if(!username || !pass || !note || !site) return res.status(500).send("Some of the provided fields were not valid");

        // Encyrpt entered data **NOT HASH SINCE USERS WILL NEED TO ACCESS IN PLAIN TEXT**
        username = encrypt(username);
        pass = encrypt(pass);
        note = encrypt(note);

        db.run(postPassSQL, [username, pass, note, site, id], function (err) {
            if(err) {
                console.error(err);
                res.status(500).send("Couldn't add your entry to database");
            }else{
                res.status(200).send("Successfully added entry");
            }
        });
    }

    const putPass = async (req, res) =>{
        console.log('Hit putPass controller');
        let { username, pass, note, old_site, new_site } = req.body;
        const { id } = req.account;

        blankNulls([username, pass, note, old_site, new_site]);

        username = encrypt(username);
        pass = encrypt(pass);
        note = encrypt(note);

        const params = [username, pass, note, new_site, id, old_site];

        db.run(putPassSQL, params, function (err) {
            if(err) {
                console.error(err);
                return res.status(500).send('Something went wrong while trying to update source data, please try again later');
            }
            res.status(200).send('Information successfully updated');
        });
    }

    const deletePass = async (req, res) =>{
        console.log('Hit deletePass controller');
        const { site } = req.query;
        const { id } = req.account;

        db.run(deletePassSQL, [id, site], function (err) {
            if(err){
                console.error(err);
                return res.status(500).send("Issue with deleting data");
            }
            res.status(200).send("Source successfully deleted");
        });
    }

    return{
        getAllPass, 
        getPass,
        postPass,
        putPass,
        deletePass
    };
}