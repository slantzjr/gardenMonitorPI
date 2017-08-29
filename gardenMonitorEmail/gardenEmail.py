import os
import smtplib

email_username = os.environ.get('GARDEN_MONITOR_EMAIL_ADDRESS') 
email_password = os.environ.get('GARDEN_MONITOR_PASSWORD')
recip_email = os.environ.get('GARDEN_MONITOR_ALERT_RECIP_EMAIL')

def init_email():
  print 'Setting up email'
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(email_username, email_password)
  print 'Email setup complete'
  return server

def send_alert(has_water):
  server = init_email()
  print 'sending alert'
  message = "We are happy now" if has_water else "We are thirsty"  
  payload = "\r\n".join([
    "From: Sean's lettuce",
    "To: recip_email",
    "Subject: Plant Alert!"
    "",
    message
  ])
  server.sendmail(email_username, 'recip_email', payload)
  print "Sent email notifying " + message
  server.quit()
  print "server connection closed"


