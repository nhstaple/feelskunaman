def DisplayDict(data:dict, prefix:str=''):
    for key, val in data.items():
        print(prefix + '- ' + '{:16s}'.format(key) + ' {:3.3f}'.format(val))