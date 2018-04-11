from decimal import Decimal

PRECISION_AT = 20

def compute_precision(recommendations, test_file):
    """
    Computes recommendation precision based on a tsv test file.
    """
    ## Computing precision
    # Organizing data
    user_item = {}
    with open(test_file) as test_file:
        for line in test_file:
            u, i, v = line.strip().split(' ')
            u, i = int(u) - 1, int(i) -1 
            # TODO: accept float =/
            v = 1
            if u in user_item:
                user_item[u].add(i)
            else:
                user_item[u] = set([i])

    precisions = []
    # Computing
    total_users = Decimal(len(recommendations.keys()))
    for at in range(1, PRECISION_AT+1):
        mean = 0
        hits = 0
        pos = 0
        for u in recommendations.keys():
            relevants = user_item[u]
            retrieved = recommendations[u][:at]
            if len(relevants & set(retrieved)) == 1:
                pos += 1 / (retrieved.index(list(relevants)[0]) + 1)
                hits += 1
#            print(len(retrieved))
            precision = len(relevants & set(retrieved))/Decimal(len(retrieved))
            mean += precision
        HR = hits / total_users
        ARHR = pos / float(total_users)
        if at == 5 or at == 10 or at == 15 or at == 20:
            #print ('Average Precision @%s: %s' % (at, (mean/total_users)))
            print ('Average HR @%s: %s' % (at, HR))
            print ('Average ARHR @%s: %s' % (at, ARHR))
        precisions.append([at, (mean/total_users)])

    return precisions



def compute_precision_as_an_oracle(recommendations, test_file):
    """
    Computes recommendation precision based on a tsv test file but computing it
    as we had an oracle that predicts the best ranking that can be done with
    the recommendations.
    """
    ## Computing precision
    # Organizing data
    user_item = {}
    with open(test_file) as test_file:
        for line in test_file:
            u, i, v = line.strip().split(' ')
            u, i = int(u), int(i)
            # TODO: accept float =/
            v = 1
            if u in user_item:
                user_item[u].add(i)
            else:
                user_item[u] = set([i])

    total_users = Decimal(len(recommendations.keys()))

    # Changing recommendations as an ORACLE
    for u in recommendations.keys():
        recommendations[u] = list(user_item[u] & set(recommendations[u]))
        recommendations[u] += list(
            user_item[u] | set(recommendations[u]) -
            (user_item[u] & set(recommendations[u]))
        )

    # Computing
    for at in range(1, PRECISION_AT+1):
        mean = 0
        for u in recommendations.keys():
            relevants = user_item[u]
            retrieved = recommendations[u][:at]
            precision = len(relevants & set(retrieved))/Decimal(len(retrieved))
            mean += precision

        print ('Average Precision @%s: %s' % (at, (mean/total_users)))

