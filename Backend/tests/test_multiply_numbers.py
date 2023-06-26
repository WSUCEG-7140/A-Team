from ..multiply_numbers import multiply_numbers

def test_multiply_positive_numbers():
    result = multiply_numbers(3, 4)
    assert result == 12

def test_multiply_negative_numbers():
    result = multiply_numbers(-2, 5)
    assert result == -10

def test_multiply_zero():
    result = multiply_numbers(10, 0)
    assert result == 0