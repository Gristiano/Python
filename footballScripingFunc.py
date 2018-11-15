from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re


def download_半全场(url):
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='html.parser')
    my_table = soup.find_all('table', {'class': "table6"})
    table6 = my_table[0].find_all('td')
    title1 = soup.find_all('div', {'class': 'd1'})[0].text
    title2 = soup.find_all('div', {'class': 'd3'})[0].text
    time1 = soup.find_all('p', {'class': 'p1'})[0].text
    time2 = soup.find_all('p', {'class': 'p2'})[0].text

    list1 = []
    list2 = []

    for i in range(2, 11):
        list1.append(table6[i].get_text())

        a = table6[-11 + i].get_text()
        if '↓' in a:
            b = a.strip('↓')
        elif '↑' in a:
            b = a.strip('↑')
        else:
            b = a
        list2.append(float(b))

    dic1 = dict(zip(list1, list2))

    return_rate = 0
    for i in dic1:
        gai = 1 / dic1[i]
        return_rate = return_rate + gai

    dic = {'数据': dic1, '返还率': return_rate, '对战': title1 + "vs" + title2, '时间': time1 + time2}

    return dic


# 半全场dic = download_半全场('http://www.lottery.gov.cn/football/match_hhad.jspx?mid=113572')
# print(半全场dic)


def download_主页开奖半全场(url):
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find_all('table', {'cellpadding': '1'})
    game_links = table[0].find_all('a')

    game_links = game_links[:-4]

    url_list = []

    for link in game_links:
        url_list.append('http://www.lottery.gov.cn' + link['href'])

    data = []
    for urls in url_list:
        data.append(download_半全场(urls))

    return data



def download_主页受注半全场(url):
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find_all('table', {'cellpadding': '1'})
    game_links = table[0].find_all('a')

    game_links = game_links[:]

    url_list = []

    for link in game_links:
        url_list.append('http://www.lottery.gov.cn' + link['href'])

    data = []
    for urls in url_list:
        data.append(download_半全场(urls))

    return data



def print_data_主页半全场(list):
    print(str(len(list))+'场比赛')
    for dic in list:
        print(dic['对战'])
        print(dic['时间'])
        for i in dic['数据']:
            print(i, dic['数据'][i])


def down_load彩客网(url):
    list = []
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find_all('tr', {'id': re.compile('spfTr*')})
    list1 = ['主胜', '平局', '客胜']

    for tr in table:
        list2 = []
        onegame = tr.find_all('span')
        for span in onegame:
            list2.append(span.text)
        dic_inside = dict(zip(list1, list2))
        list.append(dic_inside)

    table_hometeam = soup.find_all('a', {'id': re.compile('HomeTeam*')})
    table_guestteam = soup.find_all('a', {'id': re.compile('GuestTeam*')})
    table_ht = []
    table_gt = []
    for a in table_hometeam:
        table_ht.append(a.text)
    for a in table_guestteam:
        table_gt.append(a.text)

    list_team = []
    for i in range(len(table_ht)):
        list_team.append(table_ht[i] + 'vs' + table_gt[i])

    dic = dict(zip(list_team, list))

    return dic


def print_data_彩客网(dic):
    print(str(len(dic)) + '场比赛')
    for data in dic:
        print(data)
        for i in dic[data]:
            print(i, dic[data][i])
