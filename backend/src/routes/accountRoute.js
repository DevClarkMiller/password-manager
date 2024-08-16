module.exports = (db, app) =>{
    const accountController = require('../controllers/accountController')(db);
    const cookieJwtAuth = require('../middleware/cookieJwtAuth')(db);
    app.route('/account')
        .get(cookieJwtAuth, accountController.accountAuth)
        .post(accountController.login)
        .put(cookieJwtAuth, accountController.putAccount)
        .delete(cookieJwtAuth, accountController.deleteAccount);

    app.route('/account/create')
        .post(accountController.postAccount)

    app.route('/account/activate')
        .get(accountController.activateAccount);
};