
import numpy as np



class Fase1:

    def __init__(self, c, b, A):
        
        """Inicialitzem els valors que necessitarem en la fase1
        """
        
        self.c = [0] * len(c) + [1] * len(b) # nous coeficients en la funcio objectiu
        self.b = b # resultats restriccions
        self.restriccions = np.hstack((A, np.eye(len(self.b)))) # resulta una matriu amb els coeficients de les variables en les restriccions
        self.B = list(range(len(c) + 1, len(self.c)+1)) # inicialitzem els indexs de les variables bàsiques amb les noves dos variables artificials
        self.N = list(range(1,len(c)+1)) # inicialitzem els indexs de les variables no bàsiques amb les variables originals en forma estandar
        self.Cb = np.array([1] * len(self.b)) # coeficients de les variables bàsiques en la funció objectiu
        self.Cn = np.array([0] * len(c)) # coeficients de les variables no bàsiques en la funció objectiu
        self.Xb = b # resultat de calcular la Identitat (B^-1) x b
        self.Xn = [0]*len(c) # sempre han de ser 0 i len(variables no bàsiques)
        self.An = np.array(A) # matriu dels coeficients de les variables no bàsiques en les restriccions
        self.mB = np.eye(len(self.b)) # matriu dels coeficients de les variables bàsiques en les restriccions (amb np.eye posem 1s a la diagonal amb mida 'len(argument) x len(argument)')
        self.z = np.dot(self.Cb,self.Xb) # resultat del producte escalar entre els vectors cb i xb
        
        self.es_optim()
        

    def es_optim(self):

        self.mB_inv = np.linalg.inv(self.mB) # calculem inversa de la matriu B (dels coeficients en restr. de les var. bàsiques)
        Cb_mB_inv = np.dot(self.Cb, self.mB_inv) # producte escalar entre cb i la inversa calculada
        Cb_mB_inv_An = np.dot(Cb_mB_inv, self.An) # calcul de cb x B^-1 x An
        r = self.Cn - Cb_mB_inv_An # calcul final del cost reduït
         
        if self.positius(r): # si r és positiu

            self.resultat() 
        
        else:
            self.canviar_base(r)


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

           print('DBF de descenso no acotada, Problema Lineal no acotado')
        
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

        self.actualitzar(theta, p, rq)

    def actualitzar(self, theta, p, rq):
        
        columna_entra = self.restriccions[:, self.B[p]-1]
        self.mB[:, p]=columna_entra
        
        columnes_de_indexs =[]
        for index in self.N:
            columna = self.restriccions[:,index-1]
            columnes_de_indexs.append(columna)
            
        self.An = np.column_stack(columnes_de_indexs)
        
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
        
        if self.positius(self.Xb):
            
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

        for i in range(len(self.b)):
            
            if db[i]<0:
            
                llista_min.append(-self.Xb[i]/db[i])

        minim = min(llista_min)
        p = llista_min.index(minim)

        return minim, p


    """def trobar_p(self, db):

        llista_min = []

        for i in range(len(self.b)):
            
            if db[i]<0:
            
                llista_min.append(-self.Xb[i]/db[i])

        minim = min(llista_min)
        p = llista_min.index(minim)
        
        return p"""
    
    def resultat(self):
        
        print(self.z)
        print(self.B)
        print(self.N)
        return

Fase1([-1, 0, 0],[4,2],[[1, 1, 1],[2, -1, 0]])