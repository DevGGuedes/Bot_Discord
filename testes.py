import datetime
from time import gmtime, strftime
date = datetime.datetime.now().time()

data = datetime.datetime.now().date()
w = datetime.datetime.today().weekday()
print(w)

ontem = datetime.datetime(2021, 8, 23)
print(ontem.weekday())

ontem = datetime.datetime(2021, 8, 22)
print(ontem.weekday())

ontem = datetime.datetime(2021, 8, 15)
print(ontem.weekday())

#t = datetime.date(2021,8,28)
#print(t)

week = data.isocalendar()[1]
print(week)

if week % 2 == 0:
    print("Par")
else:
    print("Impar")

#print(data)

#print(date)


#t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#t = strftime("%Y-%m-%d", gmtime())
#print(t)

'''list1 = ['1','2','3']

list1.remove('1')

for i in list1:
    print(i)'''

'''lista_completa = [1,2,3,4]

lista_pares = [x for x in lista_completa if x % 2 == 0]
print(lista_pares)'''