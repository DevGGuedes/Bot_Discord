import datetime
date = datetime.datetime.now().time()
print(date)

from time import gmtime, strftime
strftime("%Y-%m-%d %H:%M:%S", gmtime())