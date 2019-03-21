def GetWorkingRoutes():
    from os import listdir
    from os.path import isfile, join

    fout = open('works.txt', 'w')
    files1 = [f.split('.')[0] for f in listdir('reestr/') if isfile(join('reestr/', f))]
    files1 = set(files1)
    files2 = open('routes_list.txt', 'r')
    files2 = set(files2.read().split())
    ans = list(files1 & files2)
    ans.sort()
    print(*ans, sep='\n', file=fout)
    fout.close()
