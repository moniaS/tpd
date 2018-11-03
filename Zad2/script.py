import numpy as numpy

arrayRowsInfo = []
arrayColumnsInfo = []
matrix = numpy.loadtxt('wariant1.txt')
optimizedMatrix = []
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
        return True
    return False

#function that search for recessive columns and rows
def findDominatedRowsAndColumns(matrix):
    rowOrColumnDeleted = False
    #check for column domination
    columnsNumber = matrix.shape[1]
    tempArray = []
    for i in range(columnsNumber-2):
        tempArray = matrix[i,:]
        for j in range(i+1, columnsNumber-1):
            print(compareTwoVectors(tempArray, matrix[j,:]))
            #TODO IF RETURNED 1 OR 2 DELETE CORRESPONDING ROW
# return 0 if none of vectors is entirely smaller, return 1 if first is smaller, return 2 if second is smaller
def compareTwoVectors(array1, array2):
    print("Comparing...")
    print(array1)
    print(array2)
    print("--------------")
    arraySize = array1.size
    numberOfSmallerOrEqualElementsInArray1 = 0
    numberOfSmallerOrEqualElementsInArray2 = 0
    for i in range(arraySize):
        if array1[i] <= array2[i]:
            numberOfSmallerOrEqualElementsInArray1 += 1
        elif array1[i] >= array2[i]:
            numberOfSmallerOrEqualElementsInArray2 += 1
    if numberOfSmallerOrEqualElementsInArray1 == arraySize:
        return 1
    elif numberOfSmallerOrEqualElementsInArray2 == arraySize:
        return 2
    else:
        return 0
findDominatedRowsAndColumns(matrix)


#minMaxForRows()
#maxMinForColumns()
#if(checkPunktSiodlowy(minMaxForRows(), maxMinForColumns())):
#    print("Koniec")
#    quit()
#else:
#    print("Brak punktu siodłowego. Aby znaleźć rozwiązanie należey skorzystać z programowania liniowego.")
#if (arrayRowsInfo[0] == arrayColumnsInfo[0])
