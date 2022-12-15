'''
rivers
https://github.com/HuTa0kj
'''


import requests
from requests import get
import os
import argparse
import json
from bs4 import BeautifulSoup
# 模块主要用于解析url中的参数，对url按照一定格式进行 拆分或拼接
from urllib.parse import urlparse
import getpass

# os.system("clear")
print("\033[93m-------------------------------------------------------------------------------------")
print("\033[92m _____       _         _                       _        __   __                ")
print("\033[92m/  ___|     | |       | | ___                 (_)       \ \ / /                 ")
print("\033[92m\ `--. _   _| |__   __| |/   \ _ __ ___   __ _ _ _ __    \`/ /                 ")
print("\033[92m `--. \ | | | '_ \ / _` |  /| | '_ ` _ \ / _` | | '_ \    /`/\                 ")
print("\033[92m/\__/ / |_| | |_) | (_| \ |_/ / | | | | | (_| | | | | |  / /\ \                ")
print("\033[92m\____/ \__,_|_.__/ \__,_|\___/|_| |_| |_|\__,_|_|_| |_| /_/  \_\      V1.0     ")
print("\033[93m-------------------------------------------------------------------------------------")
print("")


def parse_args():
    parse = argparse.ArgumentParser(description='Calculate cylinder volume')  # 创建参数对象
    parse.add_argument('-d', '--domain', required=True, help='domain')  # 往参数对象添加参数
    parse.add_argument('-z', '--zoomeye', action='store_const', const=str, help='Zoomeye')  # 使用Zoomeye进行查询
    parse.add_argument('-b', '--brute', action='store_const', help='Brute cracked dictionary', const=str)
    parse.add_argument('-r', '--reptile', action='store_const', help='Get by bing search engine', const=str)  # 浏览器site
    parse.add_argument('-p', '--pages', default=10, help='page')  # 页数范围
    parse.add_argument('-l', '--list', default='./dic/subname_base.txt', help='list')  # 默认字典
    parse.add_argument('-e', '--engine', default='https://www.baidu.com/', help='Search engine')  # 默认搜索引擎
    args = parse.parse_args()  # 解析参数对象获得解析对象
    return args


def zm_subdomain(domain, pages, headers):
    url = 'https://api.zoomeye.org/domain/search?q=' + str(domain) + '&type=1&page=' + str(pages)    
    res = requests.get(url=url, headers=headers).json() 
    return res


def zm(domain):
    #
    user = input("\033[95m    Enter Zoomeye username >>> ")
    pswd = getpass.getpass("\033[95m    Enter Zoomeye password >>> ")

    print("\033[95m    Querying......  ")
    print("\033[94m-------------------------------------------------------------------------------------")

    login_url = "https://api.zoomeye.org/user/login"
    login_info = \
        {"username": user,
         "password": pswd
         }
    encoded_data = json.dumps(login_info)
    resp = requests.post(login_url, encoded_data)
    access_token = resp.json()['access_token']

    headers = {'Authorization': 'JWT ' + access_token}

    for page in range(20):
        res = zm_subdomain(domain, page + 1, headers)

        if len(res['list']) == 0:
            break
        for each in res['list']:
            sub = each['name']
            ip = each['ip']
            print(sub)
            output(sub)
    print("\033[93m-------------------------------------------------------------------------------------")


def brute(domain, dic, engine):  # 使用字典破解
    print("")
    try:

        get(engine)
        internet = True
        print("\t\t\t\t Internet Connected !!")
        print("\n")
        print("\033[93m-------------------------------------------------------------------------------------")
    except:
        print("\tYou are not Connected to Internet. Please Turn on your Mobile Data")
        print("\n")
        exit()

    # file = open('wordlist.txt','r')
    file = open(dic, 'r')
    content = file.read()

    subdomains = content.splitlines()

    for subdomain in subdomains:
        url1 = f"http://{subdomain}.{domain}"
        url2 = f"https://{subdomain}.{domain}"
        try:
            requests.get(url1)
            print(f"\033[94m Discovered URL: {url1}")
            output(url1)
            requests.get(url2)
            print(f"\033[94m Discovered URL: {url2}")
            output(url2)
        except requests.ConnectionError:
            pass
    print("\n")
    print("\n")
    print("\033[93m-------------------------------------------------------------------------------------")


def bing_search(site, pages): # 搜索引擎
    Subdomain = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (x11; Linux x86_64;rv:68.0)Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': "https://cn.bing.com",
        'Cookie': "MUID=3B46E5B***********78X&T=6"
    }
    for i in range(1, int(pages) + 1):
        url = "https://cn.bing.com/search?q=site%3a" + site + "&go=Search&qs=ds&first=" + str(
            (int(i) - 1) * 10) + "&FORM=PERE"
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        job_bt = soup.findAll('h2')  # 返回一个包含HTML文档标题标签h2的列表
        for i in job_bt:
            link = i.a.get('href')
            domain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)  # 储存子域名
            if domain in Subdomain:
                pass
            else:
                Subdomain.append(domain)
                print(domain)
                output(domain)


def output(data,):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(data+'\n')


if __name__ == '__main__':
    args = parse_args()
    if args.zoomeye != None:
        zm(args.domain)
    elif args.brute != None:
        brute(args.domain, args.list, args.engine)
    elif args.reptile != None:
        Subdomain = bing_search(args.domain, args.pages)
