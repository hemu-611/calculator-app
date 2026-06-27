from calculator import Calculator

calc = Calculator()


def test_addition():
    assert calc.format_result(calc.evaluate("3 + 5")) == "8"

def test_operator_precedence():
    assert calc.format_result(calc.evaluate("3 + 5 * 2")) == "13"

def test_sqrt():
    assert calc.format_result(calc.evaluate("sqrt(144)")) == "12"

def test_power():
    assert calc.format_result(calc.evaluate("2 ** 10")) == "1024"

def test_trig_degrees():
    result = float(calc.format_result(calc.evaluate("sind(90)")))
    assert abs(result - 1.0) < 1e-9

def test_division():
    assert calc.format_result(calc.evaluate("9 / 2")) == "4.5"

def test_floor_division():
    assert calc.format_result(calc.evaluate("7 // 2")) == "3"

def test_factorial():
    assert calc.format_result(calc.evaluate("factorial(6)")) == "720"

def test_division_by_zero():
    try:
        calc.evaluate("1 / 0")
        assert False, "should raise"
    except ZeroDivisionError:
        pass
