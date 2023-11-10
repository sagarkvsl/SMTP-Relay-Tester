from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuring Flask app for Flask-Mail
app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        smtp_host = request.form['smtp_host']
        smtp_port = int(request.form['smtp_port'])
        smtp_username = request.form['smtp_username']
        smtp_password = request.form['smtp_password']
        from_email = request.form['from_email']
        to_email = request.form['to_email']

        try:
            # Configuring Flask app with form input
            app.config['MAIL_SERVER'] = smtp_host
            app.config['MAIL_PORT'] = smtp_port
            app.config['MAIL_USE_TLS'] = True
            app.config['MAIL_USERNAME'] = smtp_username
            app.config['MAIL_PASSWORD'] = smtp_password
            app.config['MAIL_DEFAULT_SENDER'] = from_email

            # Initializing the Mail object (moved outside of the try block)
            mail.init_app(app)

            # Sending confirmation email with customized HTML body and embedded image
            msg = Message('SMTP Relay Tester - Confirmation',
                          recipients=[to_email],
                          html="<h1>Your SMTP credentials are working fine!</h1>"
                               "<img src='https://c.tenor.com/12Fv9x_3mCIAAAAC/tenor.gif'>")

            mail.send(msg)

            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Error sending email: {str(e)}', 'error')

    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
