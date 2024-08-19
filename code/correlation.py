from itertools import combinations


def rank(X):
    """
    :param x: a list of values
    :return: ranking of the input list
    """
    sorted_X = sorted((x, i) for i, x in enumerate(X))
    ranks = [0] * len(X)
    sum_ranks = 0
    prev_value = None
    for rank, (value, idx) in enumerate(sorted_X):
        if value != prev_value:
            rank_val = rank
            prev_value = value
            sum_ranks = rank
        else:
            sum_ranks += rank
        ranks[idx] = sum_ranks / (rank - rank_val + 1) if value == prev_value else rank
    return ranks


def pearson_correlation(X, Y):
    """
    :param x: a list of values
    :param y: a list of values
    :return: Pearson correlation coefficient of X and Y
    """
    # filter out non-numeric values
    X = [x for x in X if isinstance(x, (int, float))]
    Y = [y for y in Y if isinstance(y, (int, float))]

    n = len(X)
    mean_X = sum(X) / n if n > 0 else 0
    mean_Y = sum(Y) / n if n > 0 else 0
    cov = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(n))
    std_X = (sum((X[i] - mean_X) ** 2 for i in range(n)) / n) ** 0.5 if n > 0 else 0
    std_Y = (sum((Y[i] - mean_Y) ** 2 for i in range(n)) / n) ** 0.5 if n > 0 else 0
    if std_X == 0 or std_Y == 0:
        return 0  

    return cov / (std_X * std_Y)
    

def spearman_correlation(X, Y):
    """
    :param x: a list of values
    :param y: a list of values
    :return: Spearman correlation coefficient of X and Y
    """
    rank_X = rank(X)
    rank_Y = rank(Y)
    return pearson_correlation(rank_X, rank_Y)


def kendall_correlation(X, Y):
    """
    :param x: a list of values
    :param y: a list of values
    :return: Kendall-B correlation coefficient of X and Y
    """
    n = len(X)
    rank_X = rank(X)
    rank_Y = rank(Y)
    
    concordant_pairs = discordant_pairs = tied_X = tied_Y = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            if rank_X[i] == rank_X[j]:
                tied_X += 1
            if rank_Y[i] == rank_Y[j]:
                tied_Y += 1
            if (rank_X[i] < rank_X[j] and rank_Y[i] < rank_Y[j]) or (rank_X[i] > rank_X[j] and rank_Y[i] > rank_Y[j]):
                concordant_pairs += 1
            elif (rank_X[i] < rank_X[j] and rank_Y[i] > rank_Y[j]) or (rank_X[i] > rank_X[j] and rank_Y[i] < rank_Y[j]):
                discordant_pairs += 1

    total_pairs = concordant_pairs + discordant_pairs
    tau_b = (concordant_pairs - discordant_pairs) / ((total_pairs + tied_X) * (total_pairs + tied_Y)) ** 0.5
    return tau_b

class CorrelationMatrix(dict):
    """
    This class behaves like a dictionary, where the correlation between two elements 1 and 2 is accessible via
    cor_matrix[(element_1, element_2)] or cor_matrix[(element_2, element_1)] since the matrix is symmetrical.
    It also stores the row (or column) names of the input DataMatrix.
    """
    def __init__(self, data_matrix, method, rows):
        """
        :param data_matrix: a DataMatrix (see data_matrix.py)
        :param method: string specifying the correlation method, must be 'Pearson', 'Spearman' or 'Kendall'
        :param rows: True if the correlation matrix should be constructed for the rows, False if for the columns
        """
        # initialise the dictionary
        super().__init__(self)

        if rows:
            data = data_matrix.get_rows()
        else:
            data = data_matrix.get_columns()

        # sorted list of row names
        self.names = list(sorted(data.keys()))

        # compute the correlation between all pairs of rows or columns
        for name_1, name_2 in combinations(data.keys(), 2):
            if method == 'Pearson':
                correlation = pearson_correlation(data[name_1], data[name_2])
            elif method == 'Spearman':
                correlation = spearman_correlation(data[name_1], data[name_2])
            elif method == 'Kendall':
                correlation = kendall_correlation(data[name_1], data[name_2])
            else:
                raise ValueError('The correlation method not supported must be either Pearson, Spearman or Kendall.')

            self[(name_1, name_2)] = correlation
            self[(name_2, name_1)] = correlation
