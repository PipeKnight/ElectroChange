def ParseMosgortransTimetable():
    import requests
    from urllib.parse import quote

    h = '<span class="hour"'
    m = '<span class="minutes"'
    routes_list = open('routes_list.txt', 'r')
    stations = 'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto' # если хотим список всех станций
    prefix = 'http://www.mosgortrans.org/pass3/shedule.php?type=avto'
    Date = ['1111111', '1111110', '1111100', '1111000', '0000011', '1000000', '0000100', '0000010', '0000001']
    Direction = ['AB', 'BA'] # AB - туда, BA - обратно
    Waypoint = ['0'] # мы же хотим смотреть только первую остановку, по сути?
    # хотя для учета сокращенных маршрутов надо переделать

    for way in routes_list.readlines():
        way = way.strip()
        with open(f'timetable/{way}.txt', 'w', encoding='utf-8') as route_file:
            for date in Date:
                route = {}
                for direction in Direction:
                    for waypoint in Waypoint:
                        ref = (
                            f'{prefix}&way='
                            + quote(way.encode('cp1251'))
                            + '&date='
                            + date
                            + '&direction='
                            + direction
                            + '&waypoint='
                            + waypoint
                        )

                        r = requests.get(ref)
                        source = r.text.split('\n')
                        hour = -1
                        minute = -1
                        for s in source:
                            if h in s:
                                hour = s.split(h)[1].split('>')[1].split('<')[0]
                            if m in s:
                                color = f'{date} {direction}'
                                if 'style="color: ' in s:
                                    color += ' ' + s.split('style="color: ')[1].split(';')[0]
                                minute = s.split(m)[1].split('>')[1].split('<')[0]
                                if minute == '':
                                    continue
                                time = int(hour) * 60 + int(minute)
                                if color not in route.keys():
                                    route[color] = []
                                route[color].append(time)
                for i, value in route.items():
                    print(i, file=route_file)
                    print(*value, file=route_file)


def ParseLkcarTimetable():
    import requests
    from urllib.parse import quote

    h = '<span class="hour"'
    m = '<span class="minutes"'
    stations = 'http://www.mosgortrans.org/pass3/request.ajax.php?list=waypoints&type=avto' # если хотим список всех станций
    prefix = 'http://lkcar.transport.mos.ru/ExternalService/schedule/table?'
    Date = ['WEEKDAYS', 'WEEKENDS']
    Direction = ['0', '1'] # 0 - туда, 1 - обратно
    Waypoint = ['0'] # ???

    for way in range(5000):
        way = string(way)
        with open(f'timetable2/{way}.txt', 'w', encoding='utf-8') as route_file:
            for date in Date:
                route = {}
                for direction in Direction:
                    for waypoint in Waypoint:
                        ref = (
                            f'{prefix}&way='
                            + quote(way.encode('cp1251'))
                            + '&date='
                            + date
                            + '&direction='
                            + direction
                            + '&waypoint='
                            + waypoint
                        )

                        r = requests.get(ref)
                        source = r.text.split('\n')
                        hour = -1
                        minute = -1
                        for s in source:
                            if h in s:
                                hour = s.split(h)[1].split('>')[1].split('<')[0]
                            if m in s:
                                color = f'{date} {direction}'
                                if 'style="color: ' in s:
                                    color += ' ' + s.split('style="color: ')[1].split(';')[0]
                                minute = s.split(m)[1].split('>')[1].split('<')[0]
                                if minute == '':
                                    continue
                                time = int(hour) * 60 + int(minute)
                                if color not in route.keys():
                                    route[color] = []
                                route[color].append(time)
                for i, value in route.items():
                    print(i, file=route_file)
                    print(*value, file=route_file)
