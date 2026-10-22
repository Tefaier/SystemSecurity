from pwn import *
from math import gcd
from Crypto.Util.number import long_to_bytes, inverse
import re

n0 = 0
e  = 0
c0 = int("", 16)
n1 = 0

# Recover the shared prime factor.
p  = gcd(n0, n1)
q0 = n0 // p

phi0 = (p - 1) * (q0 - 1)
d0   = inverse(e, phi0)

m = pow(c0, d0, n0)
print(long_to_bytes(m))