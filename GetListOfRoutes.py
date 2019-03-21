def GetListOfRoutes():
    import requests

    fout = open('routes_list.txt', 'w')

    ref = 'http://www.mosgortrans.org/pass3/request.ajax.php?list=ways&type=avto'
    r = requests.get(ref)
    text = r.text.split()
    rmv = ['route', 'stations', 'streets']
    for i in rmv:
        if i in text:
            text.remove(i)
    print(*text, sep='\n', file=fout)
    fout.close()
