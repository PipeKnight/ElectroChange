from GetListOfRoutes import *
from ParseTimetable import *
from Calculate import *
from TextToJson import *
from UpdateListOfRoutes import *

GetListOfRoutes()
print('List of routes got!')
ParseMosgortransTimetable()
print('Timetable parsed!')
Calculate()
print('Everything calculated!')
GetWorkingRoutes()
TextToJson()
print('Updating ended!')
