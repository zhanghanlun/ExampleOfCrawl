
import requests
import smtplib
from email.mime.text import MIMEText
from lxml import html


mail_host = 'mail.ustc.edu.cn'
mail_user = 'sa517487@mail.ustc.edu.cn'
mail_pass = '13084564113a'
sender = 'sa517487@mail.ustc.edu.cn'
receiver = '1910747135@qq.com'
url = 'https://www.nowcoder.com/discuss?order=3&type=0&page='



def send_email(content):
    message = MIMEText(content,'plain','utf-8')
    message['Subject'] = '实习通知'
    message['From'] = sender
    message['To'] = receiver

    try:

        smtpObj = smtplib.SMTP_SSL(mail_host)
        print(smtpObj.login(mail_user,mail_pass))
        smtpObj.sendmail(sender,receiver,message.as_string())
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error ',e)
def detail_information(second_url):
    a = 1
    result = requests.get(second_url).content
    html1 = html.fromstring(result)
    HRcontent = html1.xpath("//div[@class='post-topic-des']//text()")
    datetime = html1.xpath("//span[@class='post-time']/text()")[0]
    return datetime,HRcontent


def crawl_information(start_url):
    send_content = '牛客网每天实习信息更新\n'
    for x in range(1,8):
        r = requests.get(start_url+str(x)).content
        html1 = html.fromstring(r)
        result = html1.xpath("//li[@class='clearfix']")
        for node in result:
            name = node.xpath('./div/div[1]/a[1]/text()')[0]
            tags = node.xpath('./div/div[1]/a/text()')
            storage1 = 0
            storage2 = 0
            for tag in tags:
                if tag == '实习':
                    storage1 = 1
                    break
            if(name.find('阿里')!=-1 or name.find('百度')!=-1 or
                name.find('美团')!=-1 or name.find('网易')!=-1 or name.find('点评')!=-1):
                storage2 = 1
            if name.find('产品')!=-1 or name.find('策划') != -1 or name.find('PM') !=-1:
                storage1 = 0
            if storage1 == 1 & storage2==1 :
                second_url = node.xpath('./div/div[1]/a[1]//@href')[0]
                second_url = 'https://www.nowcoder.com' + second_url
                datetime, HRcontent = detail_information(second_url)
                if datetime.find('今天')!=-1 :
                    send_content = send_content + name + datetime + second_url+'\n'
    return send_content

content = crawl_information(url)
print(content)
send_email(content)
