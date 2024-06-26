import numpy as np


    
class Iteracions:

    def __init__(self, c, b, A, B, N, i, nom=None):
        
        """Inicialitzem els valors que necessitarem en la fase1
        """
        self.c = c # nous coeficients en la funcio objectiu
        self.b = b # resultats restriccions
        self.restriccions = A # resulta una matriu amb els coeficients de les variables en les restriccions
        self.B = B # inicialitzem els indexs de les variables bàsiques amb les noves variables artificials
        self.N = N # inicialitzem els indexs de les variables no bàsiques amb les variables originals en forma estandar
        self.Cb = np.array(self.fer_Cb_Cn(self.B)) # coeficients de les variables bàsiques en la funció objectiu
        self.Cn = np.array(self.fer_Cb_Cn(self.N)) # coeficients de les variables no bàsiques en la funció objectiu
        self.mB = np.array(self.fer_matriu(self.B)) # matriu dels coeficients de les variables bàsiques en les restriccions
        self.An = np.array(self.fer_matriu(self.N)) # matriu dels coeficients de les variables no bàsiques en les restriccions
        self.mB_inv = np.linalg.inv(self.mB) # matriu inversa de la matriu mB
        self.Xb = np.dot(self.mB_inv,self.b) # resultat de calcular la Identitat (B^-1) x b
        self.Xn = [0]*len(self.N) # sempre han de ser 0 i len(variables no bàsiques)
        self.z = np.dot(self.Cb,self.Xb) # resultat del producte escalar entre els vectors cb i xb
        self.i = i # numero d'iteracions
        self.nom = nom # nom del fitxer de sortida
        
        self.es_optim()
    
    def fer_matriu(self, Bases): # Funció per a contruir les matrius mB i An
        
        columnes_de_indexs =[]
        for index in Bases:
            columna = self.restriccions[:,index-1]
            columnes_de_indexs.append(columna)
        
        return np.column_stack(columnes_de_indexs)
    
    def fer_Cb_Cn(self, Bases): #Funció per a construir  Cb i Cn
        
        Cx = []  
        for index in Bases:  
            Cx.append(self.c[index-1]) 
        
        return Cx

    def es_optim(self):

        Cb_mB_inv = np.dot(self.Cb, self.mB_inv) # producte escalar entre cb i la inversa calculada
        Cb_mB_inv_An = np.dot(Cb_mB_inv, self.An) # calcul de cb x B^-1 x An
        self.r = self.Cn - Cb_mB_inv_An # calcul final del cost reduït
        
        if self.positius(self.r): # si r és positiu np.all(vector > 0)
            return self.optim()
        
        else:
            self.canviar_base(self.r)


    def positius(self, r): # funció per a veure si tots els elements son positius

        for element in r:
            if element < 0:
                return False
        return True
    
    def canviar_base(self,r):

        q = self.primer_negatiu(r) # retornem l'index de la primera variable negativa que ens trobem (Regla de Bland) 
        
        db = np.dot(-(self.mB_inv),self.trobar_Aq(q)) # calculem db = - B^-1 x Aq (coeficients de la variable amb index q en les restriccions)
        
        rq= r[q] 
        
        if self.positius(db): # si db es positiu
            
            with open(self.nom, 'a', encoding='utf8') as sortida:
                
                print('\nDBF de descens no acotada, Problema Lineal no acotat', file=sortida)
                self.B = None
                return None
        
        theta, p = self.calcular_0_p(db) # calculem el valor de la theta i lindex de la variable de sortida

        self.entra = self.N[q] # id variable d'entrada
        self.surt = self.B[p] # id variable de sortida

        self.B[p] = self.entra # actualitzem variables de B
        self.N[q] = self.surt # actualitzem variables de N

        self.N.sort() # ordenem els indexs de les variables no bàsiques

        index_cn = next(i for i in range(len(self.N)) if self.N[i] == self.surt)

        if self.c[self.N[q]-1]!=0: # si el coeficient de la variable que ha entrat en les no bàsiques és diferent de 0
            self.Cn[index_cn] = self.c[self.N[q]-1] # actualitzem vector cn amb el coeficient en la funcio objectiu de la variable que entra en N
        else:
            self.Cn[index_cn] = 0

        self.actualitzar(theta, p, rq, db)

    def actualitzar(self, theta, p, rq, db):
        
        columna_entra = self.restriccions[:, self.B[p]-1]
        self.mB[:, p]=columna_entra
        
        self.An = self.fer_matriu(self.N)
        
        e = np.eye(len(self.mB))
        nova_columna = []
        for i in range(len(db)):
            if i != p:
                nova_columna.append(-db[i] / db[p]) 
            else:
                nova_columna.append(-1/db[p])
        nova_columna = np.array(nova_columna) 
        
        e[:, p] = nova_columna
        self.mB_inv = np.dot(e,self.mB_inv)
        
        # actualitzem Xb sense fer ús de la inversa
        for i in range(len(self.Xb)):
            if i == p:
                self.Xb[p] = theta
            else:
                self.Xb[i] += (theta*db[i])
        
        self.z = self.z + (theta*rq)
        
        if self.c[self.B[p]-1]!=0:
            self.Cb[p] = self.c[self.B[p]-1]
        else:
            self.Cb[p] = 0
        
        self.Cn = self.fer_Cb_Cn(self.N)

        
        with open(self.nom, 'a', encoding='utf8') as sortida:
            print(f"Iteració {self.i}: N[q] = {self.surt}, B[p] = {self.entra}, theta*= {round(theta,3)}, z = {round(self.z,4)}", file=sortida)

        if self.positius(self.Xb):
            
           self.i += 1
           self.es_optim()
           
        else:
            
            with open(self.nom, 'a', encoding='utf8') as sortida:
                print("\nS'ha perdut la factibilitat", file=sortida)
                self.B = None
                return None
                
    def primer_negatiu(self,r): # Troba l'index del primer element negatiu

        for i in range(len(r)):
            if r[i] < 0:
                return i
        return None
    
    def trobar_Aq(self, q): #Troba la columna Aq

        Aq = []
        for fila in self.An:
            Aq.append(fila[q])

        return np.array(Aq)

    def calcular_0_p(self,db): # Calcula els valors de p i tetha
        
        llista_min = []
        indexs_min = []
        
        for i in range(len(self.b)):
            if db[i]<0:
            
                llista_min.append(-self.Xb[i]/db[i])
                indexs_min.append(i)
        
        minim = min(llista_min)
        index = llista_min.index(minim)
        p = indexs_min[index]
        
        return minim, p

    
    def base_B_N(self): # Retorna les noves bases i el nombre d'iteracions
                    
        return  self.B, self.N, self.i
        
    def optim(self): # retorna la base la Xb el costos reduits i la z del resultat optim
        
        return self.B, self.Xb, self.z, self.r, self.i
    

class Simplex:
    
    def __init__(self, c, b, A, cjt=None, pl=None):
        self.c = np.array(c) # inicialitzem c
        self.b = np.array(b) # inicialitzem b
        self.A = np.array(A) # inicialitzem la matriu A
        self.i = 0 # inicialitzem el nombre d'iteracions
        
        self.nom = f'Cjt{cjt}_Problema{pl}_sortida.txt'
        
        with open(self.nom, 'w', encoding='utf8') as sortida:
            
            print("Inici simplex primal amb regla de Bland", file=sortida)

        self.fase1() # Comencem la fase I
        
    def fase1(self):
        with open(self.nom, 'a', encoding='utf8') as sortida:
            print("Fase I", file=sortida)
            
        c = [0] * len(self.c) + [1] * len(self.b) # Tornem a construir c amb els nous valors
        A = np.hstack((self.A, np.eye(len(self.b)))) # Tornem a construir A amb els nous valors
        B = list(range(len(self.c) + 1, len(c)+1)) # Construim la base amb les variables bàsiques que pertanyen a les variables auxiliars
        N = list(range(1,len(self.c)+1)) # Construim la base de les variables no bàsques les quals son les variables originals del problema
        indexs = B.copy() # guardem els indexs de les variables auxiliars
        
        self.B, self.N, self.i = Iteracions(c, self.b, A, B, N, self.i, self.nom).base_B_N() # Trobem una base factible
 
        if self.no_tenen_valor(indexs): # Si les variables auxiliars no tenen valor les eliminem

            for _ in range(len(self.B)): 
                self.N.pop()

            self.fase2() # Comencem la fase II
            
        else:
            with open(self.nom, 'a', encoding='utf8') as sortida:
                print('\nEl problema lineal no és factible ja que z* > 0 en la fase I', file=sortida)
        
    def fase2(self):
        with open(self.nom, 'a', encoding='utf8') as sortida:
            print("Fase II", file=sortida)
            
        self.B, self.Xb, self.z, self.r, self.i = Iteracions(self.c, self.b, self.A, self.B, self.N, self.i, self.nom).optim() # Trobem la solució optima
        
        if self.B: # Si té solució donem el resultat
            
            with open(self.nom, 'a', encoding='utf8') as sortida:
                print("\nSolució òptima trobada, iteració = ", self.i-1,", z = ", round(self.z,4), file=sortida)
                print("Fi simplex primal", file=sortida)
            
            self.solucio()
        
    def no_tenen_valor(self,indexs): # Mira que les variables auxiliars no tinguin valor
        
        for valor in indexs:         
            if valor in self.B:
                return False
            
        return True
    
    def solucio(self): # Escriu la solució en el document de sortida
        
        with open(self.nom, 'a', encoding='utf8') as sortida:
            print("\nSolució òptima: \n", file=sortida)
        
            Vb = ' '.join(str((numero)) for numero in self.B)
            print("Vb = ", Vb, file=sortida)
        
            Xb = ' '.join(str(round(numero,2)) for numero in self.Xb)
            print("xb = ", Xb, file=sortida)
            print("z = ", round(self.z,4), file=sortida)
            r = ' '.join(str(round(numero,2)) for numero in self.r)
            print("r = ", r, file=sortida)
