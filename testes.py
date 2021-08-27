'''import datetime
date = datetime.datetime.now().time()
print(date)

from time import gmtime, strftime
strftime("%Y-%m-%d %H:%M:%S", gmtime())

list1 = ['1','2','3']

list1.remove('1')

for i in list1:
    print(i)'''

lista_completa = [1,2,3,4]

lista_pares = [x for x in lista_completa if x % 2 == 0]
print(lista_pares)