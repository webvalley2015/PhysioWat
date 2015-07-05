import numpy as np

def scatter_error_bar_creator(mat):
    """Given a Numpy matrix with columns (x,y,error), returns two Numpy matrixes: one with columns (x,y) called "mat_data" and the other with columns (y-error,y+error) called "mat_error""""
    mat_data = mat[:,0:2]
    mat_error = np.empty((mat.shape))
    for i in mat:
        mat_error[:,0] = mat[:,1] - mat[:,2]
        mat_error[:,1] = mat[:,1] + mat[:,2]
    return mat_data, mat_error
