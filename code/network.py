from correlation import CorrelationMatrix

class CorrelationNetwork:
    def __init__(self, correlation_matrix, threshold):
        """
        Constructs a co-expression network from a correlation matrix by adding edges between nodes with absolute
        correlation bigger than the given threshold.
        :param correlation_matrix: a CorrelationMatrix (see correlation.py)
        :param threshold: a float between 0 and 1
        """
        self.edges = []
        for (node1, node2), correlation in correlation_matrix.items():
            if abs(correlation) >= threshold and node1 != node2:
                self.edges.append((node1, node2, correlation))


    def to_sif(self, file_path):
        """
        Write the network into a simple interaction file (SIF).
        Column 0: label of the source node
        Column 1: interaction type
        Columns 2+: label of target node(s)
        :param file_path: path to the output file
        """
        with open(file_path, 'w') as f:
            for node1, node2, correlation in self.edges:
                f.write(f"{node1}\tco-expression\t{node2}\n")
