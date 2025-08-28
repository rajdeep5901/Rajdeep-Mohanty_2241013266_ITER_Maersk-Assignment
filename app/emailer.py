import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
from .config import C
def send_mail(to_list, ctx):
    if not to_list:
        return False
    m=MIMEMultipart("alternative")
    m["Subject"]=f"[NDAC] {ctx.get('sev')} {ctx.get('typ')} on {ctx.get('elem')}"
    m["From"]=C.FROM_ADDR
    m["To"]=",".join(to_list)
    txt=render_template("email_alert.txt",**ctx)
    html=render_template("email_alert.html",**ctx)
    m.attach(MIMEText(txt,"plain"))
    m.attach(MIMEText(html,"html"))
    c=ssl.create_default_context()
    with smtplib.SMTP(C.SMTP_HOST, C.SMTP_PORT) as s:
        s.starttls(context=c)
        s.login(C.SMTP_USER,C.SMTP_PASS)
        s.sendmail(C.FROM_ADDR,to_list,m.as_string())
    return True