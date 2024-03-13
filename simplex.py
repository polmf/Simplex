import numpy as np


    
class Iteracions:

    def __init__(self, c, b, A, B, N, i):
        
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
        
        self.indexs_nous = self.B.copy()
        
        self.es_optim()
    
    def fer_matriu(self, Bases):
        
        columnes_de_indexs =[]
        for index in Bases:
            columna = self.restriccions[:,index-1]
            columnes_de_indexs.append(columna)
        
        return np.column_stack(columnes_de_indexs)
    
    def fer_Cb_Cn(self, Bases):
        
        Cx = []  # Inicializamos una matriz fila de ceros
    
        for index in Bases:
            
            Cx.append(self.c[index-1])  # Asignamos los valores de c en los índices de B a Cb
        
        return Cx

    def es_optim(self):

        self.mB_inv = np.linalg.inv(self.mB) # calculem inversa de la matriu B (dels coeficients en restr. de les var. bàsiques)
        Cb_mB_inv = np.dot(self.Cb, self.mB_inv) # producte escalar entre cb i la inversa calculada
        Cb_mB_inv_An = np.dot(Cb_mB_inv, self.An) # calcul de cb x B^-1 x An
        self.r = self.Cn - Cb_mB_inv_An # calcul final del cost reduït
        
        if self.positius(self.r): # si r és positiu np.all(vector > 0)

            return self.optim()
        
        else:
            self.canviar_base(self.r)


    def positius(self, r):

        for element in r:
            if element < 0:
                return False
        return True
    
    def canviar_base(self,r):

        q = self.primer_negatiu(r) # retornem l'index de la primera variable negativa que ens trobem (Regla de Bland)  
        # mB_inv = np.linalg.inv(self.mB) # ja la tenim calculada
        db = np.dot(-(self.mB_inv),self.trobar_Aq(q)) # calculem db = - B^-1 x Aq (coeficients de la variable amb index q en les restriccions)
        
        rq= r[q] 
        
        if self.positius(db): # si db es positiu
            
            with open('sortida.txt', 'a') as sortida:
                
                print('DBF de descenso no acotada, Problema Lineal no acotado', file=sortida)
        
        theta, p = self.calcular_0_p(db) # calculem el valor de la theta i lindex de la variable de sortida

        #p = self.trobar_p(db) 

        entra = self.N[q] # id variable d'entrada
        surt = self.B[p] # id variable de sortida

        self.B[p] = entra # actualitzem B
        self.N[q] = surt # actualitzem N

        self.N.sort()

        index_cn = next(i for i in range(len(self.N)) if self.N[i] == surt)

        if self.c[self.N[q]-1]!=0: # si el coeficient de la variable que ha entrat en les no bàsiques és diferent de 0
            self.Cn[index_cn] = self.c[self.N[q]-1] # actualitzem vector cn amb el coeficient en la funcio objectiu de la variable que entra en N
        else:
            self.Cn[index_cn] = 0

        self.actualitzar(theta, p, rq, q)

    def actualitzar(self, theta, p, rq, q):
        
        columna_entra = self.restriccions[:, self.B[p]-1]
        self.mB[:, p]=columna_entra
        
        columnes_de_indexs =[]
        for index in self.N:
            columna = self.restriccions[:,index-1]
            columnes_de_indexs.append(columna)
            
        self.An = np.column_stack(columnes_de_indexs)
        
        #actualitzar inversa
        
        mB_inv = np.linalg.inv(self.mB)
        self.Xb = np.dot(mB_inv,self.b)
        
        self.z = self.z + (theta*rq)
        
        if self.c[self.B[p]-1]!=0:
            self.Cb[p] = self.c[self.B[p]-1]
        else :
            self.Cb[p] = 0
        
        self.Cn = []
        for index in self.N:
            if self.c[index-1]!=0:
                self.Cn.append(self.c[index-1])
            else:
                self.Cn.append(0)
        self.Cn = np.array(self.Cn)
        
        with open('sortida.txt', 'a') as sortida:
            print("Iteració ", self.i," : q = ", q,", B[p] = ", p,", theta*=", round(theta,3),", z = ",round(self.z,3))

        if self.positius(self.Xb):
            
           self.i += 1
           self.es_optim()

    def primer_negatiu(self,r):

        for i in range(len(r)):
            if r[i] < 0:
                return i
        return None
    
    def trobar_Aq(self, q):

        Aq = []

        for fila in self.An:
            Aq.append(fila[q])

        return np.array(Aq)

    def calcular_0_p(self,db):
        
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

    
    def base_B_N(self):
                    
        return  self.B, self.N, self.i
        
    def optim(self):
        
        return self.B, self.Xb, self.z, self.r, self.i


class Simplex:
    
    def __init__(self, c, b, A):
        self.c = np.array(c)
        self.b = np.array(b)
        self.A = np.array(A)
        self.i = 0
        
        with open('sortida.txt', 'w') as sortida:
            
            print("Inici simplex primal amb regla de Bland")

        self.fase1()
        
    def fase1(self):
        with open('sortida.txt', 'a') as sortida:
            print("Fase I", file=sortida)
            
        c = [0] * len(self.c) + [1] * len(self.b)
        A = np.hstack((self.A, np.eye(len(self.b))))
        B = list(range(len(self.c) + 1, len(c)+1))
        N = list(range(1,len(self.c)+1))
        indexs = B.copy()
        
        self.B, self.N, self.i =  Iteracions(c, self.b, A, B, N, self.i).base_B_N()
 
        if self.no_tenen_valor(indexs):

            for _ in range(len(self.B)): 
                self.N.pop()

            self.fase2()
        
    def fase2(self):
        with open('sortida.txt', 'a') as sortida:
            print("Fase II", file=sortida)
            
        self.B, self.Xb, self.z, self.r, self.i =Iteracions(self.c, self.b, self. A, self.B, self.N, self.i).optim()
        with open('sortida.txt', 'a') as sortida:
            print("Solució òptima trobada, iteració = ", self.i-1,", z = ", round(self.z,3))
            print("Fi simplex primal")
        
        self.solucio()
        
    def no_tenen_valor(self,indexs):
        
        for valor in indexs:
            
            if valor in self.B:

                return False
            
        return True
    
    def solucio(self):
        
        with open('sortida.txt', 'a') as sortida:
            print("\nSolució òptima: \n")
        
            Vb = ' '.join(str((numero)) for numero in self.B)
            print("Vb = ", Vb)
        
            Xb = ' '.join(str(round(numero,2)) for numero in self.Xb)
            print("xb = ", Xb)
            print("z = ", round(self.z,3))
            r = ' '.join(str(round(numero,2)) for numero in self.r)
            print("r = ", r)


"""Simplex([-28, -65, -48, -75, 91, 42, -39, -31, 15, 36, -10, -27, -100, -11, 0, 0, 0, 0, 0, 0], [338, 294, 54, 252, 1009, 404, 162, 143, 148, 65],[
    [-52, -99, 81, 99, 66, 0, -38, 70, 53, 77, -54, 99, 4, 32, 0, 0, 0, 0, 0, 0],
    [-76, -23, 16, 75, -9, 95, 29, 97, -3, 36, 85, -45, -70, 87, 0, 0, 0, 0, 0, 0],
    [91, 4, -42, 55, 22, 53, -100, -82, -44, 5, -4, 83, -29, 42, 0, 0, 0, 0, 0, 0],
    [-26, 64, 90, 76, -6, -21, -56, -40, 58, 35, 31, 88, 25, -66, 0, 0, 0, 0, 0, 0],
    [69, 69, 84, 90, 57, 61, 80, 71, 78, 82, 66, 61, 77, 63, 1, 0, 0, 0, 0, 0],
    [92, 33, -14, 83, 9, 78, 66, 20, 14, 55, -96, -51, 17, 99, 0, -1, 0, 0, 0, 0],
    [-90, 66, -15, 18, -20, -99, 21, 77, 99, 63, -68, -49, 59, 99, 0, 0, 1, 0, 0, 0],
    [-14, 99, -67, 88, 68, -39, -29, 82, 99, 1, 25, -89, -67, -15, 0, 0, 0, 1, 0, 0],
    [93, -15, 22, 86, -82, -94, 39, -26, 65, -3, -7, -40, 66, 43, 0, 0, 0, 0, 1, 0],
    [45, -17, 88, -79, 40, -7, -6, -45, 75, 51, -20, -89, 24, 6, 0, 0, 0, 0, 0, -1]
])"""

