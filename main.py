from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem
from mydesign import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys

from gauss import SystemOfLinearEquationsSolution
 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.label_for_rows = QLabel("Количество уравнений")
        self.label_for_cols = QLabel("Количество неизвестных")
        self.spin_for_rows = QSpinBox()
        self.spin_for_cols = QSpinBox()
        self.spin_for_cols.setMinimum(2)
        self.spin_for_rows.setMinimum(2)
        self.ans_verdict = QLabel("")
        self.ans_vector = QLabel("")
        self.save_button = QPushButton("Сохранить")
        self.load_button = QPushButton("Загрузить")
        self.header = QLabel("Решение систем линейных уравнений методом Гаусса")
        self.header.setAlignment(QtCore.Qt.AlignHCenter)
        self.solve_button = QPushButton("Привести к треугольному виду и решить")  

        self.table = QTableWidget()
        self.table.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Thin)) 
        
        self.many_zeros()

        self.table_triangle = QTableWidget()
        # self.table_triangle.setColumnCount(3)
        # self.table_triangle.setRowCount(3)

        self.header.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Light)) 
        self.header.setStyleSheet("""
            margin-top: 20px;
            margin-bottom: 20px;
        """)

        
        grid = QGridLayout()
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
        self.solve_button.clicked.connect(self.solve)
        self.spin_for_rows.valueChanged.connect(self.update_table_rows)
        self.spin_for_cols.valueChanged.connect(self.update_table_cols)
        
        self.table.cellChanged.connect(self.update_resize)
        self.my_A = []
    
    def update_resize(self):
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        for i in range(rows):
            for j in range(cols + 2):
                self.table.item(i, j).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)


    def many_zeros(self):
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols + 2)
        headers = [f'x{i + 1}' for i in range(cols)]
        headers.append("=")
        headers.append("y")
        self.table.setHorizontalHeaderLabels(headers)
        for i in range(rows):
            for j in range(cols + 2):
                if (j == cols):
                    self.table.setItem(i, j, QTableWidgetItem('='))
                else:
                    self.table.setItem(i, j, QTableWidgetItem('0'))
                self.table.item(i, j).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


    def paint_triangle(self, new_A):
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        self.table_triangle.setRowCount(rows)
        self.table_triangle.setColumnCount(cols + 2)
        headers = [f'x{i + 1}' for i in range(cols)]
        headers.append("=")
        headers.append("y")
        self.table_triangle.setHorizontalHeaderLabels(headers)
        for i in range(rows):
            for j in range(cols):
                self.table_triangle.setItem(i, j, QTableWidgetItem(str(new_A[i][j])))
                self.table_triangle.item(i, j).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.table_triangle.setItem(i, cols, QTableWidgetItem("="))
            self.table_triangle.setItem(i, cols + 1, QTableWidgetItem(str(new_A[i][cols])))
            self.table_triangle.item(i, cols + 1).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        self.table_triangle.resizeColumnsToContents()
        self.table_triangle.resizeRowsToContents()

    def solve(self):
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        self.my_A = []
        for i in range(self.spin_for_rows.value()):
            arr = []
            for j in range(self.spin_for_cols.value() + 2):
                if j == self.spin_for_cols.value():
                    continue
                if (self.table.item(i, j) != None):
                    try:
                        arr.append(float(self.table.item(i, j).text()))
                    except ValueError:
                        print(i, j)
                        print(self.table.item(i, j).text())
                        print("Поменяй введенные значения на нормальные, дебил")
                else:
                    arr.append(0)
            self.my_A.append(arr)
        print(self.my_A)

        kek = SystemOfLinearEquationsSolution(self.my_A)
        res_text, res = kek.Gauss()
        self.ans_verdict.setText(res_text)
        if (len(res)):
            self.ans_vector.setText(str(res))

        self.paint_triangle(kek.A)


    
    def update_table_rows(self):
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        self.table.setRowCount(rows)
        for i in range(cols + 2):
            if (i == cols):
                self.table.setItem(rows - 1, i, QTableWidgetItem('='))
            elif (self.table.item(rows - 1, i) == None):
                self.table.setItem(rows - 1, i, QTableWidgetItem('0'))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
    
        
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


if __name__ == "__main__":        
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())