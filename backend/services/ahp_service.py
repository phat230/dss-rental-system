import numpy as np

RI_TABLE = {
    1: 0,
    2: 0,
    3: 0.58,
    4: 0.90,
    5: 1.12,
}

class AHPService:

    @staticmethod
    def calculate_weights(matrix):

        matrix = np.array(matrix)

        n = matrix.shape[0]

        # Normalize matrix
        col_sum = matrix.sum(axis=0)
        normalized_matrix = matrix / col_sum

        # Eigenvector approximation
        weights = normalized_matrix.mean(axis=1)

        # λmax
        weighted_sum = np.dot(matrix, weights)
        lambda_max = np.mean(weighted_sum / weights)

        # CI
        CI = (lambda_max - n) / (n - 1)

        RI = RI_TABLE.get(n, 1.12)

        CR = CI / RI if RI != 0 else 0

        if CR > 0.1:
            raise ValueError("Matrix inconsistent. Please re-enter pairwise comparison.")

        return weights.tolist(), CR