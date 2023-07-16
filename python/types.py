from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    address: list[Address]
    names: list[str]
    paypal_email: str | None
@dataclass
class Address:
    street: str
    number: int
