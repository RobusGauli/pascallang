import os
import six
import sys
import collections 
from collections import namedtuple
import argparse
import functools
import operator
import concurrent
import sqlalchemy
import flask
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from functools import wraps

class Contract:
    @classmethod
    def check(cls, val):
        pass


    def __set_name__(self, cls, name):
        self.name = name

    def __set__(self, instance, val):
        self.check(val)
        print('setting')
        instance.__dict__[self.name] = val
        #setattr(instance, self.name, val)
    

class Typed(Contract):
    ty = None
    @classmethod
    def check(cls, val):
        assert isinstance(val, cls.ty), 'Expeected {}'.format(cls.ty)
        super().check(val)

class Integer(Typed):
    ty = int

class Float(Typed):
    ty = float

class String(Typed):
    ty = str


from inspect import signature
def check(func):
    ann = func.__annotations__
    sig = signature(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for key, val in bound.arguments.items():
            if key in ann:
                ann[key].check(val)
        return func(*args, **kwargs)
    return wrapper


@check
def add(a: Integer, b: Integer):
    return a + b


class Vector:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, vec):
        self.x += vec.x
        self.y += vec.y

#we will go roung the trouble to make this class also a type check
from inspect import Signature, Parameter

make_signature = lambda fields: Signature([Parameter(f, Parameter.POSITIONAL_OR_KEYWORD) for f in fields])

class MyType(type):

    def __new__(cls, clsname, bases, clsdict):
        _fields = [key for key, val in clsdict.items() if isinstance(val, Contract)]
        _sig = make_signature(_fields)
        clsdict['sig'] = _sig

        return super().__new__(cls, clsname, bases, clsdict)

class Base(metaclass=MyType):
    
    def __init__(self, *args, **kwargs):
        bound = self.sig.bind(*args, **kwargs)
        for key, val in bound.arguments.items():
            setattr(self, key, val)
        
class Vector(Base):

    x = Integer() #differnece in specfication
    y = Integer() #difference in specfication

class Person(Base):
    name = String()
    age = Integer() 
    shares = Float()
    #this must looks so much familiar with the django model
    #because this is all the magic they used to make client code more readable

class Person(Base):
    name: String
    age: Integer
    shares: Float
    #new feature in python 3.6


class MyType(type):

    def __new__(cls, clsname, bases, clsdict):
        _cls = super().__new__(cls, clsname, bases, clsdict)
        if __annoations__ in _cls.__dict__:
            _sig = make_signature(_cls.__annotations__)
            setattr(_cls, 'sig', _sig)
            for key, val in _cls.__annotations__.items():
                setattr(_cls, key, val())
        return _cls

class Base(metaclass=MyType):

    def __init__(self, *args, **kwargs):
        bound = self.sig.bind(*args, **kwargs)
        for key, val in bound.arguments.items():
            setattr(self, key, val)

class Person(Base):
    name: String
    age: Integer




