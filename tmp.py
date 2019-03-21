rfile = open('reestr.json', 'r')
print(rfile.read().encode('cp1251').decode('utf8'))
