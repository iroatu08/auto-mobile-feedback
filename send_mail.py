import smtplib 
from email.mime.text import MIMEText


def send_mail(customer, email, dealer, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'd5a8d037eca150'
    password = 'af8f8bdaeece6c'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Customer: {email}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'iroatu7@gmail.com'
    receiver_email = email
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Mercedes-Benz Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())