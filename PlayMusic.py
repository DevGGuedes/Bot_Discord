import pafy
import vlc

url = "https://www.youtube.com/watch?v=bMt47wvK6u0"
video = pafy.new(url)
best = video.getbest()
playurl = best.url