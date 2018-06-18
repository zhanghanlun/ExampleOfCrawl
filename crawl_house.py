import requests
import smtplib
from email.mime.text import MIMEText
from lxml import html

mail_host = 'mail.ustc.edu.cn'
mail_user = 'sa517487@mail.ustc.edu.cn'
mail_pass = '13084564113a'
sender = 'sa517487@mail.ustc.edu.cn'
receiver = '1910747135@qq.com'

url1 = "https://www.douban.com/group/558784/discussion?start="
url2 = 'https://www.douban.com/group/383972/discussion?start='
send_content = '豆瓣租房每天信息更新\n'

def send_email(content):
    message = MIMEText(content,'plain','utf-8')
    message['Subject'] = '豆瓣租房筛选'
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

def crawl1(start_url):
    global send_content
    for x in range(0,15):
        r = requests.get(start_url + str(x*25)).content
        html1 = html.fromstring(r)
        node_list = html1.xpath("//td[@class='title']")
        for node in node_list:
            name = node.xpath('./a//@title')[0]
            house_url = node.xpath('./a//@href')[0]
            storage = 0
            if name.find('华夏西路')!= -1 or name.find('高青路')!=-1 or name.find("东明路")!=-1 \
                    or name.find('高科西路')!=-1 or name.find('临沂新村')!=-1 \
                    or name.find('北洋泾路')!=-1 or name.find('德平路')!=-1 \
                    or name.find('云山路')!=-1:
                storage = 1
                # print(name)
                # print(house_url)
                send_content = send_content + str(name)+'\n' + str(house_url)  + '\n'


def crawl2(start_url):
    global send_content
    for x in range(0,46):
        r = requests.get(start_url + str(x*25)).content
        html1 = html.fromstring(r)
        node_list = html1.xpath("//td[@class='title']")
        for node in node_list:
            name = node.xpath('./a//@title')[0]
            house_url = node.xpath('./a//@href')
            storage = 0
            if name.find('华夏西路')!= -1 or name.find('高青路')!=-1 or name.find("东明路")!=-1 \
                    or name.find('高科西路')!=-1 or name.find('临沂新村')!=-1 \
                    or name.find('北洋泾路')!=-1 or name.find('德平路')!=-1 \
                    or name.find('云山路')!=-1:
                storage = 1
                # print(name)
                # print(house_url)
                send_content = send_content + str(name) +'\n' + str(house_url) + '\n'

crawl1(url1)
crawl2(url2)
send_email(send_content)