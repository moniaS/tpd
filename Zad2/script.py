import numpy as numpy
from scipy.optimize import linprog

arrayRowsInfo = []
arrayColumnsInfo = []
matrix = numpy.loadtxt('wariant5.txt')
optimizedMatrix = matrix
print("Wczytana macierz:")
print(matrix)

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

    print("Wartość maxmin to %d, wiersz %d, kolumna %d" % (max_val, i[0]+1, j+1))
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
    print("Wartość minmax to %d z wiersza %d, kolumny %d" % (minVal, i+1, j[0]+1))
    arrayInfo = [minVal, i+1, j[0]+1]
    return arrayInfo

def checkPunktSiodlowy(rowsInfo, columnsInfo):
    if rowsInfo[0] == columnsInfo[0]:
        print("Wartość puntku siodlowego wynosi %d" % rowsInfo[0])
        if rowsInfo[1] == columnsInfo[1] and rowsInfo[2] == columnsInfo[2]:
            print("Wybrane strategie to %d dla wierszy i %d dla kolumn" % (rowsInfo[1], rowsInfo[2]))
        return True
    return False

#function that search for recessive columns and rows
def findDominatedRowsAndColumns(matrix):
    optimizedMatrix = findDominatedRows(matrix)
    
    if type(optimizedMatrix) is numpy.ndarray:
        return optimizedMatrix
    else:
        return findDominatedColumns(matrix)
    return None

#check for rows domination
def findDominatedRows(matrix):
    rowsNumber = matrix.shape[0]
    tempArray = []
    for i in range(rowsNumber-2):
        tempArray = matrix[i,:]
        for j in range(i+1, rowsNumber-1):
            option = compareTwoVectors(tempArray, matrix[j,:])
            if option == 1:
                optimizedMatrix = numpy.delete(matrix, i, axis=0)
                print("Usunieto wiersz %d zdominowany przez wiersz %d" % (i+1, j+1))
                return optimizedMatrix
            elif option == 2:
                optimizedMatrix = numpy.delete(matrix, j, axis=0)
                print("Usunieto wiersz %d zdominowany przez wiersz %d" % (j+1, i+1))
                return optimizedMatrix
    return None

#check for columns domination
def findDominatedColumns(matrix):
    columnNumber = matrix.shape[1]
    tempArray = []
    for i in range(columnNumber-2):
        tempArray = matrix[:, i]
        for j in range(i+1, columnNumber-1):
            option = compareTwoVectors(tempArray, matrix[:,j])
            if option == 1:
                optimizedMatrix = numpy.delete(matrix, j, axis=1)
                print("Usunieto kolumne %d zdominowana przez kolumne %d" % (j+1, i+1))
                return optimizedMatrix
            if option == 2:
                optimizedMatrix = numpy.delete(matrix, i, axis=1)
                print("Usunieto kolumne %d zdominowana przez kolumne %d" % (i+1, j+1))
                return optimizedMatrix
    return None
   

# return 0 if none of vectors is entirely smaller, return 1 if first is smaller, return 2 if second is smaller
def compareTwoVectors(array1, array2):
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

def checkForDominatedXY(optimizedMatrix):
    #delete dominated rows and columns
    changedMatrix = findDominatedRowsAndColumns(optimizedMatrix)
    if type(changedMatrix) is numpy.ndarray:
        optimizedMatrix = changedMatrix
    else:
        print("Brak zdominowanych wierszy badz kolumn")
    while(type(changedMatrix) is numpy.ndarray):
        changedMatrix = findDominatedRowsAndColumns(optimizedMatrix)
        if type(changedMatrix) is numpy.ndarray:
            optimizedMatrix = changedMatrix
    print("Macierz po optymalizacji")
    print(optimizedMatrix)
    return optimizedMatrix

def prepareMatrixWithPositiveNumbers():
    global optimizedMatrix
    min = checkMinValueInMatrix(optimizedMatrix)
    if min < 0:
        for i in range(optimizedMatrix.shape[0]):
            for j in range(optimizedMatrix.shape[1]):
                optimizedMatrix[i][j] -= min
        return min
    return 0

def checkMinValueInMatrix(matrix):
    min = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] < min:
                min = matrix[i][j]
    return min

def simplexX(temp_matrix):
    c = numpy.ones(len(temp_matrix[0]), dtype= int) #c = c1 * x1 + c2 * x2 itd, w naszym przypadku wspolczynniki c to same
    print(c)
    A = [x * -1 for x in temp_matrix] #mnozymy macierz przez -1 aby zmienić znak na >=
    #print(A)
    b = numpy.full((len(temp_matrix)), -1, dtype=int) #po prawej stronie nierownosci mamy -1 bo podzielilismy przez v i zmienilismy znak
    #print(b)
    bounds = (0, None) #przyjmujemy, ze x1, x2 itp musi byc wieksze rowne 0
    result = linprog(c, A, b, bounds=bounds, method='simplex') #w rezultacie otrzymujemy tablice wynikow x', ktora w naszym przypadku to wartosci x1', x2' itp
    print(result) 
    v = 1 / sum(result.x) #obliczamy wygrana v
    print("Wygrana wynosi %d" % v)
    x = []
    for val in result.x.tolist():
        x.append(v * val) #obliczamy wartosci x1, x2 itp mnozac x1', x2' itp przez v (wygrana)
    print("Współczynniki dla strategii dla wierszy:")
    print(x)

def simplexY(temp_matrix):
    c = numpy.full((len(temp_matrix[0])), -1, dtype=int) #c = c1 * y1 + c2 * y2 itd, w naszym przypadku wspolczynniki c to same -1
    # print(c)
    A = temp_matrix
    # print(A)
    b = numpy.full((len(temp_matrix)), 1, dtype=int) #po prawej stronie nierownosci mamy 1 bo podzielilismy przez v
    # print(b)
    bounds = (0, None) #przyjmujemy, ze y1, y2 itp musi byc wieksze rowne 0
    result = linprog(c, A, b, bounds=bounds, method='simplex') #w rezultacie otrzymujemy tablice wynikow y', ktora w naszym przypadku to wartosci y1', y2' itp
    # print(result) 
    v = 1 / sum(result.x) #obliczamy wygrana v
    print(v)
    y = []
    for val in result.x.tolist():
        y.append(v * val) #obliczamy wartosci y1, y2 itp mnozac y1', y2' itp przez v (wygrana)
    print("Współczynniki dla strategii dla kolumn:")
    print(y) 

minMaxForRows()
maxMinForColumns()
if(checkPunktSiodlowy(minMaxForRows(), maxMinForColumns())):
    quit()
else:
    print("Brak punktu siodłowego. Aby znaleźć rozwiązanie należey skorzystać z programowania liniowego.")

optimizedMatrix = checkForDominatedXY(optimizedMatrix)

minValInMatrix = prepareMatrixWithPositiveNumbers()

simplexX(numpy.transpose(optimizedMatrix))
simplexY(optimizedMatrix)