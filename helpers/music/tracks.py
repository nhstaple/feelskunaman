
def decode_ms(milliseconds: float) -> str:
    import math
    length = int(milliseconds / 1000)
    min = math.floor(length / 60) ; sec = length - (60 * min)
    return str(min) + 'm ' + str(sec) + 's'

def decode_mode(val: int) -> str:
    return 'major ' if val else 'minor'

def decode_key(val: int) -> str:
    if   val == 0:  return 'C'
    elif val == 1:  return 'C♯'
    elif val == 2:  return 'D'
    elif val == 3:  return 'D♯'
    elif val == 4:  return 'E'
    elif val == 5:  return 'F'
    elif val == 6:  return 'F♯'
    elif val == 7:  return 'G'
    elif val == 8:  return 'G♯'
    elif val == 9:  return 'A'
    elif val == 10: return 'A♯'
    elif val == 11: return 'B'
    else          : return 'C'

