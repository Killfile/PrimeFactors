def ignore_exception(IgnoreException=Exception,DefaultVal=None):
    """ Decorator for ignoring exception from a function
    e.g.   @ignore_exception(DivideByZero)
    e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
    """
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec

safe_int = ignore_exception(ValueError,0)(int)

class StringNumber:
  def __init__(self, value:str):
    self._value = value

  def __init__(self, value:int):
    self._value = str(value)
  
  def increment(self, amount:int=1):
    return StringNumber(safe_int(self._value)+amount)

  def toInt(self):
    return safe_int(self._value)

  def toString(self):
    return self._value

  def length(self):
    return len(self._value)

  def reverse(self):
    return StringNumber(self._value[::-1])

  def __add__(self, other:int):
    return self.increment(other)
  

class PalendromeicOddNumber:
  def __init__(self,left:str,middle:str,right:str):
    intLeft = safe_int(left)
    intRight = safe_int(right)
    intMid = safe_int(middle)
    if(intLeft != intRight):
        if(intRight == 0 and intMid == 0):
            if intLeft > 9:
                raise("Left and right must be the same value")   

    if(intRight == 0 and intLeft > 3 and intLeft % 2 == 0):
        raise("This is supposed to be an odd number")
    elif intRight == 0 and intLeft % 2 == 0:
        raise("This is supposed to be an odd number")

    newValues = [1,2,3]
    if intLeft > 0:
      newValues[0] = StringNumber(intLeft)
    else:
      newValues[0] = StringNumber("")

    if len(middle) > 0: 
        newValues[1] = StringNumber(intMid) 
    else: 
        newValues[1] = StringNumber("")
    
    if intRight > 0:
      newValues[2] = StringNumber(right)
    else:
      newValues[2] = StringNumber("")

    self._updateValues(newValues)

  def maxComponentLength(self):
    return max(self._right.length(), self._middle.length(), self._left.length())

  def toInt(self):
    return int(self.toString())

  def toString(self):
      return self._left.toString() + self._middle.toString() + self._right.toString()

  def odd_increment(self):
    outerInterval = 2
    innerInterval = 1
    newValues = [self._left, self._middle, self._right]

    if self._length == 1:
      newValues[0] = self._left.increment(outerInterval)
      if(newValues[0].toInt() > 9): newValues = self.rebalance(newValues)
    elif self._length == 2:
      newValues[0] = self._left.increment(outerInterval)
      if(newValues[0].toInt() > 9): newValues = self.rebalance(newValues)
      newValues[2] = newValues[0]
    elif self._length %2 == 1:
      newValues[1] = self._middle.increment(innerInterval)
      if newValues[1].toInt() > 9: 
        newValues = self.rebalance_out(newValues)
    elif self._length % 2 == 0:
      newValues[0] = self._left.increment(innerInterval)
      if(newValues[0].length() > self.maxComponentLength()): newValues = self.rebalance(newValues)
      newValues[2] = newValues[0].reverse()
      if newValues[2].toInt() % 2 == 0:
        leftOrderOfMagnitude = pow(10,self._left.length()-1)
        newValues[0] = newValues[0].increment(leftOrderOfMagnitude)
        newValues[2] = newValues[0].reverse()

    self._updateValues(newValues)
    return self.toInt()

  def _updateValues(self, newValues):
    self._left = newValues[0]
    self._middle = newValues[1]
    self._right = newValues[2]
    self._length = len(self.toString())


  def rebalance(self, newValues):
    if newValues[1].toInt() > 9:
      return self.rebalance_out(newValues)

    if self._length < 4:
      left = newValues[0].toString()[0:1]
      right = newValues[0].toString()[1:2]
    elif self._length % 2 == 0:
      left = newValues[0].toString()[:-1]
      right = left[::-1]

    if(self._length % 2 == 0):
      middle = "0"
    else:
      middle = ""
    
    return [StringNumber(left), StringNumber(middle), StringNumber(right)]

  def rebalance_out(self, newValues):
    newValues[1] = StringNumber("0")
    newValues[0] = newValues[0].increment(1)
    if newValues[0].length() > self.maxComponentLength():
      newValues[1] = StringNumber("")

    if newValues[0].reverse().toInt() % 2 == 0:
      leftOrderOfMagnitude = pow(10,self._left.length()-1)
      newValues[0] = newValues[0].increment(leftOrderOfMagnitude)
    
    newValues[2] = newValues[0].reverse()
    return newValues

