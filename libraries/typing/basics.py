from typing import *
from typing import List, Dict, Set, Optional, Any, Sequence, Tuple, Callable #
# Callabe -> function 

# mainly for documentation for coding


x: str = 1 # the str here does not assign format to 1, just showing what format it should be

def adding(a: int, b: int, c: int) -> int:
    return(a+b+c)

add1 = adding(1,2,3)
print(add1)

add2 = adding('a','b','c')
print(add2)

x: List[List[int]] = []
x: Dict[str, str] = {}
x: Set[float] = {}


Vector = List[float]
Vectors = List[Vector]
def foo(v: Vectors) -> Vector:
    print(v)
    

def foo2(seq: Sequence[str]):
    pass

def testing(number1: Optional[int] = None):
    print(number1)