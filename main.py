from GetListOfRoutes import *
from ParseTimetable import *
from ParseRegistry import *
from Calculate import *

# https://openpyxl.readthedocs.io/en/stable/api/openpyxl.utils.cell.html
# https://stackoverflow.com/questions/23562366/how-do-i-get-value-present-in-a-merged-cell

GetListOfRoutes()
ParseMgtTimetable()
ParseRegistry()
Calculate()
print('Everything calculated!')
print('Updating ended!')
