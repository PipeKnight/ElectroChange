F1 = {}
F2 = {}

def Calculate():
    import json
    import requests
    from urllib.parse import quote
    from os import listdir
    from os.path import isfile, join

    global F1, F2

    with open('calcdata.json', 'w') as fout:
        works = open('works.json', 'w')

        t_file = open('timetable.json', 'r', encoding='utf8')
        timetable = json.loads(t_file.readline())

        r_file = open('reestr.json', 'r', encoding='utf8')
        registry = json.loads(r_file.readline())

        routes_list = open('routes_list.txt', 'r')
        routes = routes_list.readlines()


        calc = {}
        percent = {}
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
            if route not in registry or route not in timetable:
                print(route, route in registry, route in timetable)
                continue
            arr = registry[route].split(';')
            dist = float(arr[0].split()[0].split('(')[0].replace(',', '.'))
            num = int(arr[1])
            tmp = timetable[route]
            time = {i.strip(): list(map(int, tmp[i])) for i in tmp}
            cnt = sum(
                365 / 7 * i.count('1') * len(value)
                for i, value in time.items()
                if 'BA' in i
            )

            F1[route] = cnt
            tmparr = [dist] # Расстояние туда и обратно
            if route in F2:
                tmparr.append(F2[route] / max(num, 1))
            else:
                tmparr.append(F1[route] / max(num, 1))
            #print(round(cnt / max(num, 1)), file=fout) # Сколько в среднем за год
            # проходит один автобус по маршруту

            tmparr.append(num) # количество автобусов на маршруте
            if route in percent:
                tmparr.append(percent[route] * 100)
            elif 'НМ-' in route or 'З-' in route:
                tmparr.append(0)
            else:
                tmparr.append(Sum * 100) # процент под контактной сетью
            tmparr.append(30) # расход топлива на 100 км
            calc[route] = [str(i) for i in tmparr]
        ROUTES = ["-1"]
        ROUTES.extend(iter(calc))
        print(json.dumps(calc, ensure_ascii=False), file=fout)
        print(json.dumps(ROUTES, ensure_ascii=False), file=works)
    works.close()


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
