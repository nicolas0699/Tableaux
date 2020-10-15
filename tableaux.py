# -*-coding: utf-8-*-
from random import choice

##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []


##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
    def __init__(self, label, left, right):
        self.left = left
        self.right = right
        self.label = label


def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
    if f.right is None:
        return f.label
    elif f.label == '-':
        return f.label + Inorder(f.right)
    else:
        return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"


def StringtoTree(A):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
    # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree

    # OJO: DEBE INCLUIR SU CÓDIGO DE STRING2TREE EN ESTA PARTE!!!!!

    Conectivos = ['O', 'Y', '>', '=']
    Pila = []
    for c in A:
        if c in letrasProposicionales:
            Pila.append(Tree(c, None, None))
        elif c == '-':
            FormulaAux = Tree(c, None, Pila[-1])
            del Pila[-1]
            Pila.append(FormulaAux)
        elif c in Conectivos:
            FormulaAux = Tree(c, Pila[-1], Pila[-2])
            del Pila[-1]
            del Pila[-1]
            Pila.append(FormulaAux)
        else:
            print(u"Hay un problema: el símbolo " + str(c) + " no se reconoce")
    return Pila[-1]


##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
    cadena = "{"
    primero = True
    for f in H:
        if primero == True:
            primero = False
        else:
            cadena += ", "
        cadena += Inorder(f)
    return cadena + "}"


def complemento(a):
    if a.label == '-':
        print(Inorder(a.right))
        return a.right
    else:
        print(Inorder(Tree('-', None, a)))
        return Tree('-', None, a)


def par_complementario(l):
    # Esta función determina si una lista de solo literales
    # contiene un par complementario
    # Input: l, una lista de literales
    # Output: True/False
    for o in range(0, len(l)):
        if es_literal(l[o]) == True:
            c = complemento(l[o])
        for i in range(0, len(l)):
            if Inorder(c) == Inorder(l[i]):
                return True
    return False


def es_literal(f):
    # Esta función determina si el árbol f es un literal
    # Input: f, una fórmula como árbol
    # Output: True/False
    if f.right is None:
        return True
    elif f.label == '-':
        if f.right.right is None:
            return True
        else:
            return False
    else:
        return False


def no_literales(l):
    # Esta función determina si una lista de fórmulas contiene
    # solo literales
    # Input: l, una lista de fórmulas como árboles
    # Output: None/f, tal que f no es literal
    for i in range(len(l)):
        if not es_literal(l[i]):
            return l[i]
    return None


def clasificacion(f):
    # clasifica una fórmula como alfa o beta
    # Input: f, una fórmula como árbol
    # Output: string de la clasificación de la formula
    if f.label == '-':
        if f.right.label == '-':
            return '1ALFA'
        elif f.right.label == '>':
            return '4ALFA'
        elif f.right.label == 'O':
            return '3ALFA'
        elif f.right.label == 'Y':
            return '1BETA'
        else:
            print("Error en la clasificaión, el conectivo {0} es invalido".format(f.right.label))
    elif f.label == 'Y':
        return '2ALFA'
    elif f.label == 'O':
        return '2BETA'
    elif f.label == '>':
        return "3BETA"
    else:
        print("Error en la clasificaión, el conectivo {0} es invalido".format(f.label))


def clasifica_y_extiende(f, h):
    # Extiende listaHojas de acuerdo a la regla respectiva
    # Input: f, una fórmula como árbol
    # 		 h, una hoja (lista de fórmulas como árboles)
    # Output: no tiene output, pues modifica la variable global listaHojas

    global listaHojas

    print("Formula:", Inorder(f))
    print("Hoja:", imprime_hoja(h))

    assert (f in h), "La formula no esta en la lista!"

    clase = clasificacion(f)
    print("Clasificada como:", clase)
    assert (clase is not None), "Formula incorrecta " + imprime_hoja(h)

    if clase == '1ALFA':
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [f.right.right]
        listaHojas.append(aux)
    elif clase == '2ALFA':
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [f.left, f.right]
        listaHojas.append(aux)
    elif clase == '3ALFA':
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [Tree('-', None, f.left), Tree('-', None, f.right)]
        listaHojas.append(aux)
    elif clase == '4ALFA':
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [f.left, Tree('-', None, f.right)]
        listaHojas.append(aux)
    elif clase == '1BETA':
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [[Tree('-', None, f.left)], [Tree('-', None, f.right)]]
        listaHojas.append(aux)
    elif clase == '2BETA':
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [[f.left], [f.right]]
        listaHojas.append(aux)
    elif clase == '3BETA':
        aux = [x for x in h]
        listaHojas.remove(h)
        aux.remove(f)
        aux += [[Tree('-', None, f.left)], [f.right]]
        listaHojas.append(aux)


# Aqui el resto de casos


def Tableaux(f):
    # Algoritmo de creacion de tableau a partir de lista_hojas
    # Imput: - f, una fórmula como string en notación polaca inversa
    # Output: interpretaciones: lista de listas de literales que hacen
    # verdadera a f

    global listaHojas
    global listaInterpsVerdaderas

    A = StringtoTree(f)
    print(u'La fórmula introducida es:\n', Inorder(A))

    listaHojas = [[A]]

    while len(listaHojas) > 0:
        h = choice(listaHojas)
        print("Trabajando con hoja:\n", imprime_hoja(h))
        x = no_literales(h)
        if x is None:
            if par_complementario(h):
                listaHojas.remove(h)
            else:
                listaInterpsVerdaderas.append(h)
                listaHojas.remove(h)
        else:
            clasifica_y_extiende(x, h)

    return listaInterpsVerdaderas
