from bs4 import BeautifulSoup
import requests as req
base_url="http://www.talkinghands.co.in"
open_pg=req.get(base_url+"/sentences").text
soup=BeautifulSoup(open_pg,"lxml")
vid_title_url={}
for i in soup.find("div",{"class":"span8"}).find_all("div",{"class":"views-field views-field-title"}):
	
	vid_pg=BeautifulSoup(req.get(base_url+i.find("a").get("href")).text,"lxml")
	vid_title_url[i.text]=vid_pg.find("iframe").get("src").replace("//","")

from pytube import YouTube
for i in vid_title_url.keys():
	yt = YouTube(vid_title_url[i])
	yt.streams.first().download(filename=i)
