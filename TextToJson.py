def TextToJson():
    from os import listdir
    from os.path import isfile, join

    fin = open('works.txt', 'r')
    fout1 = open('json_data.txt', 'w')
    fout2 = open('json_routes.txt', 'w')
    arr = fin.read().split()
    s1 = "'{ "
    s2 = "'[ "
    s2 += '"-1", '
    for i in arr:
        s1 += '"' + i + '": ['
        s2 += '"' + i + '"'
        curf = open('calcdata/' + i + '.txt', 'r')
        a = curf.read().split()
        for j in a[:len(a) - 1]:
            s1 += '"' + j + '", '
        s1 += '"' + a[-1] + '"], '
        s2 += ', '
    s1 = s1[:len(s1) - 2]
    s2 = s2[:len(s2) - 2]
    s1 += " }';"
    s2 += " ]';"
    print(s1, file=fout1)
    print(s2, file=fout2)
    fout1.close()
