
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
        self.z = len(b)
        
        self.trobar_SBF()
        

    def trobar_SBF(self):

        mB_inv = np.linalg.inv(self.mB)
        Cb_mB_inv = np.dot(self.Cb, mB_inv)
        Cb_mB_inv_An = np.dot(Cb_mB_inv, self.An)
        r = self.Cn - Cb_mB_inv_An

        if self.positius(r):

            return 
        
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

        
        if self.positius(db):

            return
        
        o = self.calcular_0(db)

        p = self.trobar_p(db)
        
        entra = self.N[q]
        surt = self.B[p]

        self.B[p] = entra
        self.N[q] = surt

        self.N.sort()
        
        self.actualitzar(o, db, entra)

    def actualitzar(self, o, db, rq):
        
        self.z = self.z + (o*rq)
        


    def primer_negatiu(self,r):

        for i in range(len(r)):
            if r[i] < 0:
                return i
        return None
    
    def trobar_Aq(self, q):

        Aq = []

        for fila in self.restriccions:
            Aq.append(fila[q])

        return Aq

    def calcular_0(self,db):
        
        llista_min = []

        for i in range(len(self.b)):

            llista_min.append(-self.b[i]/db[i])

        minim = min(llista_min)

        return minim


    def trobar_p(self, db):

        llista_min = []

        for i in range(len(self.b)):

            llista_min.append(-self.b[i]/db[i])

        minim = min(llista_min)
        p = llista_min.index(minim)
        
        return p
    


Fase1([1, 1, 0],[4,2],[[1, 1, 1],[2, -1, 0]])