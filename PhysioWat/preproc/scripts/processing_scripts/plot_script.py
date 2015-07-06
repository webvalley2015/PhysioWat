import numpy as np

def scatter_error_bar_creator(mat):
    """Given a Numpy array with columns (x,y,error), returns two Numpy arrays: one with columns (x,y) called "mat_data" and the other with columns (y-error,y+error) called "mat_error""""
    mat_data = mat[:,0:2] #extracts first two columns (x,y)
    mat_error = np.empty((mat.shape)) #initialises array mat_error
    for i in mat: #for every row
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

def mean_std(array):
    """ Unuseful function """
    return np.mean(array), np.std(array)
