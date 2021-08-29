
def ComputeMean(data:list):
    # initialize the return object
    n    = len(data)
    mean = dict()
    for key in data[0]: mean[key] = float(0)

    # iterate over the data to get the mean
    for x in data:
        for key in mean:
            mean[key] = mean[key] + ( x[key] / n )
    
    # print('mean data:')
    # for key in mean:
    #     print('{0:16s} {1:.4f}'.format(key, mean[key]))
    return mean
