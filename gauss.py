import math
from functools import reduce

class SystemOfLinearEquationsSolution:
    def __init__(self, A): #А-матрица (в ней же вектор b)
        self.A = A  # тут будет лежать матрица (в ней же вектор б)
        self.rows = len(A) # количество уравнений
        self.cols = len(A[0]) # количество неизвестных
        self.ans = [0 for i in range(self.rows)] # вектор с результатом

    #прямой ход
    def forvard_stroke(self, pos): #номер переменной, с которой начинаемся обнуление
        k = pos
        # тут смотришь, не является ли опорный элемент нулем, если является, меняем с ненулевым
        while (k < self.rows and self.A[k][pos] == 0): 
            k += 1
        #тут меняем
        if (k < self.rows and k != pos):
            self.A[k], self.A[pos] = self.A[pos], self.A[k]
        #собссна само высчитывание
        for i in range(pos + 1, self.rows):
            for j in range(pos + 1, self.cols):
                #тут такая формула, чтобы подольше оставаться в целых числах
                self.A[i][j] = self.A[pos][pos] * self.A[i][j] - self.A[pos][j] * self.A[i][pos]
            # обнуляем элементы под опорным
            self.A[i][pos] = 0.0
            
    # обратный ход
    def return_stroke(self, pos):
        # свободная переменная 
        q = self.A[pos][self.cols - 1]
        #проходимся по всем уже найденным значениям и вычиляем
        for i in range(self.rows):
            q -= self.A[pos][i] * self.ans[i]
        #делим на коэффциент при искомой переменной
        self.ans[pos] = q / self.A[pos][pos]

    # Гаусс
    def Gauss(self): 
        #приводим к треугольному виду
        for i in range(self.rows - 1):
            self.forvard_stroke(i)
        
        for i in range(self.rows):
            filA = list( filter(lambda x: x != 0, self.A[i]) )
            if not len(filA):
                continue
            gcd = reduce(math.gcd, list(map(int, filA)))
            self.A[i] = list(map(lambda x: x / gcd, self.A[i]))
            
        #считаем сколько ненулевых строк в матрице
        self.none_zero_rows = 0
        for i in range(self.rows):
            check = 0
            for j in range(self.cols - 1):
                check += abs( self.A[i][j] )

            #проверка на случай, если нет решения
            if (check == 0 and self.A[i][self.cols - 1] != 0):
                return ("Решений нет", [], 0)
            if (check != 0):
                self.none_zero_rows += 1
        #если число необнуленных уравнений равно числу неизвестный, то решение сущ и ед
        if (self.none_zero_rows == self.cols - 1):
            #обратным ходом считаем решение
            j = self.rows - 1
            while (j >= 0):
                self.return_stroke(j)
                j -= 1
            #отправляем ответ
            return ("Решение существует и оно единственное", self.ans, 1)
        else:
            #если решений много, то возвращаем результат функции для моиска множества решений
            return self.multiple_solutions()
            
    def multiple_solutions(self):
        basis_vars = [] #тут будем хранить базисные переменные
        big_answer = [] #тут будет ответ (массив векторов Х)
        first = 0
        #если элемент с индексом (0, 0) ненулевой
        if(self.A[0][0] != 0):
            first += 1
            basis_vars.append(0)

        #получаем все базисные переменные
        for i in range(first, self.rows):
            for j in range(self.cols - 1):
                if(self.A[i][j] == 0 and self.A[i][j + 1] != 0):
                    basis_vars.append(j + 1)
                    break
        # свободные переменные
        free_vars = [i for i in range(self.cols - 1) if i not in basis_vars]

        #идем по свободным переменным и поочередно присваиваем каждой значение 1 (остальные 0)
        for var in free_vars:
            #генерируем массив с ответом
            self.ans = [0 for i in range(self.cols - 1)]
            # одной из свободных переменных даем 1
            self.ans[var] = 1
            #счетчик для хранения номера текущей строки
            current_row = self.none_zero_rows - 1

            #обратных ход для ступенчатой матрицы
            for i in range(len(basis_vars) - 1, -1, -1):
                tmp = self.A[current_row][self.cols -1] # это у
                #логика как в return_stroke (разница в том, что там номер переменной совпадаем с номером уравнения, а тут нет)
                for j in range(self.cols - 2, basis_vars[i], -1): 
                    tmp -= self.A[current_row][j] * self.ans[j]
                tmp /= self.A[current_row][basis_vars[i]]
                #в ответ записываем найденный результат с округлением до 5 знаков после запятой
                self.ans[basis_vars[i]] = round(tmp, 5)
                #поднимаемся на следующую переменную
                current_row -= 1               
            #ответ, полученный для случая, когда свободная переменная вар = 1, а остальные свободные 0
            #записывает в big_answer
            big_answer.append(self.ans)
        #Возвращаем ответ
        return("Существует бесконечно много решений", big_answer, 2)

#ДЛЯ ТЕСТОВ

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