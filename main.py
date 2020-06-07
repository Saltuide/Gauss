from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem
from mydesign import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
 
 
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
        self.ans = QLabel("self.ans")
        self.save_button = QPushButton()
        self.save_button.setText("Сохранить")
        self.load_button = QPushButton()
        self.load_button.setText("Загрузить")
        self.header = QLabel("Решение систем линейных уравнений методом Гаусса")
        self.header.setAlignment(QtCore.Qt.AlignHCenter)

        self.table = QTableWidget()
        self.update_table()


        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.header, 0, 0, 1, 6)
        grid.addWidget(self.label_for_rows, 1, 0)
        grid.addWidget(self.spin_for_rows, 1, 1)

        grid.addWidget(self.label_for_cols, 1, 2)
        grid.addWidget(self.spin_for_cols, 1, 3)
        grid.addWidget(self.table, 2, 0, 1, 6)
        grid.addWidget(self.ans, 3, 0)
        grid.addWidget(self.save_button, 1, 4)
        grid.addWidget(self.load_button, 1, 5)


        self.ui.centralwidget.setLayout(grid)

        self.spin_for_rows.valueChanged.connect(self.update_table)
        self.spin_for_cols.valueChanged.connect(self.update_table)



        
    def update_table(self):
        cols = self.spin_for_cols.value()
        rows = self.spin_for_rows.value()
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols + 2)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        headers = [f'x{i + 1}' for i in range(cols)]
        headers.append("=")
        headers.append("y")

        for i in range(rows):
            if(self.table.item(i, cols) != None):
                item = self.table.item(i, cols).text()
                self.table.setItem(i, cols + 1, QTableWidgetItem(item))
            if(self.table.item(i, cols - 1) != None and self.table.item(i, cols - 1).text() == "="):
                self.table.setItem(i, cols - 1, QTableWidgetItem())

            self.table.setItem(i, cols, QTableWidgetItem("="))
        self.table.setHorizontalHeaderLabels(headers)

        


if __name__ == "__main__":        
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())