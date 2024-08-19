from data_matrix import DataMatrix
from network import CorrelationNetwork
from correlation import CorrelationMatrix


def exercise_1():
    expression_file = 'expression.tsv'  
    methylation_file = 'methylation.tsv'  
    
    # load process expression data 
    expression_data = DataMatrix(expression_file)
    expression_data.to_tsv('Rehman_Basit_expression.tsv')
    
    # check for normal distribution 
    expr_not_normal_rows = expression_data.not_normal_distributed(alpha=0.05, rows=True)
    expr_not_normal_cols = expression_data.not_normal_distributed(alpha=0.05, rows=False)
    print(f"Expression Data: {len(expr_not_normal_rows)} genes and {len(expr_not_normal_cols)} samples do not follow a normal distribution")

    # load process methylation data
    methylation_data = DataMatrix(methylation_file)
    methylation_data.to_tsv('Rehman_Basit_methylation.tsv')
    
    # check for normal distribution 
    meth_not_normal_rows = methylation_data.not_normal_distributed(alpha=0.05, rows=True)
    meth_not_normal_cols = methylation_data.not_normal_distributed(alpha=0.05, rows=False)
    print(f"Methylation Data: {len(meth_not_normal_rows)} genes and {len(meth_not_normal_cols)} samples do not follow a normal distribution")



def exercise_3():
    expression_file = 'expression.tsv'  
    methylation_file = 'methylation.tsv'  
    threshold = 0.75
    
    # load process expression data
    expression_data = DataMatrix(expression_file)
    expression_correlation_pearson = CorrelationMatrix(expression_data, 'Pearson', rows=True)
    expression_correlation_spearman = CorrelationMatrix(expression_data, 'Spearman', rows=True)
    expression_correlation_kendall = CorrelationMatrix(expression_data, 'Kendall', rows=True)
    
    # create co-expression networks for expression data
    network_pearson_expr = CorrelationNetwork(expression_correlation_pearson, threshold)
    network_spearman_expr = CorrelationNetwork(expression_correlation_spearman, threshold)
    network_kendall_expr = CorrelationNetwork(expression_correlation_kendall, threshold)
    
    # write co-expression networks to SIF files
    network_pearson_expr.to_sif('Rehman_Basit_expression_network_pearson.sif')
    network_spearman_expr.to_sif('Rehman_Basit_expression_network_spearman.sif')
    network_kendall_expr.to_sif('Rehman_Basit_expression_network_kendall.sif')
    
    # load process methylation data
    methylation_data = DataMatrix(methylation_file)
    methylation_correlation_pearson = CorrelationMatrix(methylation_data, 'Pearson', rows=True)
    methylation_correlation_spearman = CorrelationMatrix(methylation_data, 'Spearman', rows=True)
    methylation_correlation_kendall = CorrelationMatrix(methylation_data, 'Kendall', rows=True)
    
    # create co-expression networks for methylation data
    network_pearson_meth = CorrelationNetwork(methylation_correlation_pearson, threshold)
    network_spearman_meth = CorrelationNetwork(methylation_correlation_spearman, threshold)
    network_kendall_meth = CorrelationNetwork(methylation_correlation_kendall, threshold)
    
    # write co-expression networks to SIF files
    network_pearson_meth.to_sif('Rehman_Basit_methylation_network_pearson.sif')
    network_spearman_meth.to_sif('Rehman_Basit_methylation_network_spearman.sif')
    network_kendall_meth.to_sif('Rehman_Basit_methylation_network_kendall.sif')



# only execute the following if this module is the entry point of the program, not when it is imported into another file
if __name__ == '__main__':
    exercise_1()
    exercise_3()
