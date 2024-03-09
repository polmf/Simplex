
import numpy as np



class Fase1:

    def __init__(self, c, b, A):
        
        self.funcio_objectiu = [0] * len(c) + [1] * len(b)
        self.b = b
        self.restriccions = np.hstack((A, np.eye(len(self.b))))
        self.B = list(range(len(c) + 1, len(self.funcio_objectiu)+1))
        self.N = list(range(1,len(c)+1))
        self.Cb = np.array([1] * len(self.b))
        self.Cn = np.array([0] * len(c))
        self.Xb = b
        self.Xn = [0]*len(c)
        self.An = np.array(A)
        self.mB = np.eye(len(self.b))
        self.z = np.dot(self.Cb,self.Xb)
        
        self.es_optim()
        

    def es_optim(self):

        mB_inv = np.linalg.inv(self.mB)
        Cb_mB_inv = np.dot(self.Cb, mB_inv)
        Cb_mB_inv_An = np.dot(Cb_mB_inv, self.An)
        r = self.Cn - Cb_mB_inv_An
         
        if self.positius(r):

            self.resultat()
        else:
            self.canviar_base(r)


    def positius(self, r):

        for element in r:
            if element < 0:
                return False
        return True
    
    def canviar_base(self,r):

        q = self.primer_negatiu(r)
        mB_inv = np.linalg.inv(self.mB)
        db = np.dot(-(mB_inv),self.trobar_Aq(q))
        
        rq= r[q]
        
        if self.positius(db):

           print(1)
        
        o = self.calcular_0(db)

        p = self.trobar_p(db)
        
        entra = self.N[q]
        surt = self.B[p]

        self.B[p] = entra
        self.N[q] = surt

        if self.funcio_objectiu[self.N[q]-1]!=0:
            self.Cn[q] = self.funcio_objectiu[self.N[q]-1]
        else:
            self.Cn[q] = 0

        self.N.sort()
        self.actualitzar(o, p, rq)

    def actualitzar(self, o, p, rq):
        
        columna_entra = self.restriccions[:, self.B[p]-1]
        self.mB[:, p]=columna_entra
        
        columnes_de_indexs =[]
        for index in self.N:
            columna = self.restriccions[:,index-1]
            columnes_de_indexs.append(columna)
            
        self.An = np.column_stack(columnes_de_indexs)
        
        mB_inv = np.linalg.inv(self.mB)
        self.Xb = np.dot(mB_inv,self.b)
        
        self.z = self.z + (o*rq)
        
        if self.funcio_objectiu[self.B[p]-1]!=0:
            self.Cb[p] = self.funcio_objectiu[self.B[p]-1]
        else :
            self.Cb[p] = 0
        
        self.Cn = []
        for index in self.N:
            if self.funcio_objectiu[index-1]!=0:
                self.Cn.append(self.funcio_objectiu[index-1])
            else :
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

    def calcular_0(self,db):
        
        llista_min = []

        for i in range(len(self.b)):
            
            if db[i]<0:
            
                llista_min.append(-self.Xb[i]/db[i])

        minim = min(llista_min)

        return minim


    def trobar_p(self, db):

        llista_min = []

        for i in range(len(self.b)):
            
            if db[i]<0:
            
                llista_min.append(-self.Xb[i]/db[i])

        minim = min(llista_min)
        p = llista_min.index(minim)
        
        return p
    
    def resultat(self):
        
        print(self.z)
        print(self.B)
        print(self.N)
        return

Fase1([-1, 0, 0],[4,2],[[1, 1, 1],[2, -1, 0]])