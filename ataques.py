# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 10:18:02 2021

@author: Henrique
"""
from math import * 
import sympy

class Ataque:
    def __init__(self, N,e):
        self.N = N
        self.e = e
    
    def força_bruta(self):
        ''' Roda rápido se N = 1039*58484513; e = 7 '''
        N = self.N
        if N % 2 == 0:
            return (2, int(N/2))
        else: 
            t = 3
            while N % t != 0 and t** 2 <= N:
                t += 2
            if N % t == 0:
                return (t, int(N/t))
            else:
                print("N é primo!")
                return (N,1)
            
    def fermat(self):
        ''' Roda rápido se N = 58484519*58484513; e = 3'''
        N = self.N
        if N % 2 == 0:
            return (2, int(N/2))
        else:
            x = floor(sqrt(N)) # trocar para sympy?
            if N % x == 0:
                return (x,int(N/x))
            else:
                while x != (N+1)/2:
                    x += 1
                    y = sympy.sqrt(x**2 - N)
                    if y.is_integer:
                        y = int(y)
                        return (x - y, x+y)
                print("N é primo!")
                return (N,1)
    
    def wiener(self):
        '''Roda rápido se N = 98484527*58484519, e = 3839880022378979'''
        N = self.N
        e = self.e
        def convergentes(numerador, denominador):
            h, k, h_, k_ = 0, 1 , 1, 0
            while True:
                an = denominador // numerador
                h, k, h_, k_ = an*h + h_, an*k + k_, h, k
                yield h,k
                denominador, numerador = numerador, denominador % numerador
        
        x = sympy.symbols('x')
        frac = convergentes(e,N)
        k, d = next(frac)
        while (k, d) != (e,N):
            phi = (e*d - 1)/k # trocar para sympy?
            phi = float(phi)
            if phi.is_integer():
                phi = int(phi)
                soluções = tuple(map(int,list(sympy.solveset(x**2 - (N - phi + 1)*x + N, domain = sympy.S.Integers))))
                if soluções != ():
                    print(' k: ', k, '\n d: ', d,'\n phi: ', phi)
                    return soluções
            k , d = next(frac)
        print('Falhamos!')
        


        