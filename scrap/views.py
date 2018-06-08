from django.shortcuts import render, HttpResponse
import urllib.request as urllib2
from bs4 import BeautifulSoup
from multiprocessing import Pool,Process
import collections
from datetime import datetime
from functools import partial

# Create your views here.

def yoyo(question, username):
        urlprofile = 'http://www.spoj.com/status/' + question + ',' + username + '/'
        pagetoopen = urllib2.urlopen(urlprofile)
        soup = BeautifulSoup(pagetoopen, 'html.parser')
        name_box = soup.find('tbody')
        soup = BeautifulSoup(str(name_box), 'html.parser')
        for solved in soup.find_all('tr'):
            a = solved.find_all('td')
            if str(a[3].text.replace('\n', '')) == 'accepted':
                problem = a[2].a.get('title')
                time = str(a[1].text.replace('\n', ''))
                time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                li = [problem, time]
                return li


def homepage(request):
    if request.method == 'GET':
        return render(request, 'homepage/homepage.html')
    elif request.method == 'POST':
        tic = datetime.now()
        username = str(request.POST.get('username'))
        urlofprofile = 'http://www.spoj.com/users/' + username + '/'
        pagetoopen = urllib2.urlopen(urlofprofile)
        soup = BeautifulSoup(pagetoopen, 'html.parser')

        question_list = []

        for name in soup.find_all('td'):
            if name.text == '':
                break
            question_list.append(name.text)
        listss=[]
        #p = Process(target=yoyo, args=(question_list, username))
        #p.start()
        #p.join()
        p = Pool()
        p_x = partial(yoyo, username)
        listss = p.map(p_x, question_list)
        #k = p.map(yoyo, itertools.izip(question_list, itertools.repeat(username)))
        #listss.append(k)
        #p.join()
        #p.close()
        print(listss)
        listss = filter(None, listss)
        from operator import itemgetter
        listss = sorted(listss, key=itemgetter(1))
        print(listss)
        context = {
            "f": listss,
        "username":username,}
        toc = datetime.now()
        print(toc-tic)
        return render(request, 'homepage/homepage.html', context)



