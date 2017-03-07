'''
    # Asignatura: Sistemas de Gestion de Datos y de la Informacion
    # Practica 1 (MapReduce y ApacheSpark)
    # Grupo 10 (Adrian Garcia y Frank Julca)
    # Declaracion de integridad: Adrian Garcia y Frank Julca
    declaramos que esta solucion es fruto exclusivamente de nuestro trabajo personal.
    No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solucion de fuentes externas,
    y tampoco hemos compartido nuestra solucion con nadie. Declaramos ademas que no hemos realizado de manera
    deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demas.
'''

from mrjob.job import MRJob
from mrjob.compat import jobconf_from_env
from operator import itemgetter

class MRInvertedIndex(MRJob):

    # Fase MAP (line es una cadena de texto) emite cada palabra de la linea como clave y el archivo
    # al que pertenecen como valor.
    def mapper(self, key, line):
        
        # Eliminamos los caracteres especiales salvo que sean espacios en blanco o comillas simples.
        formatLine = ''.join(e for e in line if e.isalpha() or e == ' ' or e == "'")
        for word in formatLine.lower().split():
            yield word, jobconf_from_env('mapreduce.map.input.file')

    # Fase REDUCE (key es una cadena texto, values un generador de nombres de ficheros) emite la palabra
    # como clave y como valor tuplas (archivo, apariciones) con los nombres de los archivos en los que
    # aparecen y su numero de veces.
    def reducer(self, key, values):

        # Creamos un diccionario para contar las apariciones de la palabra en cada archivo y detectar si
        # en alguno de ellos aparece mas de 20 veces.
        books = {}
        mayorDeVeinte = False
        for file in values:
            if file in books:
                books[file] += 1
                if books[file] > 20:
                    mayorDeVeinte = True
            else:
                books[file] = 1
    
        if mayorDeVeinte:
            
            # Ordenamos los archivos en los que aparece por el numero de apariciones y obtenemos
            # una lista de tuplas (archivo, numero de apariciones).
            orderedBooks = sorted(books.items(), key=itemgetter(1), reverse=True)
            
            # Unimos cada tupla de la lista por comas para formatear la salida.
            infoBooks = ', '.join(str((file,value)) for file,value in orderedBooks)
            yield key, infoBooks

if __name__ == '__main__':
    MRInvertedIndex.run()
