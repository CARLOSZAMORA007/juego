
#cambios de carril enemigos/villano y para seleccionar pocion
#posibles estados
#probabilidades de cada estado
#numero pseudoaleatorio generado por la clase utilities/randomnumber creado por congruencial lineal
def montecarlo(items, probabilities, r):
    sum_prob=0
    i=0
    for p in probabilities:
        sum_prob+=p
        if r<=sum_prob:
            break
        else:
            i+=1
    if i>=len(items):
        i=len(items)-1
    return items[i]