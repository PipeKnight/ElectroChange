def GetListOfRoutes():
    import requests

    fout = open('routes_list.txt', 'w')

    ref = 'http://www.mosgortrans.org/pass3/request.ajax.php?list=ways&type=avto'
    r = requests.get(ref)
    text = r.text.split()
    text.remove('route')
    text.remove('stations')
    text.remove('streets')
    print(*text, sep='\n', file=fout)
    fout.close()
