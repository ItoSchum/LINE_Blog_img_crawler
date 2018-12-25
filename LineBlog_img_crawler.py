#!/usr/bin/python3
from urllib import request 
from bs4 import BeautifulSoup as soup
import os
import random


raw_url = input("\nPlease input the url: (e.g. https://lineblog.me/uesaka_sumire/archives/2018-11.html)\n")
# e.g.
# raw_url = "https://lineblog.me/uesaka_sumire/archives/2018-11.html?p=1"
folder_dirname = input("\nPlease input the path: (e.g. ~/[YOUR_DIRNAME])\n")

def requests_headers():
    head_connection = ['Keep-Alive','close']
    head_accept = ['text/html,application/xhtml+xml,*/*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5','en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    header = {
        'Connection':head_connection[random.randrange(0,len(head_connection))],
        'Accept':head_accept[0],
        'Accept-Language':head_accept_language[random.randrange(0,len(head_accept_language))],
        'User-Agent':head_user_agent[random.randrange(0,len(head_user_agent))],
    }
    print('headers.py connection Success!')
    return header

def find_target_urls(target_url):
	req = request.Request(url = target_url, headers = requests_headers())
	uClient = request.urlopen(req)
	page_html = uClient.read()
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	paging_number = page_soup.find("ol", {"class":"paging-number"})
	target_urls = paging_number.find_all("a")

	return target_urls


def mkdir(path):
	
	folder = os.path.exists(path)
	if not folder:                   
		os.makedirs(path)            
		print("---  Made New Dir  ---")
	else:
		print("---  Alredy Exsits  ---")
		

def downloadImg(imgURLs_article, article_name):
	
	imgID = 0
	for imgURL_article in imgURLs_article:
		imgURL = imgURL_article.get('href')
		
		folder_basename = article_name.split("\n")[2] + " " + article_name.split("\n")[1]
		folder_basename = folder_basename.replace('/', '-')
		folder_path = os.path.join(os.path.expanduser(folder_dirname), folder_basename)
		mkdir(folder_path) 

		request.urlretrieve(imgURL, folder_path + "/%03d.jpg" %imgID)

		print(imgURL)
		imgID = imgID + 1


def parse_and_download(target_url):

	# opening up connection, grabbing the page
	req = request.Request(url = target_url, headers = requests_headers())
	uClient = request.urlopen(req)
	page_html = uClient.read()
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	# grabs each element
	articles = page_soup.findAll("article", {"class":"article"})

	for article in articles:
		title_article = article.find("header", {"class":"article-header"})
		article_name = title_article.text
		imgURLs_article = article.find("div", {"class":"article-body-inner"}).find_all("a", {"target":"_blank"})
		downloadImg(imgURLs_article, article_name)

target_urls = find_target_urls(raw_url)

parse_and_download(raw_url)
for target_url in target_urls:
	parse_and_download(target_url.get('href'))
	

