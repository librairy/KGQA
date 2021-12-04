#import itertools

'''
def exactMatchScore(string1,string2):
    #Funcion auxiliar que incorpora la medida EM (exact match)
    matches = 0
    total = 0
    for (x,y) in itertools.zip_longest(string1,string2):
        if(x == y):
            matches+=1
        total+=1
    return matches/total
'''

def exactMatchScore(string1,string2):
    '''
    Funcion auxiliar que incorpora la medida EM (exact match). 1 si ambas cadenas son iguales, 0 e.o.c.
    Para listas de cadenas, comprueba si ambas contienen los mismos elementos (no importa el orden)
    '''
    if ("," in string1) and ("," in string2):
        string1 = string1.split(",")
        string2 = string2.split(",")
        return int((len(string1) == len(string2)) and (set(string1) == set(string2)))
    return int(string1 == string2)


print(exactMatchScore("north america,south sudan","south sudan,north america"))
print(exactMatchScore("north america, south sudan","south sudan, north america"))
print(exactMatchScore("north america,south sudan","south sudan,north america,south sudan"))