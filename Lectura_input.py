with open("C:/UPC/4rt Quadrimestre/OPT/Pràctica Simplex/Input.txt", "r") as archivo:
    total = []
    for i, linea in enumerate(archivo):
        #print(f'linia{i}', linea)
        total.append(linea)
        
    
    llista_dic = []
    iteracio = 0
    i = 0
    c = []
    A = []
    b = []
    num = 1
    while i < len(total):
        #print(total[i])
        if 'c=' in total[i]:
            #print(i)
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
                if not 'C' in total[k]:
                    for item in total[k].split():
                        try:
                            num = int(item)
                            A.append(num)
                        except ValueError:
                            pass  # Si no puede convertirse a entero, omitirlo
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
            iteracio += 1
            #print('iteracio: ', iteracio, '\n', c, A, b)
            nom_dic = 'problem_{}'.format(num)  # Nombre del diccionario con número de iteración
            nom_dic = {'c': c, 'A': A, 'b': b}
            llista_dic.append(nom_dic)
            c = []
            b = []
            A = []
        
        i += 1
          
"""print(len(llista_dic))
print(llista_dic)"""

for dic in llista_dic:
    print('c: ', dic['c'])
    print('b: ', dic['b'])
    print('A: ', dic['A'], '\n')
