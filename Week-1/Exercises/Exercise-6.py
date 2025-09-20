"""
Write a script that lists all the prime numbers between 1 and 10000.
(A prime number is an integer greater or equal to 2 which has no divisors except 1 and itself). 
Hint: Write an is_factor helper function.
"""

def is_factor(d, n):
    """True iff (if and only if) d is a divisor of n."""
    return True if n % d == 0 else False

def is_prime(n):
    prime = True
    if n == 1:
        prime = False
    else:
        for i in range(2, int(n**0.5+1)):
            if is_factor(i, n):
                prime = False
                break
    return prime

def find_primes(lowerbound, upperbound):
    return [n for n in range(lowerbound, upperbound + 1) if is_prime(n)]

list_of_primes = find_primes(1, 10000)
print(list_of_primes)