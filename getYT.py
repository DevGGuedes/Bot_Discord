import urllib
from urllib.request import urlopen
from lxml import etree


youtube = etree.HTML(urlopen("https://www.youtube.com/watch?v=fVPY3wNURxw").read()) #enter your youtube url here
video_title = youtube.xpath("//*[@id='container']/h1/yt-formatted-string/text()") #get xpath using firepath firefox addon
print(video_title)