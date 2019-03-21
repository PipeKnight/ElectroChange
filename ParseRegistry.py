#link to registry:
# https://www.mos.ru/dt/function/razvitie-nazemnogo-obshchestvennogo-transporta/reestr-regulyarnyh-marshrutov/

def PrepareTable(sheet, merged):
    import openpyxl
    import openpyxl.utils
    Dict = dict()
    for mrg in merged:
        merged_cells = list(openpyxl.utils.cols_from_range(mrg))
        for cell in merged_cells[0]:
            Dict[cell] = merged_cells[0][0]
        #print(mrg, merged_cells, merged_cells[0])
        for cell in merged_cells:
            #print(cell[0])
            #print(cell, cell[0], merged_cells[0][0])
            Dict[cell[0]] = merged_cells[0][0]
    return Dict


def getValueWithMergeLookup(linkmerged, sheet, cell):
    idx = cell.coordinate
    if idx in linkmerged:
        return sheet[linkmerged[idx]].value
    else:
        print("No such key: ", idx)
        return 0
          

def ParseRegistry():
    import json
    import openpyxl

    print("Started working with registry.")
    reestr = dict()
    reestrfile = open('reestr.json', 'w', encoding='utf8')
    log = open('collizions.txt', 'w')
    logarr = []
    for partnum in [1, 2]:
        print("Doing part number:", partnum)
        wb = openpyxl.load_workbook(filename='Reestr_' + str(partnum) + '.xlsx', data_only=True)
        ws = wb.active
        mergedcells = sorted([str(i) for i in ws.merged_cell_ranges])
        linktofirstcell = PrepareTable(ws, mergedcells)
        arr = [[cell.value if str(type(cell)) != "<class 'openpyxl.cell.cell.MergedCell'>" else getValueWithMergeLookup(linktofirstcell, ws, cell) for cell in row] for row in ws.rows]
        i = 5
        while i < len(arr):
            name = str(arr[i][1])
            if 'Зеленоград' in ''.join(list(map(str, arr[i]))) or name in reestr and '01' <= name <= '32':
                name = 'З-' + name
            if name in reestr or name == 'None':
                i += 1
                logarr.append(name)
                continue
            if type(name) != type('string'):
                name = name.decode('cp1251')
            name = name.upper()
            if partnum == 1:
                t1 = arr[i][7:10]
            else:
                t1 = arr[i][8:11]
            if partnum == 1:
                t2 = str(arr[i][13])
            else:
                t2 = str(arr[i][14])
            if partnum == 1:
                t3 = arr[i][15:19]
            else:
                t3 = arr[i][16:20]
            
            for j in range(len(t1)):
                t1[j] = str(t1[j])
                if '\n' in t1[j]:
                    t1[j] = t1[j].replace('\n', '')
            for j in range(len(t3)):
                if t3[j] is None:
                    t3[j] = 0
                t3[j] = str(t3[j])
            #print(name, t1, t2, t3)
            i += 1
            reestr[name] = ' '.join(t1) + ';' + t2 + ';' + ' '.join(t3)
    print("Finished! Number of routes in registry:", len(reestr))
    print(json.dumps(reestr, ensure_ascii=False), file=reestrfile)
    logarr = list(set(logarr))
    # Here should be logging
    reestrfile.close()
