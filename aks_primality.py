# Borrowed from Rosettacode: http://rosettacode.org/wiki/AKS_test_for_primes#Python

class AKSPrimalityTest:
    @staticmethod
    def _expand_x_1(n): 
    # This version uses a generator and thus less computations
        c =1
        for i in range(n//2+1):
            c = c*(n-i)//(i+1)
            yield c
    
    @staticmethod
    def isPrime(p):
        if p==2:
            return True
    
        for i in AKSPrimalityTest._expand_x_1(p):
            if i % p:
                # we stop without computing all possible solutions
                return False
        return True