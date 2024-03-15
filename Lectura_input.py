from simplex import *

with open("Input.txt", "r") as archivo:
    total = []
    cjt1 = None
    canvi = None
    for linea in archivo:
        if 'alumno' in linea and '34' in linea:
            cjt1 = True
            
        elif 'alumno' in linea and '35' in linea:
            cjt1 = False
            
        elif 'alumno' in linea and '45' in linea:
            canvi = True
            
        elif 'alumno' in linea and '46' in linea:
            break
        
        if cjt1:
            total.append(linea)
            
        elif canvi:
            total.append(linea)
        
    
    i = 0
    c = []
    A = []
    b = []
    
    pl = 1
    
    trobat = False
    
    while i < len(total):
        
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
                
                if 'alumno' in total[i] and '45' in total[i]:
                    canvi = False
                
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
                
                
        if len(c) and len(A) and len(b):
            if not canvi and pl == 5:
                pl = 1
                cjt1 = True
                
            if not canvi and cjt1:
                Simplex(c=c, b=b, A=A, cjt='45', pl=pl)
            else:
                Simplex(c=c, b=b, A=A, cjt='34', pl=pl)
            
            c = []
            b = []
            A = []
            pl += 1

        i += 1

