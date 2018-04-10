"""
SLIM basic implementation. To understand deeply how it works we encourage you to
read "SLIM: Sparse LInear Methods for Top-N Recommender Systems".
"""
from sklearn.linear_model import SGDRegressor
from util import tsv_to_matrix
from metrics import compute_precision
from recommender import slim_recommender
import numpy as np
from scipy.sparse import lil_matrix


def slim_train(A, l1_reg=0.001, l2_reg=0.0001):
    """
    Computes W matrix of SLIM

    This link is useful to understand the parameters used:

        http://web.stanford.edu/~hastie/glmnet_matlab/intro.html

        Basically, we are using this:

            Sum( yi - B0 - xTB) + ...
        As:
            Sum( aj - 0 - ATwj) + ...

    Remember that we are wanting to learn wj. If you don't undestand this
    mathematical notation, I suggest you to read section III of:

        http://glaros.dtc.umn.edu/gkhome/slim/overview
    """
    alpha = l1_reg+l2_reg
    l1_ratio = l1_reg/alpha

    model = SGDRegressor(
        penalty='elasticnet',
        fit_intercept=False,
        alpha=alpha,
        l1_ratio=l1_ratio,
    )

    # TODO: get dimensions in the right way
    m, n = A.shape

    # Fit each column of W separately
    W = lil_matrix((n, n))

    for j in range(n):
        if j % 50 == 0:
            print('-> %2.2f%%' % ((j/float(n)) * 100))

        aj = A[:, j].copy()
        # We need to remove the column j before training
        A[:, j] = 0

        model.fit(A, aj.toarray().ravel())
        # We need to reinstate the matrix
        A[:, j] = aj

        w = model.coef_

        # Removing negative values because it makes no sense in our approach
        w[w<0] = 0

        for el in w.nonzero()[0]:
            W[(el, j)] = w[el]

    return W


def main(train_file, part_file ,test_file):


         
    AG = tsv_to_matrix(train_file, 942, 1682)
    AP = tsv_to_matrix(part_file, 942, 1682)

         
    W1 = slim_train(AG)
    W2 = slim_train(AP)
    for i in range(0,11):
        W = (i/10)*W1 + (1-i/10)*W2
        print(i/10)
        recommendations = slim_recommender(AP, W)
        compute_precision(recommendations, test_file)

if __name__ == '__main__':
    main('train_50.tsv',
         'train_data3.tsv',
         'test_data3.tsv')

