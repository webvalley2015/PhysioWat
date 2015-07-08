import numpy as np

def scatter_error_bar_creator(mat):
    """Given a Numpy array with columns (x,y,error), returns two Numpy arrays: one with columns (x,y) called "mat_data" and the other with columns (y-error,y+error) called "mat_error"""
    mat_data = mat[:,0:2] #extracts first two columns (x,y)
    mat_error = np.empty((mat.shape)) #initialises array mat_error
    mat_error[:,0] = mat[:,1] - mat[:,2] #y-error
    mat_error[:,1] = mat[:,1] + mat[:,2] #y+error
    return mat_data, mat_error

def scatter_error_bar_creator_2(accuracy, error):
    """Given two Numpy arays of accuracy and error with same dimensions, returns an array with the coordinates of the points and relative accuracy and error"""
    mat_modified = np.empty([0,3]) #initialises array mat_modified
    for index, item in np.ndenumerate(accuracy):
        mat_modified = np.vstack((mat_modified, [index[0], index[1], item])) #gives the coordinates and the content of each element in accuracy array
    mat_modified = np.hstack((mat_modified, (accuracy - error).flatten().reshape((-1,1)))) #y-error
    mat_modified = np.hstack((mat_modified, (accuracy + error).flatten().reshape((-1,1)))) #y+error
    return mat_modified

def statistic_values(list): # argument: list of lists

    """ computes statistical values needed for a box-plot """

    data = np.array(list) # converts the list into a Numpy array called data
    
    def q14(array, axis=1): # first quartile
        return np.median(array, axis=1) - np.std(array, axis=1)
    def q34(array, axis=1): # third quartile
        return np.median(array, axis=1) + np.std(array, axis=1)
    functions = (np.amin, q14, np.median, q34, np.amax)

    statistics = np.empty((data.shape[0],0)) # initialises numpy array called statistics

    for i in functions:
        statistics = np.hstack((statistics, i(data, axis=1).reshape(-1,1))) # append column to statistics at every iteration

    return statistics

def convert_PandaDataFrame_to_ListOfLists_2D(data):
    return data.values.tolist()

def convert_PandaDataFrame_to_ListOfLists_3D(data):
    return data.values.tolist()
