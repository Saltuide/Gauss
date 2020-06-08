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
        self.none_zero_rows = 0
        #считаем сколько ненулевых строк в матрице
        for i in range(self.rows):
            check = 0
            for j in range(self.cols - 1):
                check += abs( self.A[i][j] )
                
            if (check == 0 and self.A[i][self.cols - 1] != 0):
                return ("Решений нет", [])

            if (check != 0):
                self.none_zero_rows += 1
                
        if (self.none_zero_rows == self.cols - 1):
    
            j = self.rows - 1
            while (j >= 0):
                self.return_stroke(j)
                j -= 1
            return ("Решение существует и оно единственное", self.ans)
        else:
            return self.multiple_solutions()
            
    def multiple_solutions(self):
        basis_vars = []
        big_answer = []
        if(self.A[0][0] != 0):
            basis_vars.append(0)
        for i in range(self.rows - 1):
            for j in range(self.cols - 1):
                if(self.A[i][j] == 0 and self.A[i][j + 1] != 0):
                    basis_vars.append(j + 1)
                    break
        
        free_vars = [i for i in range(self.cols - 1) if i not in basis_vars]
        for var in free_vars:
            self.ans = [0 for i in range(self.cols - 1)]
            self.ans[var] = 1
            current_row = self.none_zero_rows - 1
            for i in range(len(basis_vars) - 1, -1, -1):
                tmp = self.A[current_row][self.cols -1] # это у

                for j in range(self.cols - 2, basis_vars[i], -1):
                    tmp -= self.A[current_row][j] * self.ans[j]

                tmp /= self.A[current_row][basis_vars[i]]
                self.ans[basis_vars[i]] = round(tmp, 5)
                current_row -= 1                
            big_answer.append(self.ans)
        return("Существует бесконечно много решений", big_answer)


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