from fraction import gcd
from random import randint
from constants import *

def get_sieve(N):
    prime = [1] * (N + 1)
    prime[0] = 0
    prime[1] = 0
    for i in range(N + 1):
        if prime[i]:
            for j in range(i * 2, N + 1, i):
                prime[j] = 0
    primes = []
    for i in range(N + 1):
        if prime[i]:
            primes.append(i)

    return primes

def generate_permutation_hash_functions( length, count ):
    primes = get_sieve(100000))
    next = 0

    hash_functions = []
    for x in range(count):
        while gcd(length, primes[next]) != 1:
            next += 1
        hash_functions.append( { 'a' : primes[next] , 'b' : randint(0, length) }
        next += 1

    return hash_functions

def xor_range_hasher(length):
    curr = 1
    while curr < length:
        curr <<= 1

    #partition 0 .. curr into segments
    func = lambda x : ( x * NUM_HASH_FUNCTIONS ) / curr
    
    return func
