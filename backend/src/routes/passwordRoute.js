module.exports = (db, app) =>{
    const passController = require('../controllers/passwordController')(db);
    const cookieJwtAuth = require('../middleware/cookieJwtAuth')(db);
    app.route('/password')
        .get(cookieJwtAuth, passController.getPass)
        .post(cookieJwtAuth, passController.postPass)
        .put(cookieJwtAuth, passController.putPass)
        .delete(cookieJwtAuth, passController.deletePass);

    app.route('/password/all')
        .get(cookieJwtAuth, passController.getAllPass)

    app.route('/test')
        .get((req, res) =>{
            res.send(`This is a test, your origin is ${req.get('host')}`)
        })
}