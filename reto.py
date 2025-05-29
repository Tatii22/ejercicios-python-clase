#reto 

lista = [300, 5, 3, 7,0, 9, 200, -3, 76]

def ordenar():
    for izq in range (len(lista)-1):
        for der in range (izq +1, len (lista)):
            if lista [izq]< lista [der]:
                tem = lista[izq]
                lista [izq]= lista [der]
                lista [der]= tem 

        print (f"der: {lista}")
    print (f"izq:{lista}")

#ordenar()
#investigar como funciona el quicksort
def Ordenarquick(lista):
    if len(lista) <= 1:
        return lista
    else:
        pivot = lista[len(lista) // 2]  # Tomamos el pivote en la mitad
        left = [x for x in lista if x < pivot]    # Elementos menores al pivote
        middle = [x for x in lista if x == pivot] # Elementos iguales al pivote
        right = [x for x in lista if x > pivot]   # Elementos mayores al pivote
        return Ordenarquick(left) + middle + Ordenarquick(right)

# Llamamos a la función y mostramos el resultado
resultado = Ordenarquick(lista)
print("Lista ordenada:", resultado)