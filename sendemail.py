from os import sendfile, stat
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
 
my_sender='1057072764@qq.com'    # 发件人邮箱账号
my_pass = 'einugfkdksdxbeej'              # 发件人邮箱密码

def mail(username, email, status):
    if(email):
        ret=True
        try:
            msg=MIMEText('此邮件由GZHU_Autoclock自动发出','plain','utf-8')
            msg['From']=formataddr(["GZHU_autoclock",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["dear", email])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            if(status):
                msg['Subject']="打卡成功,尊敬的{}".format(username)
                # 邮件的主题，也可以说是标题
            else:
                msg['Subject']="打卡失败,尊敬的{}".format(username)
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender,[email,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret=False
        return ret
