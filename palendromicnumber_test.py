from palendromicoddnumber import PalendromeicOddNumber
from palendromicoddnumber import StringNumber
import pytest

def test_initialValue():
    splits = splitPalendrome("3")
    actual = PalendromeicOddNumber(splits[0], splits[1], splits[2])
    assert 3 == actual.toInt()

def splitPalendrome(inputString):
    length = len(inputString)
    if length == 1:
        return [inputString,"",""]
    elif length % 2 == 0:
        divider = int(length / 2)
        left = inputString[0:divider]
        middle = ""
        right = inputString[divider:length]
        return [left, middle, right]
    else:
        divider = int((length-1) / 2)
        return [inputString[0:divider],inputString[divider:divider+1],inputString[divider+1:length]]
    
odd_increment_data = [
    ["3",5],
    ["9",11],
    ["11",33],
    ["99",101],
    ["101",111],
    ["111",121],
    ["191",303],    #should really be 303
    ["999",1001],
    ["1001",1111],
    ["1111",1221],
    ["1991",3003],  #should really be 3003
    ["9999",10001],
    ["10001",10101],
    ["10901",11011],
    ["19991",30003],
    ["99999",100001]
]
@pytest.mark.parametrize("start, expected", odd_increment_data)
def test_odd_increment(start,expected):
    split = splitPalendrome(start)
    actual = PalendromeicOddNumber(split[0],split[1],split[2])
    assert expected == actual.odd_increment()

    
def test_odd_increment_longrun():
    expected = [5, 7, 9, 11, 33, 55, 77, 99, 101]
    split = splitPalendrome("3")
    palendromicOdd = PalendromeicOddNumber(split[0],split[1],split[2])
    palendromes = []
    for i in range(0,9):
        palendromes.append(palendromicOdd.odd_increment())
    assert expected == palendromes

rebalance_data = [
    ["9",["11","",""],["1","","1"]],
    ["99",["11","","9"],["1","0","1"]],
    ["191",["1","10","1"],["3","0","3"]],
    ["999",["9","10","9"],["10","","01"]],
    ["9999",["100","","99"],["10","0","01"]]
]
@pytest.mark.parametrize("start, next, expected", rebalance_data)
def test_rebalance(start, next, expected):
    split = splitPalendrome(start)
    dummy = PalendromeicOddNumber(split[0],split[1],split[2])
    rebalanced = dummy.rebalance([StringNumber(next[0]),StringNumber(next[1]),StringNumber(next[2])])
    actual = [rebalanced[0].toString(), rebalanced[1].toString(), rebalanced[2].toString()]
    assert expected == actual
