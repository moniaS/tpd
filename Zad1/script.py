import numpy as np
#load 2d array from file
matrix = np.loadtxt('sample.txt')
print(matrix)

def minimax():
    row_min = [] 

    for i, row in enumerate(matrix):
        row_min.append(min(row)) #for every row we find min value and add it to row_min array

    max_val = max(row_min) #find max value from min values in rows

    best_decisions = [] 
    for i, row in enumerate(matrix):
        if (min(row) == max_val):
            best_decisions.append(i + 1) 
    
    print('Wynik kryterium minimax: ' + str(max_val) + ', najlepsza decyzja: ' + str(best_decisions))

def maxmax():
    row_max = [] 

    for i, row in enumerate(matrix):
        row_max.append(max(row)) #for every row we find max value and add it to row_max array

    max_val = max(row_max) #find max value from max values in rows

    best_decisions = [] 
    for i, row in enumerate(matrix):
        if (max(row) == max_val):
            best_decisions.append(i + 1)
    
    print('Wynik kryterium maxmax: ' + str(max_val) + ', najlepsza decyzja: ' + str(best_decisions))

def count_row_indicator(min, max, indicator):
    return indicator * min + (1 - indicator) * max 

def get_caution_indicator():
    indicator_result = None
    while(indicator_result == None):
        indicator = float(input('Podaj współczynnik ostrożności dla kryterium Hurwicza: '))
        is_indicator_correct = check_indicator_value(indicator)
        if(is_indicator_correct):
            indicator_result = indicator
        else:
            print('Współczynnik ostrożności musi mieścić się w przedziale zamkniętym od 0 do 1')
            indicator_result = None
    return indicator_result

def check_indicator_value(indicator):
    return (indicator >= 0 and indicator <= 1)

def hurwicz():
    indicator = get_caution_indicator()
    row_indicators = []
    for row in matrix:
        row_indicators.append(count_row_indicator(min(row), max(row), indicator)) #count caution indicator for every row

    max_val = max(row_indicators) #find max value from rows indicators

    best_decisions = []
    for i, val in enumerate(row_indicators):
        if (val == max_val):
            best_decisions.append(i + 1)
    
    print('Wynik kryterium Hurwicza dla współczynnika ostrożności ' + str(indicator) + ': ' + str(max_val) + ', najlepsza decyzja: ' + str(best_decisions))

def bayes_laplace():
    probabilities = np.loadtxt('probabilities.txt')
    row_values = []
    for row in matrix:
        row_value = 0
        for i, col_val in enumerate(row):
            row_value += col_val * probabilities[i]
        row_values.append(row_value)
    
    max_val = max(row_values)

    best_decisions = []
    for i, val in enumerate(row_values):
        if (val == max_val):
            best_decisions.append(i + 1)

    print('Wynik kryterium Bayesa-Laplace: ' + str(max_val) + ', najlepsza decyzja: ' + str(best_decisions))
    
minimax()
maxmax()
hurwicz()
bayes_laplace()
