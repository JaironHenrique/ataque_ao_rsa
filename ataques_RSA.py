from math import floor, gcd, log, isqrt
import sympy
import random
import time

lcm_dict = {}
p = []
def lcm_range(B):
    if B < 3: return B
    if B - (B+1)%2 in lcm_dict: return lcm_dict[B - (B+1)%2]
    if p:
        start = p[-1]
        lcm = lcm_dict[start]
    else:
        start = 3
        lcm = 2**floor(len(bin(B))-3)
    for i in range(start, B + 1, 2):
        if all(i % j for j in p):
            p.append(i)
            lcm *= i ** floor(log(B, i))
        lcm_dict[i] = lcm
    return lcm


class Ataque:
    def __init__(self, p, q, e):
        self.N = p*q
        self.e = e
        if (gcd((p-1)*(q-1), e) != 1):
            print('e ruim')

    def força_bruta(self):
        ''' Roda rápido se N = 1039, 58484513; e = 7 '''
        N = self.N
        if N%2 == 0:
            return 2, N//2
        c = isqrt(N)
        for t in range(3, c+1, 2):
            if N%t == 0:
                return t, N//t
        print("N é primo!")
        return N, 1

    def fermat(self):
        ''' Roda rápido se N = 58484519, 58484513; e = 3'''
        N = self.N
        if N % 2 == 0:
            return 2, N//2
        x = isqrt(N)
        if N%x == 0:
            return x, N//x
        for i in range(x + 1, 1 + (N+1)//2):
            val = i**2 - N
            y = isqrt(val)
            if y**2 == val:
                return i - y, i + y
        print("N é primo!")
        return N, 1

    def wiener(self):
        '''Roda rápido se N = 98484527, 58484519, e = 3839880022378979'''
        N = self.N
        e = self.e
        def convergentes(numerador, denominador):
            h, k, h_, k_ = 0, 1, 1, 0
            while True:
                an = denominador // numerador
                h, k, h_, k_ = an*h + h_, an*k + k_, h, k
                yield h, k
                denominador, numerador = numerador, denominador % numerador

        frac = convergentes(e, N)
        k, d = next(frac)
        while (k, d) != (e, N):
            if (e * d - 1)%k == 0:
                phi = (e * d - 1) // k
                b = - N + phi - 1
                delta = b**2 - 4*N
                sq_delta = isqrt(max(0,delta))
                if sq_delta**2 == delta:
                    print(f'k: {k}\nd: {d}\nphi: {phi}')
                    return (sq_delta - b) // 2, (-sq_delta - b) // 2
            k, d = next(frac)
        print('Falhamos!')

    def pollard_p_menos_1(self, mudar_B = 500):
        N = self.N
        B = floor(N**0.22)
        mult = 1.3
        k = lcm_range(B)

        for _ in range(mudar_B):
            for _ in range(3):
                a = random.randint(2, N)
                a = pow(a,k,N)
                f = gcd(a-1,N) # b grande: a=1, f=N // b peq, a=?, f=1
                if f != 1 and f !=N:
                    return (f, N//f) # se ultimo valor de a for 1, diminuir o b
            if a == 1:
                B //= mult
            else:
                B *= mult
                B = int(B)
            k = lcm_range(B)
        print('falhamos!')

    def ECM(self, tentativas=1, B=100):
        def soma_E(P: tuple, Q: tuple, a: int, b: int, N: int):
            if P == 'O':
                return Q
            if Q == 'O':
                return
            if P == Q:
                u = (3 * P[0] ** 2 + a) % N
                v = (2 * P[1]) % N
            else:
                u = (Q[1] - P[1]) % N
                v = (Q[0] - P[0]) % N
            if v == 0:
                return 'O'
            try:
                inv_v = sympy.mod_inverse(v, N)
            except ValueError:
                return gcd(N, v)
            lam = u * inv_v
            x = (lam**2 - P[0] - Q[0]) % N
            y = (lam*(P[0] - x) - P[1]) % N
            return x, y

        N = self.N
        k = lcm_range(B)
        binario_k = bin(k)[2:]
        numero_de_somas = len(binario_k)
        for _ in range(tentativas):
            a = random.randint(2, N)
            x = random.randint(2, N)
            y = random.randint(2, N)
            b = y**2 - x**3 - a*x
            P = (x, y)
            Q = P
            if binario_k[-1] == '0':
                KP = 'O'
            else:
                KP = P
            # print(KP)
            if gcd(4 * a ** 3 + 27 * b ** 2, N) == 1:
                for i in range(numero_de_somas - 1):
                    Q = soma_E(Q, Q, a, b, N)
                    # print(i,Q)
                    if isinstance(Q, int):
                        return (N // Q, Q)
                    if binario_k[-i - 2] == '1':
                        KP = soma_E(KP, Q, a, b, N)
                        # print(KP)
                    if isinstance(KP, int):
                        return (N//KP, KP)
        print('falhamos')



x = Ataque(2684093, 367004581, 7)
#print(x.força_bruta())
#print(x.fermat())
#print(x.wiener())
s = time.perf_counter()
#(x.fermat())
#x.wiener()
(x.pollard_p_menos_1())
#x.força_bruta()
e = time.perf_counter()
print(e-s)


