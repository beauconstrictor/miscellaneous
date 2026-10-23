import tkinter as tk
from math import isqrt
from random import randint
from enum import Enum, auto
from tkinter import messagebox
from collections import defaultdict
from typing import Iterator, Literal

SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

MIN, MAX = 10, 1000

# isqrt(1000) is 31, so we don't need to go any higher than that
# (1000) is the highest number we can get here
RULES = "  " + """
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

class StepStatus(Enum):
    FOUND       = "factor found."
    FINISHED    = "all factors found!"
    NOT_PRIME   = "that number is not prime."
    NOT_FACTOR  = "that number is not a factor."
    ONE_IS_BAD  = "your guess must be greater than 1"
    NOT_NATURAL = "your guess must be greater than 1"

class Game:
    def __init__(self) -> None:
        self.start_game()

    def start_game(self) -> None:
        self.n = randint(MIN, MAX)
        self.factors = defaultdict(int)
        self.remainder = self.n
        self.last_status = None

    def _step(self, factor: int) -> StepStatus:
        if factor <= 0:
            return StepStatus.NOT_NATURAL
        if factor == 1:
            return StepStatus.ONE_IS_BAD
        if self.remainder % factor != 0:
            return StepStatus.NOT_FACTOR
        if not is_prime(factor):
            return StepStatus.NOT_PRIME

        self.factors[factor] += 1
        self.remainder //= factor

        if self.remainder == 1:
            return StepStatus.FINISHED
        return StepStatus.FOUND

    def step(self, factor: int) -> StepStatus:
        self.last_status = self._step(factor)
        return self.last_status

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.game = Game()

        self.sqrt_on  = False
        self.rules_on = False

        self.title("Prime Factorisation Practice")
        self.resizable(False, False)
        
        self.remainder = tk.Label(self, text=str(self.game.n))
        self.factors   = tk.Label(self, text=f"")
        self.remainder.grid(row=0, column=0, columnspan=2)
        self.factors.grid(row=1, column=0, columnspan=2)

        self.entry     = tk.Entry(self)
        self.entry_lbl = tk.Label(self, text="Enter a prime factor: ")
        self.entry_lbl.grid(row=2, column=0)
        self.entry.grid(row=2, column=1)
        self.entry.bind("<Return>", self.step)

        self.sqrt_btn = tk.Button(self, text="Show √", command=self.toggle_sqrt)
        self.sqrt_lbl = tk.Label(self, text="")
        self.sqrt_btn.grid(row=3, column=0)
        self.sqrt_lbl.grid(row=3, column=1)

        self.rules_btn = tk.Button(self, text="Show Hints", command=self.toggle_rules)
        self.rules_lbl = tk.Text(self, width=71, height=14)
        self.rules_btn.grid(row=4, column=0, columnspan=2)
        self.rules_lbl.grid(row=5, column=0, columnspan=2)

        self.draw()

    def toggle_sqrt(self) -> None:
        self.sqrt_on = not self.sqrt_on
        self.draw()

    def toggle_rules(self) -> None:
        self.rules_on = not self.rules_on

        if self.rules_on:
            self.rules_lbl.insert("1.0", RULES)
        else:
            self.rules_lbl.delete("1.0", tk.END)

    def draw(self) -> None:
        self.remainder.config(text=str(self.game.remainder))
        if self.game.factors:
            self.factors.config(text=f"{self.game.n} = {self.game.remainder} × {show_prime_factorisation(self.game.factors)}")
        else:
            self.factors.config(text="")

        if self.sqrt_on:
            self.sqrt_lbl.config(text=f"⌊√{self.game.remainder}⌋ = {isqrt(self.game.remainder)}")
        else:
            self.sqrt_lbl.config(text="")

    def step(self, _) -> None:
        try:
            factor = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Not a number", "You must enter a number")
            return

        self.entry.delete(0, tk.END)

        match self.game.step(factor):
            case StepStatus.FINISHED:
                self.draw()
                self.update()
                if messagebox.askyesno("Success!", "Play again?"):
                    self.game.start_game()
                    self.draw()
                else:
                    self.destroy()
            case StepStatus.FOUND:
                pass
            case _:
                messagebox.showerror("Failed", self.game.last_status.value.capitalize())

        self.draw()

if __name__ == "__main__":
    App().mainloop()
