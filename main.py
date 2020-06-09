import sys
import os

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout,
                             QSpinBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QTextEdit)

from mydesign import Ui_MainWindow  # импорт нашего сгенерированного файла
from gauss import SystemOfLinearEquationsSolution
 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #объявление объектов
        self.label_for_rows = QLabel("Количество уравнений")
        self.label_for_cols = QLabel("Количество неизвестных")
        self.spin_for_rows = QSpinBox()
        self.spin_for_cols = QSpinBox()
        self.ans_verdict = QLabel("")
        self.ans_vector = QTextEdit("")
        self.save_button = QPushButton("Сохранить")
        self.load_button = QPushButton("Загрузить")
        self.header = QLabel("Решение систем линейных уравнений методом Гаусса")
        self.solve_button = QPushButton("Привести к треугольному виду и решить")  
        self.table = QTableWidget()
        self.table_triangle = QTableWidget()
        grid = QGridLayout()
        #настройки для спинов
        self.spin_for_cols.setMinimum(2)
        self.spin_for_rows.setMinimum(2)
        self.spin_for_rows.lineEdit().setReadOnly(True)
        self.spin_for_cols.lineEdit().setReadOnly(True)
        #наводим красоту для заголовка
        self.header.setAlignment(QtCore.Qt.AlignHCenter)
        self.header.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Light)) 
        self.header.setStyleSheet("""
            margin-top: 20px;
            margin-bottom: 20px;
        """)
        #изачально заполняем нулями главную таблицу
        self.many_zeros()
        #наводим красоту для главной таблицы
        self.table.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Thin)) 
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        #наводим красоту для главной таблицы
        self.table_triangle.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Thin))
        #наводим красоту для вывода ответов
        self.ans_verdict.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Thin))
        self.ans_vector.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Thin))

        #позиционирование элементов
        grid.setSpacing(10)
        grid.addWidget(self.header, 0, 0, 1, 6)
        grid.addWidget(self.label_for_rows, 1, 0)
        grid.addWidget(self.spin_for_rows, 1, 1)
        grid.addWidget(self.label_for_cols, 1, 2)
        grid.addWidget(self.spin_for_cols, 1, 3)
        grid.addWidget(self.save_button, 1, 4)
        grid.addWidget(self.load_button, 1, 5)
        grid.addWidget(self.table, 2, 0, 1, 6)
        grid.addWidget(self.solve_button, 3, 2, 1, 2)
        grid.addWidget(self.table_triangle, 4, 0, 1, 6)
        grid.addWidget(self.ans_verdict, 5, 0, 1, 6)
        grid.addWidget(self.ans_vector, 6, 0, 1, 6)
        
        self.ui.centralwidget.setLayout(grid)
        #обработка действий
        self.solve_button.clicked.connect(self.solve)
        self.spin_for_rows.valueChanged.connect(self.update_table_rows)
        self.spin_for_cols.valueChanged.connect(self.update_table_cols)
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)
        #тут будет лежать матрица
        self.my_A = []
    
    #при изменении размера матрицы на свободые места кидать нули
    def update_resize(self):
        # получаем количество строк и столбцов
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        #проходимся по матрице
        for i in range(rows):
            for j in range(cols + 2):
                #если ячейка пустая, ставим ноль
                if(self.table.item(i, j) == None):
                    self.table.setItem(i, j, QTableWidgetItem('0'))
                #чтоб было красиво
                self.table.item(i, j).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                if(j == cols):
                    #нельзя редактировать "="
                    self.table.item(i, j).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    #Для сохранения
    def save(self):
        # получаем количество строк и столбцов
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        #обнуляем матрицу
        self.my_A = []
        #заполняем матрицу А введенными значениями
        for i in range(rows):
            arr = []
            for j in range(cols + 2):
                if j == cols:
                    continue
                if (self.table.item(i, j) != None):
                    try:
                        arr.append(float(self.table.item(i, j).text()))
                        self.table.item(i, j).setBackground(QtGui.QColor(255, 255, 255))
                    except ValueError:
                        #если пользователь ввел некорректные значения, то ячейку красим в красный и выходим
                        self.table.item(i, j).setBackground(QtGui.QColor(255, 0, 0))
                        return
                else:
                    #на всякий случай
                    arr.append(0)
            self.my_A.append(arr)
        
        #открываем файл для записи
        f = open('test.txt', 'w')
        #записываем строки и столбцы
        f.write(f'{rows} {cols} \n')
        #записываем матрицу
        f.write(str(self.my_A).replace('[', '').
                                replace(',', '').
                                replace('] ', '\n').
                                replace(']', ''))
        #закрываем файл
        f.close()

    #Для загрузки
    def load(self):
        current_dir = os.getcwd()
        #открываем файл
        f = open(current_dir + '/test.txt',  'r')
        #счетчик для номера считываемой линии
        counter = -1
        #идем по строчкам файла
        for line in f:
            #устанавливаем размер матрицы
            if(counter == -1):
                size = line.split(' ')
                self.spin_for_rows.setValue(int(size[0]))
                self.spin_for_cols.setValue(int(size[1]))
                counter += 1
                self.many_zeros()
            else: #считываем и записываем матрицу
                elems = line.split(' ')
                for i, elem in enumerate(elems):
                    if(i == self.spin_for_cols.value()):
                        self.table.setItem(counter, i + 1, QTableWidgetItem(elem.replace('\n', '')))
                    else:
                        self.table.setItem(counter, i, QTableWidgetItem(elem))
                counter += 1
        #размер ячеек под контент
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        #закрываем файл
        f.close()

    # функция для начального заполнения нулями
    def many_zeros(self):
        # получаем количество строк и столбцов
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        #меняем размер таблицы
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols + 2)
        # генерируем и устанавливаем подписи
        headers = [f'x{i + 1}' for i in range(cols)]
        headers.append("=")
        headers.append("y")
        self.table.setHorizontalHeaderLabels(headers)

        #заполняем
        for i in range(rows):
            for j in range(cols + 2):
                if (j == cols):
                    self.table.setItem(i, j, QTableWidgetItem('='))
                    self.table.item(i, j).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                else:
                    self.table.setItem(i, j, QTableWidgetItem('0'))
                self.table.item(i, j).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        #размер под контент
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    #отрисовываем найденную треугольную матрицу
    def paint_triangle(self, new_A):
        # получаем количество строк и столбцов
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        #устанавливаем размер таблицы
        self.table_triangle.setRowCount(rows)
        self.table_triangle.setColumnCount(cols + 2)

        #генерируем и устанавливаем подписи
        headers = [f'x{i + 1}' for i in range(cols)]
        headers.append("=")
        headers.append("y")
        self.table_triangle.setHorizontalHeaderLabels(headers)

        #вписываем
        for i in range(rows):
            for j in range(cols):
                self.table_triangle.setItem(i, j, QTableWidgetItem(str(new_A[i][j])))
                self.table_triangle.item(i, j).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.table_triangle.item(i, j).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.table_triangle.setItem(i, cols, QTableWidgetItem("="))
            self.table_triangle.item(i, cols).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.table_triangle.item(i, cols).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.table_triangle.setItem(i, cols + 1, QTableWidgetItem(str(new_A[i][cols])))
            self.table_triangle.item(i, cols + 1).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.table_triangle.item(i, cols + 1).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        #под контент подгоняем размер
        self.table_triangle.resizeColumnsToContents()
        self.table_triangle.resizeRowsToContents()

    #решаем
    def solve(self):
        # получаем количество строк и столбцов
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        #в А записываем введенные значения
        self.my_A = []
        for i in range(rows):
            arr = []
            for j in range(cols + 2):
                if j == cols:
                    continue
                if (self.table.item(i, j) != None):
                    try:
                        arr.append(float(self.table.item(i, j).text()))
                        self.table.item(i, j).setBackground(QtGui.QColor(255, 255, 255))
                    except ValueError:
                        self.table.item(i, j).setBackground(QtGui.QColor(255, 0, 0))
                        return
                else:
                    arr.append(0)
            self.my_A.append(arr)

        #Находим ответ
        solution = SystemOfLinearEquationsSolution(self.my_A)
        res_text, res, num = solution.Gauss()
        self.ans_verdict.setText(res_text)
        #в зависимости от количества ответов выводим результат
        if (num == 2):
            fsr = 'ФСР: '
            for i, arr in enumerate(res):
                fsr += f'c{i + 1} * {arr} + '
            fsr = fsr[:-2]
            fsr += ', ci - const'
            self.ans_vector.setText(fsr)
        elif(num == 1):
            self.ans_vector.setText(str(res))
        else:
            self.ans_vector.setText('')
        self.paint_triangle(solution.A)

    #при изменении количества уравнений
    def update_table_rows(self):
        # получаем количество строк и столбцов
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        # устанавливаем новый размер таблицы
        self.table.setRowCount(rows)
        #при необходимости вписываем нули
        for i in range(cols + 2):
            if (i == cols):
                self.table.setItem(rows - 1, i, QTableWidgetItem('='))
            elif (self.table.item(rows - 1, i) == None):
                self.table.setItem(rows - 1, i, QTableWidgetItem('0'))
        #ячейки под контент
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.update_resize()
      
    #аналогично с предыдущей
    def update_table_cols(self):
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols + 2)
        headers = [f'x{i + 1}' for i in range(cols)]
        headers.append("=")
        headers.append("y")

        for i in range(rows):
            if (self.table.item(i, cols) != None and self.table.item(i, cols).text() != '='):
                item = self.table.item(i, cols).text()
                self.table.setItem(i, cols + 1, QTableWidgetItem(item))
            if (self.table.item(i, cols - 1) != None and self.table.item(i, cols - 1).text() == "="):
                self.table.setItem(i, cols - 1, QTableWidgetItem('0'))

            self.table.setItem(i, cols, QTableWidgetItem("="))

        self.table.setHorizontalHeaderLabels(headers)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.update_resize()


if __name__ == "__main__":        
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())