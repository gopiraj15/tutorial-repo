from bs4 import BeautifulSoup
import requests as req

base_url = "http://www.talkinghands.co.in"
open_pg = req.get(base_url+"/sentences").text
soup = BeautifulSoup(open_pg,"lxml")

vid_title_url={}
for i in soup.find("div",{"class":"span8"}).find_all("div",{"class":"views-field views-field-title"}):
    vid_pg = BeautifulSoup(req.get(base_url+i.find("a").get("href")).text,"lxml")
    try:
        vid_title_url[i.text] = vid_pg.find("iframe").get("src").replace("//","")
    except:
        print('Some Error!')

from pytube import YouTube
for i in vid_title_url.keys():
    if vid_title_url[i]:
        yt = YouTube(vid_title_url[i])
        try:
            #yt.streams.filter('mp4').download(filename = 'data/' + i)
            yt.streams.first().download('data/', filename = i)
        except: 
            print("Some Error!")
