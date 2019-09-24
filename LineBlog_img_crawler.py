#!/usr/bin/python3
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve as uRetr
from bs4 import BeautifulSoup as soup
import os

raw_url = input("\nPlease Input the URL: (e.g. https://lineblog.me/uesaka_sumire/archives/2018-11.html)\nURL: ")

folder_dirname = input("\nPlease Input the Saving Path: (e.g. ~/[YOUR_DIRNAME])\nPath: ")

dirname_without_title = input("\nWould yout like to have directory names without artile title? (Y/N) ")

crawler_mode = input("\nPlease Choose Mode:\n 0 --- Current Page's Lateset Article ONLY\n 1 --- Current Page ONLY\n 2 --- ALL Related Pages\n 3 --- Current Page at Specific Position\nMode: ")


def open_url_to_soup(url):

	# opening up connection, grabbing the page
	uClient = uReq(url)
	page_html = uClient.read()
	uClient.close()

	# html parsing
	page_soup = soup(page_html, "html.parser")

	return page_soup


def find_target_urls(raw_url):
    
    page_soup = open_url_to_soup(raw_url)
    
    target_urls = []
    last_page_url = []
    last_page_num = None
    paging_last = page_soup.find("li", {"class":"paging-last"})
    if paging_last != None:
        for page in paging_last:
            last_page_url = page.get("href")
            last_page_num = page.string
#             print("Last URL:", last_page_url)
#             print("Last Page Num:", last_page_num)
    
    if last_page_num != None:
        base_url = last_page_url.split("?p=")[0] + "?p="
        for i in range(1, int(last_page_num) + 1):
            concat_url = base_url + str(i)
            target_urls.append(concat_url)
#             print("Concat URL:", concat_url)
    else:  
        paging_number = page_soup.find("ol", {"class":"paging-number"})
        target_pages = paging_number.find_all("a")
        target_page_num = 1
    
        for target_page in target_pages:
            target_urls.append(target_page.get("href"))
            if target_page_num < int(target_page.string):
                target_page_num = int(target_page.string)
        
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
		
		if dirname_without_title == 'N' or dirname_without_title == 'n':
			folder_basename = article_name.split("\n")[2] + " " + article_name.split("\n")[1]
		else:
			folder_basename = article_name.split("\n")[2]
		
		folder_basename = folder_basename.replace('/', '-')
		folder_basename = folder_basename.replace(':', '-')

		folder_path = os.path.join(os.path.expanduser(folder_dirname), folder_basename)
		mkdir(folder_path) 

		uRetr(imgURL, folder_path + "/%03d.jpg" %imgID)
		print(imgURL)
		imgID = imgID + 1


def mono_article_parse(article):
	
	title_article = article.find("header", {"class":"article-header"})
	article_name = title_article.text
	imgURLs_article = article.find("div", {"class":"article-body-inner"}).find_all("a", {"target":"_blank"})
	downloadImg(imgURLs_article, article_name)


def whole_parse_and_download(target_url):

	page_soup = open_url_to_soup(target_url)
	# grabs each element
	articles = page_soup.find_all("article", {"class":"article"})

	for article in articles:
		mono_article_parse(article)
		

def specific_parse_and_download(target_url, article_position = 0):

	page_soup = open_url_to_soup(target_url)
	# grabs each element
	articles = page_soup.find_all("article", {"class":"article"})
	
	mono_article_parse(articles[article_position])



if crawler_mode == '0':
	specific_parse_and_download(raw_url)

elif crawler_mode == '1':
	whole_parse_and_download(raw_url)

elif crawler_mode == '2':
	# whole_parse_and_download(raw_url)
	target_urls = find_target_urls(raw_url)
	for target_url in target_urls:
		whole_parse_and_download(target_url)

elif crawler_mode == '3':
	article_position = input("\nPlease Choose the Article Position (Start with 1): ")
	specific_parse_and_download(raw_url, int(article_position) - 1)

	

