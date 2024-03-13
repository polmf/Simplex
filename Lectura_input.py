from simplex import *

with open("C:/UPC/4rt Quadrimestre/OPT/Pràctica Simplex/Input.txt", "r") as archivo:
    total = []
    cjt1 = None
    cjt2 = None
    for linea in archivo:
        if 'alumno' in linea and '34' in linea:
            cjt1 = True
            
        if 'alumno' in linea and '35' in linea:
            cjt1 = False
            
        if 'alumno' in linea and '45' in linea:
            cjt2 = True
            
        if 'alumno' in linea and '46' in linea:
            cjt2 = False
        
        if cjt1:
            #print(f'linia{i}', linea)
            total.append(linea)
            
        if cjt2:
            total.append(linea)
        
    
    llista_dic = []
    iteracio = 0
    
    i = 0
    c = []
    A = []
    b = []
    
    num = 1
    f = True
    trobat = False
    while i < len(total) and f:
        
        if 'c=' in total[i]:
            
            k = i+1
            while 'A=' not in total[k]:
                if not 'C' in total[k]:
                    for item in total[k].split():
                        try:
                            num = int(item)
                            c.append(num)
                        except ValueError:
                            pass  # Si no puede convertirse a entero, omitirlo
                k+=1
                i = k
        
        if 'A=' in total[i]:
            k = i+1
            while 'b=' not in total[k]:
                
                if 'Col' in total[k] and not trobat:
                    trobat = True
                    k += 1    
                
                if not 'Col' in total[k]:
                    
                    numbers = total[k].strip().split()
                    # Convertir los números de cadena a enteros
                    row = [int(num) for num in numbers]
                    # Agregar la fila a la lista de filas
                    
                    if len(row):    
                        A.append(row)
                    
                    
                if 'Col' in total[k] and trobat:
                    k += 1
                    print(len(A))
                    A_ = []
                    
                    for i in range(len(A)+1):
                        numbers = total[k+i].strip().split()
                        row = [int(num) for num in numbers]
                        
                        if len(row):    
                            A_.append(row)
                    
                    # Añadir las nuevas columnas a cada fila de la matriz A
                    for i in range(len(A)):
                        A[i] += A_[i]
                    
                    k = k+len(A)
                   
                k+=1
                i = k
                
        if 'b=' in total[i]:
            k = i+1
            while k < len(total):
                if 'c=' in total[k]:
                    i = k-1
                    break
                
                if 'vb*=' in total[k]:
                    k += 2
                    
                if not 'C' in total[k]:
                    for item in total[k].split():
                        try:
                            num = int(item)
                            b.append(num)
                        except ValueError:
                            pass  # Si no puede convertirse a entero, omitirlo
                k+=1
                i = k
                
        #print(c, A, b)
        if len(c) and len(A) and len(b):
            
            Simplex(c=c, b=b, A=A)
            
            #iteracio += 1
            #print('iteracio: ', iteracio, '\n', c, A, b)
            #nom_dic = 'problem_{}'.format(num)  # Nombre del diccionario con número de iteración
            #nom_dic = {'c': c, 'A': A, 'b': b}
            #llista_dic.append(nom_dic)
            #c = []
            #b = []
            #A = []
            f = False
            
        i += 1

