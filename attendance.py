import requests
import math
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(bot,update):
    print("hi")
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    bot.send_message(update.message.chat_id,"hi")




def attendance_fetcher(bot,update,args):
    print("inside fetcher!")
    username=str(args[0].split(":")[0])
    password=str(args[0].split(":")[1])
    # username=args[0].split(":")[0]
    # password=args[0]
    print(username,password)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'http://mca.rit.ac.in/ritsoftv3/login.php',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }



    response = requests.post('http://mca.rit.ac.in/ritsoftv3/login.php', headers=headers)
    cookie=(response.headers['Set-Cookie'].split()[0])


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'http://mca.rit.ac.in/ritsoftv3/login.php',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = 'username='+username+'&password='+password+'&login=Login'
    cookies = {
        'PHPSESSID': cookie.split('=')[1].strip(';')
    }
    print(cookies)

    response = requests.post('http://mca.rit.ac.in/ritsoftv3/login.php', headers=headers, cookies=cookies, data=data, verify=False)


    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Referer': 'http://mca.rit.ac.in/ritsoftv3/login.php',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'multipart/form-data; boundary=---------------------------17760220484614',
    }
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-GB,en;q=0.5", "Referer": "http://mca.rit.ac.in/ritsoftv3/student/login.php", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Content-Type": "multipart/form-data; boundary=---------------------------17760220484614"}
    cookies = {
        'PHPSESSID': cookie.split('=')[1].strip(';')
    }
    data="-----------------------------17760220484614\r\nContent-Disposition: form-data; name=\"date1\"\r\n\r\n2019-01-28\r\n-----------------------------17760220484614\r\nContent-Disposition: form-data; name=\"date2\"\r\n\r\n2019-04-04\r\n-----------------------------17760220484614\r\nContent-Disposition: form-data; name=\"btnshow-new\"\r\n\r\n\r\n-----------------------------17760220484614--\r\n"
    files = {'file': ''}
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.post('http://mca.rit.ac.in/ritsoftv3/student/parent_monthly.php', headers=headers2, cookies=cookies,data=data )
    f=open("res.html","w")
    f.write(response.text)
    f.close()
    soup=BeautifulSoup(response.text,"html.parser")
    i=0
    sname=[]
    total=[]
    attended=[]
    perc=[]
    count=1
    for strong_tag in soup.find_all('td')[3:]:
        #print(strong_tag.text)
        i+=1
        if(count==1):
            #print(strong_tag.text)
            sname.append(strong_tag.text)
            total.append(strong_tag.next.next.next.next.next.text)
            attended.append(strong_tag.next.next.next.next.next.next.next.next.text)
        if(count==4):
            count=0
        if(i==36):
            break
        if(strong_tag.text.find('%')!=-1):
            #print("%%%%%%",strong_tag)
            perc.append(strong_tag.text)
        count+=1
    print(sname)
    print(perc)
    classcut=[]
    for i in range(0,9):
        print(attended[i],"   ",total[i],"   ",float(attended[i])*(4/3))
        classcut+=[math.floor(float(attended[i])*(4/3))-int(attended[i])]
    print(classcut)

















def main():
    print("started!")

    f1=open("token.txt","r")
    token=f1.read().strip()
    updater = Updater(token)
    f1.close()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("login", attendance_fetcher,pass_args=True))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
	main()
