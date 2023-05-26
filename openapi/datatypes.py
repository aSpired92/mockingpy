import re
import string
import sys
from _decimal import Decimal


class _OAType:
    """
    Bazowy typ openapi. Kolejne klasy będą zawierały walidację danych odpowiednich dla danego typu
    """

    def __init__(self, value):
        self.value = value


class _OATypeNumeral(_OAType):
    """
    Numeryczny typ openapi. Sprawdza, czy wpisana wartość nie wykracza poza zakres typu ('min', 'max').
    Zakres jest opisany na typie 'Decimal' w celu zachowania dokładności
    """

    min = None
    max = None

    def __init__(self, value):
        if self.min and self.max:
            if not self.min < value < self.max:
                raise RuntimeError(f'limit reached: {value} ({self.min}, {self.max})')
        super().__init__(value)


class _OATypeText(_OAType):
    """
    Typ tekstowy. Sprawdza, czy wpisana wartość jest poprawna względem formułki 'regex' i czy
    zawiera litery wyłącznie z podanego alfabetu
    """

    regex = None
    characters = string.printable

    def __init__(self, value):
        if set(value) > set(self.characters):
            raise RuntimeError(f'Value does not match allowed characters')
        if self.regex:
            if not re.match(self.regex, value):
                raise RuntimeError(f'Value does not match format')
        super().__init__(value)


class String(str, _OATypeText):
    pass


class Date(String):
    regex = r"^\d{4}-\d{2}-\d{2}$"


class DateTime(String):
    regex = r"^(?:\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?)(?:Z|[\+-]\d{2}:\d{2})?$"


class Password(String):
    pass


class Byte(String):
    regex = r"^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/][AQgw]==|[A-Za-z0-9+\/]{2}[AEIMQUYcgkosw048]=)?$"


class Binary(String):
    regex = r"^[0*1*][1*0*]*$"


class Number(float, _OATypeNumeral):
    min = Decimal(sys.float_info.min)
    max = Decimal(sys.float_info.max)


class Integer(int, _OATypeNumeral):
    min = Decimal(-sys.maxsize - 1)
    max = Decimal(sys.maxsize)


class Int32(Integer):
    min = Decimal('-2147483648')
    max = Decimal('2147483647')


class Int64(Integer):
    min = Decimal('-9223372036854775808')
    max = Decimal('9223372036854775807')


class Float(Number):
    min = Decimal('-3.402823466E+38')
    max = Decimal('3.402823466E+38')


class Double(Number):
    min = Decimal('-1.7976931348623158E+308')
    max = Decimal('1.7976931348623158E+308')





