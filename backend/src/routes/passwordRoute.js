module.exports = (db, app) =>{
    const passController = require('../controllers/passwordController')(db);
    app.route('/password')
        .get(passController.getPass)
        .post(passController.postPass)
        .put(passController.putPass)
        .delete(passController.deletePass);
};