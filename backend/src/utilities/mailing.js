const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    service: 'gmail',
    host: 'smtp.gmail.com',
    port: process.env.TRANSPONDER_PORT,
    secure: false,
    auth: {
        user: process.env.MAIL_USER,
        pass: process.env.MAIL_PASS
    }
});

const sendMail = accountRoute = async (mailOpts) =>{
    try{
        await transporter.sendMail(mailOpts);
        console.log('Email successfully sent!');
    }catch(error){
        console.log(error);
    }
}

const createMailOptions =  (details) =>{
    const mailOptions = {
        from: {
            name: details.name
        },
        to: details.sendTo,
        subject: details.subject,
        text: details.text,
        html: details.html
    }
    return mailOptions;
}

const mailActivation = (email, html_template) =>{
    const mailOpts = createMailOptions({
        name: 'password-manager.clarkmiller.ca',
        subject: "Account activation",
        sendTo: email,
        text: "Thank you for signing up, to activate your account, please click the link",
        html: html_template

    });
    sendMail(mailOpts);
}

const mailer = {
    sendMail: sendMail,
    createMailOptions: createMailOptions,
    mailActivation: mailActivation
}

module.exports = mailer;