module.exports = (db, app) =>{
    const accountController = require('../controllers/accountController')(db);
    const cookieJwtAuth = require('../middleware/cookieJwtAuth')(db);
    app.route('/account')
        .get(cookieJwtAuth, accountController.accountAuth)
        .post(accountController.login)
        .put(accountController.putAccount)
        .delete(accountController.deleteAccount);

    app.route('/account/create')
        .post(accountController.postAccount)

    app.route('/account/activate')
        .get(accountController.activateAccount);
};