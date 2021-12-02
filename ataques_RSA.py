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
    def __init__(self,N, e):
        self.N = N
        self.e = e
        '''if (gcd((p-1)*(q-1), e) != 1):
            print('e ruim')'''

    def força_bruta(self):
        ''' Roda rápido se N = 1039*58484513 = 60.765.409.007; e = 7 '''
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
        ''' Roda rápido se N = 58484519*58484513=3420438611754247; e = 3'''
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
        '''Roda rápido se N = 98484527*58484519 = 5759820190537513, e = 3839880022378979'''
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
                if sq_delta**2 == delta and (sq_delta - b) % 2 == 0:
                    r1 = (sq_delta - b) // 2
                    r2 = (-sq_delta - b) // 2
                    if r1 != 1 and r2 !=N:
                        print(f'k: {k}\nd: {d}\nphi: {phi}')
                        return (sq_delta - b) // 2, (-sq_delta - b) // 2
            k, d = next(frac)
        print('Falhamos!')

    def pollard_p_menos_1(self, mudar_B = 500):
        '''Roda rápido se N = 39916801*33322727=1330136662436327; e = 13 '''
        N = self.N
        B = floor(N**0.22)
        mult = 1.3
        k = lcm_range(B)
        for _ in range(mudar_B):
            for _ in range(10):
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

    def ECM(self, tentativas=50, B=33):
        '''Roda rápido se N = 39916801*33322727=1330136662436327; e = 13 '''
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
        for _ in range(tentativas):
            a = random.randint(1, N)
            x = random.randint(1, N)
            y = random.randint(1, N)
            b = (y**2 - x**3 - a*x) % N
            P = (x, y)
            BP = P #No final do loop BP = B! P
            if gcd(4 * a ** 3 + 27 * b ** 2, N) == 1:
                for i in range(2,B+1): #em cada loop vamos obter i! P
                    Q = BP
                    binario_i = bin(i)[2:]
                    numero_de_somas = len(binario_i)
                    for j in range(numero_de_somas):
                        if j != 0:
                            Q = soma_E(Q, Q, a, b, N)
                            if isinstance(Q, int):
                                return (N // Q, Q)
                        if binario_i[-j - 1] == '1':
                            BP = soma_E(BP, Q, a, b, N)
                            if isinstance(BP, int):
                                return (N//BP, BP)
                        
            elif gcd(4 * a ** 3 + 27 * b ** 2, N) != 1:
                return gcd(4 * a ** 3 + 27 * b ** 2, N)
                
if __name__ == '__main__':
    print('Ataques ao RSA v1.0')
    print('Escolhar um ataque: ')
    print('[1] Força Bruta')
    print('[2] Ataque de Fermat')
    print('[3] Ataque de Wiener')
    print('[4] Ataque p-1 de Pollar')
    print('[5] ECM')
    escolha = 0
    while escolha not in {1,2,3,4,5}:
        escolha = int(input('Digite o número: '))
    
    print('Chave pública: ')
    N = int(input('Valor de N: '))
    e = int(input('Valor de e: '))
    
    ataque = Ataque(N,e)
    
    if escolha == 1:
        print('Executando...')
        t_inicio = time.perf_counter()
        print(ataque.força_bruta())
        t_fim = time.perf_counter()
        print(f'Executado em {t_fim-t_inicio} segundos')
    elif escolha == 2:
        print('Executando...')
        t_inicio = time.perf_counter()
        print(ataque.fermat())
        t_fim = time.perf_counter()
        print(f'Executado em {t_fim-t_inicio} segundos')
    elif escolha == 3:
        print('Executando...')
        t_inicio = time.perf_counter()
        print(ataque.wiener())
        t_fim = time.perf_counter()
        print(f'Executado em {t_fim-t_inicio} segundos')
    elif escolha == 4:
        mudar_B = input('Número de tentativas que você está disposto (digte nada e aperte enter se quiser a nossa recomendação): ')
        print('Executando...')
        t_inicio = time.perf_counter()
        if mudar_B == '':
            print(ataque.pollard_p_menos_1())
        else:
            print(ataque.pollard_p_menos_1(mudar_B = int(mudar_B)))
        t_fim = time.perf_counter()
        print(f'Executado em {t_fim-t_inicio} segundos')
    elif escolha ==5:
        tentativas = input('Número de tentativas que você está disposto (digte nada e aperte enter se quiser a nossa recomendação): ')
        B = input('Valor de B (digte nada e aperte enter se quiser a nossa recomendação): ')
        print('Executando...')
        if B == '' and tentativas == '':
            t_inicio = time.perf_counter()
            print(ataque.ECM())
        elif B == '':
            t_inicio = time.perf_counter()
            print(ataque.ECM(tentativas = int(tentativas)))  
        elif tentativas == '':
            t_inicio = time.perf_counter()
            print(ataque.ECM(B = int(B)))
        else:
            t_inicio = time.perf_counter()
            print(ataque.ECM(tentativas = int(tentativas), B = int(B)))   
        t_fim = time.perf_counter()
        print(f'Executado em {t_fim-t_inicio} segundos')
