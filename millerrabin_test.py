import millerrabin
import pytest

primeTestData = [
                    (1,False),
                    (2,True),
                    (3,True),
                    (11,True),
                    (12,False),
                    (99999999977, True),
                    (99999999973, False),
                    (100123456789, True),
                    (798006269373, False),
                    (9999999999971, True),
                    (9999999999973, False),
                    #(116065545560611, False),
                    #(113068989860311, False),
                    #(156358050853651, False)
                ]
@pytest.mark.parametrize("given, expected", primeTestData)
def test_isPrime(given, expected):
    actual = millerrabin.MRPrimeTester.isPrime(given,1)
    assert expected == actual