"""
Comparing rankings of different algorithms.
"""
from util import tsv_to_matrix, show_matplot_fig
from slim import slim_train, slim_recommender
from slim_lda import slim_lda_recommender, LDAHierarquical
from metrics import compute_precision
from scipy.stats import kendalltau
import json
from matplotlib import pyplot as plt

RANKING_UNTIL = 20

def main(train_file, user_item_side_information_file, hierarchy_file, test_file):
    A = tsv_to_matrix(train_file)
    B = tsv_to_matrix(user_item_side_information_file)
    hierarchy = json.loads(open(hierarchy_file).read())

    W = slim_train(A)

    ## LDA
    #lda = LDAHierarquical(B, hierarchy, topics=20)
    #recommendations_lda = slim_lda_recommender(A, W, lda)
    #compute_precision(recommendations_lda, test_file)
    ###

    recommendations_slim = slim_recommender(A, W)
    ## HSLIM
    from hslim import handle_user_bias, hierarchy_factory, normalize_wline, generate_subitem_hierarchy
    hierarchy = hierarchy_factory('data/hierarchy.json')
    K = slim_train(handle_user_bias(B))
    Wline = generate_subitem_hierarchy(K, W, hierarchy)
    WlineNorm = normalize_wline(Wline)
    recommendations_other = slim_recommender(A, WlineNorm)
    ###

    kendall_tau_values = []
    differences_values = []

    for u in recommendations_slim.iterkeys():
        ranking_slim = recommendations_slim[u][:RANKING_UNTIL]
        ranking_other = recommendations_other[u][:RANKING_UNTIL]

        kendall_tau_values.append(kendalltau(ranking_slim, ranking_other))
        differences_values.append(RANKING_UNTIL-len(set(ranking_slim) & set(ranking_other)))

    # Differences
    plt.hist(differences_values)
    plt.xlabel('Size of difference')
    plt.ylabel('Amount of rankings')
    plt.title('Differences (novelty) between rankings')

    # Ranking comparison
    show_matplot_fig()
    plt.figure()
    plt.hist([ i[0] for i in kendall_tau_values ])
    plt.xlabel('KendallTau Distance SLIM/SLIM LDA')
    plt.ylabel('Number of occurrences')
    plt.title('Comparison between rankings')
    show_matplot_fig()


if __name__ == '__main__':
    main('data/train_100.tsv', 'data/user_item_side_information_100.tsv',
         'data/hierarchy.json', 'data/test_100.tsv', )
