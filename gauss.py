class SystemOfLinearEquationsSolution:
    def __init__(self, A): #А-матрица (в ней же вектор b)
        self.main_A = A
        self.A = A 
        self.rows = len(A)
        self.cols = len(A[0])
        self.ans = [0 for i in range(self.rows)]

    def forvard_stroke(self, pos):
        k = pos
        while (k < self.rows and self.A[k][pos] == 0):
            k += 1
        if (k < self.rows and k != pos):
            self.A[k], self.A[pos] = self.A[pos], self.A[k]
        for i in range(pos + 1, self.rows):
            for j in range(pos + 1, self.rows + 1):
                self.A[i][j] = self.A[pos][pos] * self.A[i][j] - self.A[pos][j] * self.A[i][pos]
            self.A[i][pos] = 0.0
            
    
    def return_stroke(self, pos):
        q = self.A[pos][self.cols - 1]
        for i in range(self.rows):
            q -= self.A[pos][i] * self.ans[i]
        self.ans[pos] = q / self.A[pos][pos]

    def Gauss(self): 
        for i in range(self.rows - 1):
            self.forvard_stroke(i)
        none_zero_rows = 0
        #считаем сколько ненулевых строк в матрице
        for i in range(self.rows):
            check = 0
            for j in range(self.cols - 1):
                check += abs( self.A[i][j] )
                
            if (check == 0 and self.A[i][self.cols - 1] != 0):
                return ("Решений нет", [])

            if (check != 0):
                none_zero_rows += 1
                
        if (none_zero_rows == self.cols - 1):
    
            j = self.rows - 1
            while (j >= 0):
                self.return_stroke(j)
                j -= 1
            return ("Решение существует и оно единственное", self.ans)
        else:
            return("Существует бесконечно много решений", [])
        


# arr = [ #одно решение 7, 3
#     [5, 9, 62],
#     [9, -3, 54]
# ]

# arr = [ #одно решение 8, 5, -9
#     [7, -9, 1, 2],
#     [0, 6, 5, -15],
#     [3, -3, 2, -9]
# ]

# arr = [ #решений бесконечно много
#     [2, 3, -1, 1, 1],
#     [8, 12, -9, 8, 3],
#     [4, 6, 3, -2, 3],
#     [2, 3, 9, -7, 3]
# ]

# arr = [ # решений нет
#     [1, 1, 2],
#     [2, 2, 3]
# ]

# kekmda = SystemOfLinearEquationsSolution(arr)
# kekmda.Gauss()