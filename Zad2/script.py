import numpy as numpy

matrix = numpy.loadtxt('test.txt')
print (matrix)

def minmax():
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
    max_val_index_i, = numpy.where(row_min == max_val)
    #check value position in columns
    max_val_index_j = row_min_column_index_info[max_val_index_i[0]]

    print("Maxmin value is %d from row %d, column %d" % (max_val, max_val_index_i[0]+1, max_val_index_j+1))
    
minmax()

    