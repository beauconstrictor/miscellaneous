from math import isqrt
from random import randint
from typing import Iterator
from collections import defaultdict

SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

# isqrt(1000) is 31, so we don't need to go any higher than that
# (1000) is the highest number we can get here
RULES = """
2.  final digit is 0, 2, 4, 6 or 8
3.  sum of digits is divisible by 3
5.  final digit is 0 or 5
--- for these, the 'rest' is the number without its last digit.
--- once you have used the rule, you will get a new number. if that
--- number is divisible by the factor, then so is the original.
7.  subtract twice the last digit from the rest
11. subtract the last digit from the rest
13. subtract 9x the last digit from the rest
17. subtract 5x the last digit from the rest
19. add 2x the last digit to the rest
23. add 7x the last digit to the rest
29. add 3x the last digit to the rest
31. subtract 3x the last digit from the rest
""".strip()

def yesno(s: str) -> bool:
    return input(s + " [Y/n] ").lower().strip() != "n"

# sieve of eratosthenes
def primes(limit: int) -> Iterator[int]:
    if limit < 2: return

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (
                (limit - start) // p + 1)

    yield from (n for n, is_prime in enumerate(sieve) if is_prime)

def is_prime(n: int) -> bool:
    if n < 2: return False

    for p in range(2, isqrt(n) + 1):
        if n % p == 0: return False

    return True

def superscript(n: int) -> str:
    return str(n).translate(SUPERSCRIPT)

def show_prime_factorisation(counts: dict[int, int]) -> str:
    # ik this is ugly af, but it's fun to write
    return "×".join(f"{f}{superscript(counts[f]) if counts[f] > 1 else ''}" for f in sorted(counts.keys()))

def main() -> None:
    n = randint(10, 1000)

    print("prime factorisation practice!")
    show_sqrt   = yesno("do you want to see the number's square root?")
    show_primes = yesno("do you want a list of useful prime numbers?")
    show_rules  = yesno("do you want to see common divisibility rules?")

    counts = defaultdict(int)
    n_left = n

    if show_rules:
        print("\n" + RULES)

    while n_left > 1:
        if n_left == n:
            print(f"\nyour number is: {n}.")
        else:
            print(f"\nnumber left: {n_left}.")

        print(f"found:", show_prime_factorisation(counts) or "nothing yet")

        if show_sqrt:
            print(f"⌊√{n_left}⌋ = {isqrt(n_left)}")
        if show_primes:
            print("useful primes:")
            for p in primes(isqrt(n_left)):
                print(p)

        try:
            factor = int(input("enter a prime factor: "))
        except ValueError:
            print(f"enter a single number.")
            continue
        if factor < 1 or n_left % factor != 0:
            print(f"{factor} is not a factor of {n_left}.")
            continue
        if not is_prime(factor):
            print(f"{factor} is not prime.")
            continue

        counts[factor] += 1
        n_left //= factor

    print(f"\nwell done! the prime factors of {n} are {show_prime_factorisation(counts)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nbye!")
