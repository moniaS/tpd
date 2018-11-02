import numpy as numpy

arrayRowsInfo = []
arrayColumnsInfo = []
matrix = numpy.loadtxt('test.txt')
print (matrix)


class MinmaxInfo:
    gameValue = 0
    rowNumber = 0
    columnNumber = 0

def minMaxForRows():
    row_min = []
    row_min_column_index_info = []
    
    #find min value from each row
    for i, row in enumerate(matrix):
        row_min.append(min(row))
        idx, = numpy.where(row == min(row))
        row_min_column_index_info.append(idx[0])
        
    #find max value from the min values
    max_val = max(row_min)

    #check value position in rows
    i, = numpy.where(row_min == max_val)
    #check value position in columns
    j = row_min_column_index_info[i[0]]

    print("Maxmin value is %d from row %d, column %d" % (max_val, i[0]+1, j+1))
    arrayInfo = [max_val, i[0]+1, j+1]
    return arrayInfo
def maxMinForColumns():
    column_max = []
    columnsNumber = matrix.shape[1]
    rowMaxIdxInfo = []

    for i in range(columnsNumber):
        maxInRow = max(matrix[:,i])
        column_max.append(maxInRow)
        #check row index of the max value
        idx, = numpy.where(matrix[:,i] == maxInRow)
        rowMaxIdxInfo.append(idx[0])

    #find min value from the max values
    minVal = min(column_max)

    #check value position in rows
    j, = numpy.where(column_max == minVal)
    i = rowMaxIdxInfo[j[0]]
    print("Minmax value is %d from row %d, column %d" % (minVal, i+1, j[0]+1))
    arrayInfo = [minVal, i+1, j[0]+1]
    return arrayInfo

def checkPunktSiodlowy(rowsInfo, columnsInfo):
    if rowsInfo[0] == columnsInfo[0]:
        print("Wartość puntku siodlowego wynosi %d" % rowsInfo[0])
    if rowsInfo[1] == columnsInfo[1] and rowsInfo[2] == columnsInfo[2]:
        print("Wyrane strategie to %d dla wierszy i %d dla kolumn" % (rowsInfo[1], rowsInfo[2]))

minMaxForRows()
maxMinForColumns()
checkPunktSiodlowy(minMaxForRows(), maxMinForColumns())
#if (arrayRowsInfo[0] == arrayColumnsInfo[0])
