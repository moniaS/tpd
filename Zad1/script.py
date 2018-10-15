import numpy as np
#load 2d array from file
matrix = np.loadtxt('sample.txt')
print(matrix)

def minimax():
    row_min = [] 
    best_decisions = [] 

    # find min value for every row and add it to row_min array
    for row in matrix:
        row_min.append(min(row))

    # find max value from min values in rows
    max_val = max(row_min) 

    for i, row in enumerate(matrix):
        if (min(row) == max_val):
            best_decisions.append(i + 1) 
    
    print('Wynik kryterium minimax: ' + str(max_val) + ', najlepsza decyzja: ' + str(best_decisions))

def maxmax():
    row_max = [] 
    best_decisions = [] 

    # find max value for every row and add it to row_max array
    for row in matrix:
        row_max.append(max(row)) 

    # find max value from max values in rows
    max_val = max(row_max) 

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
    best_decisions = []

    # count caution indicator for every row
    for row in matrix:
        row_indicators.append(count_row_indicator(min(row), max(row), indicator)) 

    # find max value from rows indicators
    max_val = max(row_indicators) 

    for i, val in enumerate(row_indicators):
        if (val == max_val):
            best_decisions.append(i + 1)
    
    print('Wynik kryterium Hurwicza dla współczynnika ostrożności ' + str(indicator) + ': ' + str(max_val) + ', najlepsza decyzja: ' + str(best_decisions))

def bayes_laplace_different_probabilities():
    probabilities = np.loadtxt('probabilities.txt')
    row_values = []
    best_decisions = []

    # count value for every row using given probabilities
    for row in matrix:
        row_value = 0
        for i, col_val in enumerate(row):
            row_value += col_val * probabilities[i]
        row_values.append(row_value)
    
    max_val = max(row_values)

    # find decisions with max value
    for i, val in enumerate(row_values):
        if (val == max_val):
            best_decisions.append(i + 1)

    print('Wynik kryterium Bayesa-Laplace z różnymi prawdopodobieństwami: ' + str(max_val) + ', najlepsza decyzja: ' + str(best_decisions))

def bayes_laplace_same_probabilities():
    row_values = []
    best_decisions = []

    for row in matrix:
        row_values.append(sum(row)/len(row))
    
    max_val = max(row_values)

    # find decisions with max value
    for i, val in enumerate(row_values):
        if (val == max_val):
            best_decisions.append(i + 1)

    print('Wynik kryterium Bayesa-Laplace z jednakowymi prawdopodobieństwami: ' + str(max_val) + ', najlepsza decyzja: ' + str(best_decisions))

def savage():
    max_columns = [0] * len(matrix[0])
    relative_losses = []
    max_relative_losses = []
    best_decisions = []
    
    # find max values in columns
    for row in matrix:
        for i, col_val in enumerate(row):
            if (col_val > max_columns[i]):
                max_columns[i] = col_val

    # count relative loss for every element of matrix
    for i, row in enumerate(matrix):
        relative_losses.append([])
        for j, col_val in enumerate(row):
            relative_losses[i].append(max_columns[j] - col_val)

    # find max relative loss in every row
    for row in relative_losses:
        max_relative_losses.append(max(row))

    # find min loss from max relative losses
    min_loss = min(max_relative_losses)

    # find decisions with min loss
    for i, val in enumerate(max_relative_losses):
        if (val == min_loss):
            best_decisions.append(i + 1)

    print('Wynik kryterium Savage: ' + str(min_loss) + ', najlepsza decyzja: ' + str(best_decisions))
 
minimax()
maxmax()
hurwicz()
bayes_laplace_different_probabilities()
bayes_laplace_same_probabilities()
savage()
