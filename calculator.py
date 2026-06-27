#!/usr/bin/env python3
import math
import sys

# Handle UTF-8 BOM when input is piped (e.g. from PowerShell)
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8-sig")


class History:
    def __init__(self):
        self._entries: list[tuple[str, str]] = []

    def add(self, expr: str, result: str) -> None:
        self._entries.append((expr, result))

    def clear(self) -> None:
        self._entries.clear()

    def entries(self) -> list[dict]:
        return [{"expr": e, "result": r} for e, r in self._entries]

    def display(self) -> None:
        if not self._entries:
            print("  (no history)")
            return
        for i, (expr, result) in enumerate(self._entries, 1):
            print(f"  {i:4}.  {expr}  =  {result}")


class Calculator:
    _NAMESPACE = {
        "__builtins__": {},
        # Built-ins
        "abs": abs,
        "round": round,
        "pow": pow,
        # Trig — radians
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "atan2": math.atan2,
        # Trig — degrees
        "sind": lambda x: math.sin(math.radians(x)),
        "cosd": lambda x: math.cos(math.radians(x)),
        "tand": lambda x: math.tan(math.radians(x)),
        "asind": lambda x: math.degrees(math.asin(x)),
        "acosd": lambda x: math.degrees(math.acos(x)),
        "atand": lambda x: math.degrees(math.atan(x)),
        # Roots & powers
        "sqrt": math.sqrt,
        "cbrt": math.cbrt,
        # Logarithms & exponentials
        "log": math.log,
        "log2": math.log2,
        "log10": math.log10,
        "exp": math.exp,
        # Rounding
        "ceil": math.ceil,
        "floor": math.floor,
        # Combinatorics
        "factorial": math.factorial,
        "gcd": math.gcd,
        # Constants
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
        "inf": math.inf,
    }

    def evaluate(self, expr: str):
        code = compile(expr, "<input>", "eval")
        return eval(code, self._NAMESPACE, {})

    def format_result(self, value) -> str:
        if isinstance(value, float):
            if math.isnan(value):
                return "nan"
            if math.isinf(value):
                return "inf" if value > 0 else "-inf"
            if value.is_integer() and abs(value) < 1e15:
                return str(int(value))
            return f"{value:.10g}"
        return str(value)


class REPL:
    HELP = """
  OPERATORS
    +   addition        (e.g. 3 + 5)
    -   subtraction     (e.g. 10 - 4)
    *   multiplication  (e.g. 6 * 7)
    /   division        (e.g. 9 / 2)
    **  power           (e.g. 2 ** 8)
    %   modulo          (e.g. 17 % 5)
    //  floor division  (e.g. 7 // 2)

  SCIENTIFIC FUNCTIONS
    sqrt(x)           square root        (e.g. sqrt(16))
    cbrt(x)           cube root          (e.g. cbrt(27))
    pow(x, y)         x to the power y   (e.g. pow(2, 10))
    exp(x)            e^x                (e.g. exp(1))
    log(x)            natural log        (e.g. log(e))
    log(x, base)      log with base      (e.g. log(8, 2))
    log2(x)           log base 2
    log10(x)          log base 10
    factorial(n)      n!                 (e.g. factorial(6))
    gcd(a, b)         greatest common divisor

  TRIG (radians)
    sin(x)  cos(x)  tan(x)
    asin(x) acos(x) atan(x)  atan2(y, x)

  TRIG (degrees)
    sind(x)  cosd(x)  tand(x)
    asind(x) acosd(x) atand(x)

  ROUNDING
    abs(x)        absolute value
    ceil(x)       round up
    floor(x)      round down
    round(x, n)   round to n decimal places

  CONSTANTS
    pi    3.14159...
    e     2.71828...
    tau   6.28318...
    inf   infinity

  COMMANDS
    history   show calculation history
    clear     clear history
    help      show this help
    quit      exit
"""

    def __init__(self):
        self.calculator = Calculator()
        self.history = History()

    def run(self) -> None:
        print("Scientific Calculator  |  type 'help' for reference, 'quit' to exit")
        print("-" * 60)

        while True:
            try:
                raw = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                sys.exit(0)

            if not raw:
                continue

            self._dispatch(raw)

    def _dispatch(self, raw: str) -> None:
        lower = raw.lower()
        if lower in ("quit", "exit", "q"):
            print("Bye!")
            sys.exit(0)
        elif lower == "help":
            print(self.HELP)
        elif lower == "history":
            self.history.display()
        elif lower in ("clear", "clr"):
            self.history.clear()
            print("  History cleared.")
        else:
            self._evaluate(raw)

    def _evaluate(self, expr: str) -> None:
        try:
            value = self.calculator.evaluate(expr)
            result = self.calculator.format_result(value)
            print(f"  = {result}")
            self.history.add(expr, result)
        except ZeroDivisionError:
            print("  Error: division by zero")
        except ValueError as exc:
            print(f"  Error: {exc}")
        except SyntaxError:
            print("  Error: invalid expression — type 'help' for syntax reference")
        except NameError as exc:
            print(f"  Error: {exc} — type 'help' for available functions")
        except Exception as exc:
            print(f"  Error: {exc}")


if __name__ == "__main__":
    REPL().run()
