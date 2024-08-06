module.exports = (db) =>{
    const { encrypt, decrypt } = require('../utilities/encyrption');
    const { getPassSQL, postPassSQL, putPassSQL, deletePassSQL } = require('../sql.json');

    const getPass = async (req, res) =>{
        console.log('Hit getPass controller');
        const { site } = req.body;
        const { user_id } = req.account;

        db.get(getPassSQL, [user_id, site], function (err, row) {
            if(err || row) {
                console.error(err);
             
                return res.status(404).send('User or source data not found');
            }
            // Need to decrypt the data before returning it to the user
            let { user, pass, note } = row;
            user = decrypt(user);
            pass = decrypt(pass);
            note = decrypt(note);
            res.send({ user: user, pass: pass, note: note, site: site });
        });
    }

    const postPass = async (req, res) =>{
        console.log('Hit postPass controller');
        let { user, pass, note, site } = req.body;
        const { user_id } = req.account;

        // Check if the req body data is undefined
        if(!user || !pass || !note || !site) return res.status(500).send("Some of the provided fields were not valid");

        // Encyrpt entered data **NOT HASH SINCE USERS WILL NEED TO ACCESS IN PLAIN TEXT**
        user = encrypt(user);
        pass = encrypt(pass);
        note = encrypt(note);

        db.run(postPassSQL, [user, pass, note, site, user_id], function (err) {
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
        let { user, pass, note, site } = req.body;
        const { user_id } = req.account;

        user = encrypt(user);
        pass = encrypt(pass);
        note = encrypt(note);

        db.run(putPassSQL, [user, pass, note, user_id, site], function (err) {
            if(err) {
                console.error(err);
                res.status(500).send('Something went wrong while trying to update source data, please try again later');
            }
            res.status(200).send('Information successfully updated');
        });
    }

    const deletePass = async (req, res) =>{
        console.log('Hit deletePass controller');
        const { site } = req.body;
        const { user_id } = req.account;

        db.run(deletePassSQL, [user_id, site], function (err) {
            if(err){
                console.error(err);
                res.status(500).send("Issue with deleting data");
            }else{
                res.status(200).send("Source successfully deleted");
            }
        });
    }

    return{
        getPass,
        postPass,
        putPass,
        deletePass
    };
}