import csv
import os
import json
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from . import buildimages

# Create your views here.
app_name = 'myApp'


def home(request):
    return render(request, 'myApp/index.html')


def login(request):
    if 'user' in request.session:
        return redirect('http://127.0.0.1:8000/%2Fadmins')
    if request.POST:
        email = request.POST.get('emailid')
        passd = request.POST.get('pass')
        filehandle = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/userlist.txt', 'r')
        for line in filehandle:
            words = line.strip().split('|')
            if words[2] == email and words[3] == passd:
                name = words[0] + " " + words[1]
                filename = words[0].lower() + words[1].lower() + ".txt"
                filepath = "C:/Users/akashweb/PycharmProjects/stockpadFinal/users/" + filename
                request.session['user'] = name
                request.session['filename'] = filename
                request.session['filepath'] = filepath
                return render(request, 'myApp/loginokay.html')
        return render(request, 'myApp/loginx.html')
    return render(request, 'myApp/login.html')


def register(request):
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    passd = request.POST.get('pass')
    rpassd = request.POST.get('rpass')
    if request.POST:
        if passd != rpassd:
            return render(request, 'myApp/passmismatch.html')
        else:
            fileinput = fname + "|" + lname + "|" + email + "|" + passd + "\n"
            filehandle = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/userlist.txt', 'a')
            filehandle.write(fileinput)
            filehandle.close()
            return render(request, 'myApp/passmatch.html')
    return render(request, 'myApp/register.html')


def forgot_password(request):
    if request.POST:
        email = request.POST.get('emailid')
        filehandle = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/userlist.txt', 'r')
        for line in filehandle:
            words = line.split('|')
            if words[2] == email:
                return render(request, 'myApp/mailsent.html')
        filehandle.close()
        return render(request, 'myApp/mailerror.html')
    return render(request, 'myApp/forgot-password.html')


def admin(request):
    try:
        filehandle = open(request.session['filepath'], 'r')
    except:
        filehandle = open(request.session['filepath'], 'w')

    dashsummary = [0, 0, 0, 0]

    path = request.session['filepath']
    if os.path.getsize(path) == 0:
        for i in range(4):
            filehandle.write('0\n')
    else:
        i = 0
        for line in filehandle:
            dashsummary[i] = float(line.strip())
            i = i + 1
        filehandle.close()
        dashsummary[2] = round((dashsummary[1] - dashsummary[0]), 2)
        if dashsummary[0] == 0:
            dashsummary[3] = 0
        else:
            dashsummary[3] = round(dashsummary[2] / (dashsummary[0]) * 100, 2)
        filehandle = open(request.session['filepath'], 'w')
        for i in range(4):
            filehandle.write(str(dashsummary[i]) + "\n")
        filehandle.close()
    curprice = []
    paidprice = []
    nofoshares = []
    companynames = []
    clisthandle = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/company.txt', 'r')
    for c in clisthandle:
        filename = 'C:/Users/akashweb/PycharmProjects/stockpadFinal/companydata/' + c.strip() + '.csv'
        f = open(filename, 'r')
        read = csv.reader(f)
        curprice.append(list(read)[-1][5])
        companynames.append(c.strip())
        f.close()
    clisthandle.close()
    print(curprice)
    sharefilename = 'C:/Users/akashweb/PycharmProjects/stockpadFinal/users/' + ''.join(
        request.session.get('user').split()).lower() + 'shares.txt'
    if os.path.exists(sharefilename):
        f = open(sharefilename, 'r')
        for line in f:
            words = line.strip().split('|')
            nofoshares.append(int(words[1]))
            paidprice.append(words[2])
    else:
        f = open(sharefilename, 'w')
        clisthandle = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/company.txt', 'r')
        for line in clisthandle:
            l = line.strip() + "|0|0"
            f.write(l + "\n")
            nofoshares.append(0)
            paidprice.append(0)
    pl = []
    tprice = 0
    profitloss = 0
    for i in range(len(companynames)):
        pl.append(float(nofoshares[i]) * (float(curprice[i]) - float(paidprice[i])))
        tprice = tprice + float(paidprice[i])
        print(pl[i])
        profitloss = profitloss + float(pl[i])
    filehandle = open(request.session['filepath'], 'w')
    filehandle.write(str(round(tprice, 2)) + "\n")
    filehandle.write(str(round(profitloss + tprice, 2)) + "\n")
    json_datas = json.dumps(pl)
    jshares = json.dumps(nofoshares)
    context = {'dashsummary': dashsummary,
               'json_datas': json_datas,
               'noofshares': jshares,
               }
    return render(request, 'myApp/admin.html', context)


def logout(request):
    del request.session['user']
    return render(request, 'myApp/index.html')


def companies(request):
    flag = False
    if request.POST:
        print(request.POST.get('searchkey'))
        flag = True
    curprice = []
    paidprice = []
    nofoshares = []
    companynames = []
    clisthandle = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/company.txt', 'r')
    for c in clisthandle:
        filename = 'C:/Users/akashweb/PycharmProjects/stockpadFinal/companydata/' + c.strip() + '.csv'
        f = open(filename, 'r')
        read = csv.reader(f)
        curprice.append(list(read)[-1][5])
        companynames.append(c.strip())
        f.close()
    clisthandle.close()
    sharefilename = 'C:/Users/akashweb/PycharmProjects/stockpadFinal/users/' + ''.join(
        request.session.get('user').split()).lower() + 'shares.txt'
    if os.path.exists(sharefilename):
        f = open(sharefilename, 'r')
        for line in f:
            words = line.strip().split('|')
            nofoshares.append(words[1])
            paidprice.append(words[2])
    else:
        f = open(sharefilename, 'w')
        clisthandle = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/company.txt', 'r')
        for line in clisthandle:
            l = line.strip() + "|0|0"
            f.write(l + "\n")
            nofoshares.append(0)
            paidprice.append(0)
    pl = []
    tprice = 0
    profitloss = 0
    for i in range(len(companynames)):
        pl.append(round((float(nofoshares[i]) * (float(curprice[i]) - float(paidprice[i]))), 2))
        tprice = tprice + float(paidprice[i])
        profitloss = profitloss + float(pl[i])
    filehandle = open(request.session['filepath'], 'w')
    filehandle.write(str(round(tprice, 2)) + "\n")
    filehandle.write(str(round(profitloss + tprice, 2)) + "\n")
    filehandle.close()
    if flag:
        nofoshares1 = []
        paidprice1 = []
        curprice1 = []
        companynames1 = []
        for i in range(len(companynames)):
            if request.POST.get('searchkey').strip().lower() in companynames[i].strip().lower():
                companynames1.append(companynames[i])
                nofoshares1.append(nofoshares[i])
                paidprice1.append(paidprice[i])
                curprice1.append(curprice[i])
        companynames = companynames1
        nofoshares = nofoshares1
        paidprice = paidprice1
        curprice = curprice1
    context = {'noofshares': nofoshares,
               'paidprice': paidprice,
               'curprice': curprice,
               'companynames': companynames,
               'pl': pl,
               'range': range(len(companynames)),
               'length': len(companynames),
               }
    return render(request, 'myApp/companies.html', context)


def news(request):
    URL = 'https://economictimes.indiatimes.com/markets'
    filehandle = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/news.txt', 'w')
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    p = []
    q = []
    for link in soup.find_all('span', attrs={'class': "news_heading"}):
        p.append(link.text + "...")
        q.append("https://economictimes.indiatimes.com" + link.find('a').get('href'))
    context = {'headlines': p, 'links': q, 'range': range(len(p))}
    for i in range(len(p)):
        filehandle.write(p[i] + ":" + q[i] + "\n")
    filehandle.close()
    return render(request, 'myApp/news.html', context)


def companyshow(request, name):
    buildimages.graph(name)
    buildimages.candle(name)
    if name == 'HEROMOTOCO':
        url = 'https://www.moneycontrol.com/india/stockpricequote/auto-23-wheelers/heromotocorp/HHM'
    elif name == 'HINDUNILVR':
        url = 'https://www.moneycontrol.com/india/stockpricequote/personal-care/hindustanunilever/HU'
    elif name == 'IRCTC':
        url = 'https://www.moneycontrol.com/india/stockpricequote/misc-commercial-services/irctc-indianrailwaycateringtourismcorp/IRC'
    elif name == 'MARUTI':
        url = 'https://www.moneycontrol.com/india/stockpricequote/auto-carsjeeps/marutisuzukiindia/MS24'
    elif name == 'RBLBANK':
        url = 'https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/rblbank/RB03'
    elif name == 'SPICEJET':
        url = 'https://www.moneycontrol.com/india/stockpricequote/transportlogistics/spicejet/SJ01'
    elif name == 'SUNPHARMA':
        url = 'https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/sunpharmaceuticalindustries/SPI'
    print(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    feed = soup.find_all('ul', attrs={'class': 'clearfix value_list'})
    f = feed[0].text
    f = f.strip()
    fl = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/companydata/' + name + "metrics.txt", 'w')
    fl.write(f)
    fl.close()
    fhand = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/companydata/' + name + "metrics.txt", 'r')
    marktcap = '0'
    pe = '0'
    bkval = '0'
    dvnd = '0'
    day3 = '0'
    day5 = '0'
    day8 = '0'
    lines = []
    for line in fhand:
        if line != '\n':
            lines.append(line.strip())
    print(lines)
    fhand.close()
    marktcap = lines[1]
    pe = lines[3]
    bkval = lines[5]
    dvnd = lines[7]
    mrktlot = lines[9]
    industrype = lines[11]
    epsttm = lines[13]
    pc = lines[15]
    prcbk = lines[17]
    dvndyld = lines[19]
    facevalue = lines[21]
    day3 = lines[26]
    day5 = lines[28]
    day8 = lines[30]
    graphpath = 'C:/Users/akashweb/PycharmProjects/stockpadFinal/myApp/static/myApp/'+name+"graph.png"
    context = {'name': name,
               'marktcap': marktcap,
               'pe': pe,
               'bkval': bkval,
               'dvnd': dvnd,
               'mrktlot': mrktlot,
               'industrype': industrype,
               'epsttm': epsttm,
               'pc': pc,
               'prcbk': prcbk,
               'dvndyld': dvndyld,
               'facevalue': facevalue,
               'day3': day3,
               'day5': day5,
               'day8': day8,
               'graphpath': graphpath}
    return render(request, 'myApp/companyshow.html', context)


def editrecord(request, name):
    request.session['cname'] = name
    sharefilename = 'C:/Users/akashweb/PycharmProjects/stockpadFinal/users/' + ''.join(request.session.get('user').split()).lower() + 'shares.txt'
    filehandle = open(sharefilename, 'r')
    for line in filehandle:
        words = line.split('|')
        if words[0] == name:
            quantity = int(words[1])
            amount = float(words[2])
    filehandle.close()
    context = {'name': name, 'quantity': quantity, 'amount': amount}
    return render(request, 'myApp/editrecord.html', context)


def editrecordx(request):
    name = request.session.get('cname')
    sharefilename = 'C:/Users/akashweb/PycharmProjects/stockpadFinal/users/' + ''.join(
        request.session.get('user').split()).lower() + 'shares.txt'
    filehandle = open(sharefilename, 'r')
    """
    plfilename = 'C:/Users/akashweb/PycharmProjects/stockpadFinal/users/' + ''.join(
        request.session.get('user').split()).lower() + '.txt'
    plhandle = open(plfilename,'r+')
    """
    newfile = open('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/' + ''.join(
        request.session.get('user').split()).lower() + 'shares1.txt','w')
    print(request.POST.get('quantity'))
    print(request.POST.get('amount'))
    for line in filehandle:
        words = line.split('|')
        print(line)
        if words[0] == name:
            if request.POST.get('trans') == 'buy':
                newno = int(words[1]) + int(request.POST.get('quantity'))
                newamount = (float(words[1])*float(words[2]) +(float(request.POST.get('amount'))*float(request.POST.get('quantity'))))/(float(request.POST.get('quantity'))+float(words[1]))
                newfile.write(words[0]+"|"+(str(newno))+"|"+(str(newamount))+"\n")
            else:
                newno = int(words[1]) - int(request.POST.get('quantity'))
                newamount = (float(words[1]) * float(words[2]) - (
                            float(request.POST.get('amount')) * float(request.POST.get('quantity')))) / (
                                        float(request.POST.get('quantity')) - float(words[1]))
                newfile.write(words[0] + "|" + (str(newno)) + "|" + (str(newamount)) + "\n")
            print(newno, newamount)
        else:
            newfile.write(line)
    filehandle.close()
    newfile.close()
    os.remove('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/' + ''.join(
        request.session.get('user').split()).lower() + 'shares.txt')
    os.rename(('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/' + ''.join(
        request.session.get('user').split()).lower() + 'shares1.txt'),('C:/Users/akashweb/PycharmProjects/stockpadFinal/users/' + ''.join(
        request.session.get('user').split()).lower() + 'shares.txt'))
    context ={'name': name, 'quantity': newno, 'amount': newamount}
    return render(request, 'myApp/editrecordx.html')
