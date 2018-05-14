
# ---------------------------
# ----- Perceptron class ----
# ---------------------------

class Perceptron:
    def __init__(self, X, f):
        self.coeff = [0.1 for _ in range(X)]
        self.func = f

    def evaluate(self, A):
        s=0
        for i in range(len(A)):
            s += self.coeff[i]*A[i]
        return self.func(s)

    def __str__(self):
        return (self.coeff, self.func)
