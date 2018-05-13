
# ---------------------------
# ----- Perceptron class ----
# ---------------------------

class Perceptron:
    def __init__(self, X, f):
        self.coeff = [1 for _ in range(X)]
        self.func = f

    def evaluate(self, A):
        s=0
        for i in range(len(self.coeff)):
            s += self.coeff[i]*A[i]
        return self.func(s)
