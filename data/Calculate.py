F1 = dict()
F2 = dict()

def Calculate():
    import json
    import requests
    from urllib.parse import quote
    from os import listdir
    from os.path import isfile, join

    global F1, F2
    
    files = [f.split('.')[0] for f in listdir('reestr/') if isfile(join('reestr/', f))]
    routes_list = open('routes_list.txt', 'r')
    routes = routes_list.readlines()

    
    percent = dict()
    ref = 'https://github.com/sergets/sergets.github.io/tree/master/mgtmap-gp/actuals'
    r = requests.get(ref)
    source = r.text.split('\n')
    data = []
    for i in source:
        if 'href="/sergets/sergets.github.io/blob/master/mgtmap-gp/actuals' in i:
            href = 'https://raw.githubusercontent.com' + i.split('href="')[1].split('"')[0]
            href = href.replace('/blob', '')
            data.append(href)
    for i in data:
        rr = requests.get(i)
        s = rr.text
        JSON = json.loads(s)
        T = JSON['trolleyNumbers']['fractions']
        Sum = 0
        for i in T:
            if T[i] is None:
                T[i] = 0
            percent[i] = T[i]
            Sum += T[i]
        Sum /= len(T)
        break


    freqs = 'https://raw.githubusercontent.com/sergets/sergets.github.io/master/mgtmap-gp/data/freqs.json'
    r = requests.get(freqs)
    source = r.text
    JSON = json.loads(source)
    for route in JSON:
        F2[route] = 0
        for day in JSON[route]:
            bay = bin(int(day))[2:]
            while len(bay) < 7:
                bay += '0'
            c = bay.count('1')
            for hour in JSON[route][day]:
                F2[route] += JSON[route][day][hour] * 365 / 7 * c

    
    for route in routes:
        route = route.strip()
        if route not in files:
            continue
        t_file = open('timetable/' + route + '.txt', 'r')
        r_file = open('reestr/' + route + '.txt', 'r')
        fout = open('calcdata/' + route + '.txt', 'w')
        arr = r_file.readline().split(';')
        dist = float(arr[0].split()[0].split('(')[0].replace(',', '.'))
        num = int(arr[1])
        tmp = t_file.readlines()
        time = dict()
        for i in range(0, len(tmp), 2):
            time[tmp[i].strip()] = list(map(int, tmp[i + 1].split()))
        cnt = 0
        for i in time:
            if 'BA' not in i:
                continue
            cnt += 365 / 7 * i.count('1') * len(time[i])
        F1[route] = cnt
        print(dist, file=fout) # Расстояние туда и обратно
        if route in F2:
            print(F2[route] / max(num, 1), file=fout)
        else:
            print(F1[route] / max(num, 1), file=fout)
        #print(round(cnt / max(num, 1)), file=fout) # Сколько в среднем за год
        # проходит один автобус по маршруту
        
        print(num, file=fout) # количество автобусов на маршруте
        if route in percent:
            print(percent[route] * 100, file=fout)
        elif 'НМ-' in route or 'З-' in route:
            print(0, file=fout)
        else:
            print(Sum * 100, file=fout)
        #print(100, file=fout) # процент под контактной сетью
        print(30, file=fout) # расход топлива на 100 км
        fout.close()


def GetDataFromMGTMap():
    import json
    import requests
    from urllib.parse import quote
    
    ref = 'https://github.com/sergets/sergets.github.io/tree/master/mgtmap-gp/actuals'
    r = requests.get(ref)
    source = r.text.split('\n')
    data = []
    #test = open('mgtmap.txt', 'w')
    for i in source:
        if 'href="/sergets/sergets.github.io/blob/master/mgtmap-gp/actuals' in i:
            #print(i)
            href = 'https://raw.githubusercontent.com' + i.split('href="')[1].split('"')[0]
            href = href.replace('/blob', '')
            data.append(href)
    print(*data, sep='\n')
    for i in data:
        rr = requests.get(i)
        s = rr.text
        JSON = json.loads(s)
        #print(*s, sep='\n\n')
        '''routes = set(JSON['existingRoutes'])
    my_routes = open('works.txt', 'r')
    my_routes = set(my_routes.read().split())
    print(routes - my_routes)
    print()
    print(my_routes - routes)'''
        #print(i, '\n', JSON['trolleyNumbers'], end='\n\n', file=test)
        T = JSON['trolleyNumbers']['fractions']
        Sum = 0
        for i in T:
            if T[i] is None:
                T[i] = 0
            print(i, T[i])
            Sum += T[i]
        print(Sum, Sum / len(T))
        break  
    #test.close()


def CheckFreqs():
    def g(s):
        if s == 'БК':
            return 'Бк'
        if s in ['М27', 'М7', '400Э', 'М3', 'М9', 'М5', '400Т', 'М1', '112Э', 'М2', 'М10',
                 'М8'] or ('К' in s and s not in ['ВК', 'К']):
            return s.lower()
        return s
    
    import json
    import requests
    from urllib.parse import quote

    global F2

    FF = open('freqs.txt', 'w')
    Calculate()
    ref = 'https://raw.githubusercontent.com/sergets/sergets.github.io/master/mgtmap-gp/data/freqs.json'
    r = requests.get(ref)
    source = r.text
    JSON = json.loads(source)
    for route in JSON:
        F2[route] = 0
        for day in JSON[route]:
            bay = bin(int(day))[2:]
            while len(bay) < 7:
                bay += '0'
            #print(day, bay)
            #break
            c = bay.count('1')
            for hour in JSON[route][day]:
                F2[route] += JSON[route][day][hour] * 365 / 7 * c
    SF1 = set([i for i in F1])
    SF2 = set([i.upper() for i in F2])
    R = SF1 & SF2
    R = list(R)
    R.sort()
    #print(R)
    #print(SF1 - SF2)
    #print(SF2 - SF1)
    for i in R:
        print(i, ': \t my number',  round(F1[i]), '\t his number', round(F2[g(i)]), file=FF)
        #if F1[i] * 2 >= F2[g(i)]:
        #    print(i, F1[i], F2[g(i)])
    FF.close()
