import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv


def get_html_test_message(test_num=1):
    email_message = f'`<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0f"><title>Mail Content</title></head><body><h1>Hello World test email {test_num}</h1></body></html>'
    return email_message


class Emailer:
    """
    A class to manage email sending using smtplib.
    """

    def __init__(self, host, port, from_email, password):
        self.host = host
        self.port = port
        self.from_email = from_email
        self.password = password

    def send_email(self, recipient_list, subject_text, message_text):
        """
        Sends an email to a list of recipients with a specified subject and message.

        Args:
            recipient_list (list): A list of email addresses for recipients.
            subject (str): The subject of the email.
            message (str): The body of the email (can be plain text or HTML).
        """

        try:
            smtp = smtplib.SMTP(self.host, self.port)
            smtp.starttls()
            smtp.login(self.from_email, self.password)
            message = MIMEMultipart("alternative")
            message["Subject"] = subject_text
            message["From"] = self.from_email
            message["To"] = ", ".join(recipient_list)

            html_part = MIMEText(message_text, "html")
            message.attach(html_part)


            smtp.sendmail(self.from_email, recipient_list, message.as_string())
            print("Email sent successfully!")

        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            smtp.quit()


if __name__ == "__main__":
    # Load credentials from environment variables (recommended)
    load_dotenv()
    from_email = os.getenv("from_email")
    password = os.getenv("password")

    HOST = "smtp-mail.outlook.com"
    PORT = 587

    emailer = Emailer(HOST , PORT , from_email, password)
    message = get_html_test_message()
    recipient_list = ["test1.test@testmail.com", "abc@gmail.com"]
    subject = "Test subject 4"


    emailer.send_email(recipient_list, subject, message)