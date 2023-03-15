import pytest

from classes.Parser import Parser

parser = Parser()


def test_add_sub_expressions():
    assert parser.run("1+1") == 2
    assert parser.run("21+21") == 42
    assert parser.run("1-1") == 0
    assert parser.run("50-150") == -100
    assert parser.run("100 + 100") == 200
    assert parser.run("100 + 100 -  100+1") == 101
    assert parser.run("100 + 100 -  100+1         -101                  - 900") == -900
    with pytest.raises(Exception):
        parser.run("2+*2")
    with pytest.raises(Exception):
        parser.run("2+/2")
    with pytest.raises(Exception):
        parser.run("2+")


def test_mult_div_expressions():
    assert parser.run("1*1") == 1
    assert parser.run("1*1") == 1
    assert parser.run("32*985") == 31520
    assert parser.run("3168/99") == 32
    assert parser.run("2+5*4") == 22
    assert parser.run("2*4/2") == 4
    assert parser.run("0/1") == 0
    assert parser.run("8*9/2") == 36
    assert parser.run("1/2") == 0

    with pytest.raises(Exception):
        parser.run("2**2")
    with pytest.raises(Exception):
        parser.run("2*/2")
    with pytest.raises(Exception):
        parser.run("2//2")
    with pytest.raises(Exception):
        parser.run("2/*2")
    with pytest.raises(Exception):
        parser.run("2/")
    with pytest.raises(Exception):
        parser.run("2*")


def test_add_comments():
    assert parser.run("2 # A /* 1 */ 2") == 2
    assert parser.run("1 #* A */ 1 /* A */") == 1
    assert parser.run("1 + 3#* 2 */ 3") == 4
    assert parser.run("1 # A") == 1

    with pytest.raises(Exception):
        parser.run("# A")


def test_parentheses_expressions():
    assert parser.run("(1+1)*3") == 6
    assert parser.run("(1+1)*10") == 20
    assert parser.run("(1+1)*(2+2)") == 8
    assert parser.run("(10*(9*9))") == 810
    assert parser.run("(((1+1)))") == 2

    with pytest.raises(Exception):
        parser.run("1+1)")
    with pytest.raises(Exception):
        parser.run("(1+1")
    with pytest.raises(Exception):
        parser.run("1+1(")
    with pytest.raises(Exception):
        parser.run("1(+)1")


def test_single_op():
    assert parser.run("--2") == 2
    assert parser.run("- -2") == 2
    assert parser.run("--2+40") == 42
    assert parser.run("44---2") == 42
    assert parser.run("40+-+-2") == 42
    assert parser.run("40+++++++++2") == 42

    with pytest.raises(Exception):
        parser.run("-++-/1")
