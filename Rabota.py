import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Игра: Волк, коза и капуста")
        self.setGeometry(100, 100, 400, 200)

        self.status_label = QLabel("Подайте волку, козе и капусте на другой берег, нажимая кнопку объекта, затем 'Лодка' и 'Перевезти'.", self)
        self.status_label.setGeometry(20, 20, 360, 50)

        self.btn_wolf = QPushButton("Волк", self)
        self.btn_wolf.setGeometry(20, 90, 100, 30)
        self.btn_wolf.clicked.connect(lambda: self.put_in_boat("wolf"))

        self.btn_goat = QPushButton("Коза", self)
        self.btn_goat.setGeometry(150, 90, 100, 30)
        self.btn_goat.clicked.connect(lambda: self.put_in_boat("goat"))

        self.btn_cabbage = QPushButton("Капуста", self)
        self.btn_cabbage.setGeometry(280, 90, 100, 30)
        self.btn_cabbage.clicked.connect(lambda: self.put_in_boat("cabbage"))

        self.btn_boat = QPushButton("Лодка", self)
        self.btn_boat.setGeometry(20, 130, 100, 30)
        self.btn_boat.clicked.connect(self.move_boat)
        self.btn_boat.setEnabled(True)

        self.btn_transport = QPushButton("Перевезти", self)
        self.btn_transport.setGeometry(150, 130, 100, 30)
        self.btn_transport.clicked.connect(self.move_objects)
        self.btn_transport.setEnabled(False)

        self.current_side = {"wolf": True, "goat": True, "cabbage": True, "boat": True}
        self.opposite_side = {"wolf": False, "goat": False, "cabbage": False, "boat": False}

        self.objects_to_move = []

        self.boat_clicked = False

    def put_in_boat(self, obj):
        if self.boat_clicked:
            if len(self.objects_to_move) < 2:
                if obj not in self.objects_to_move:
                    if self.current_side[obj] == self.current_side["boat"]:
                        self.objects_to_move.append(obj)
                        self.status_label.setText("Объект {} посажен в лодку.".format(obj.capitalize()))
                    else:
                        self.status_label.setText("Объект {} на противоположном берегу.".format(obj.capitalize()))
                else:
                    self.status_label.setText("Объект {} уже в лодке.".format(obj.capitalize()))
            else:
                self.status_label.setText("Лодка переполнена!")
            if len(self.objects_to_move) > 0:
                self.btn_transport.setEnabled(True)
        else:
            self.status_label.setText("Сначала нажмите 'Лодка'.")

    def move_boat(self):
        self.boat_clicked = True
        self.btn_boat.setEnabled(False)
        self.update_status()

    def move_objects(self):
        if len(self.objects_to_move) > 0:
            for obj in self.objects_to_move:
                if self.current_side[obj] == self.current_side["boat"]:
                    if obj != "boat":
                        if "wolf" in self.objects_to_move and "goat" in self.objects_to_move and "cabbage" not in self.objects_to_move:
                            self.status_label.setText("Волк съест козу!")
                            return
                        elif "goat" in self.objects_to_move and "cabbage" in self.objects_to_move and "wolf" not in self.objects_to_move:
                            self.status_label.setText("Коза съест капусту!")
                            return
                        else:
                            self.current_side[obj] = not self.current_side[obj]
                            self.opposite_side[obj] = not self.opposite_side[obj]
                            self.current_side["boat"] = not self.current_side["boat"]
                            self.opposite_side["boat"] = not self.opposite_side["boat"]
                else:
                    self.status_label.setText("Объект {} уже на противоположном берегу.".format(obj.capitalize()))
            self.update_status()
            self.objects_to_move.clear()
            self.boat_clicked = False
            self.btn_transport.setEnabled(False)
            self.btn_boat.setEnabled(True)
        else:
            self.status_label.setText("Выберите объект для перемещения.")

    def update_status(self):
        if all(value == False for value in self.current_side.values()):
            self.status_label.setText("Поздравляем! Вы выиграли!")
        elif (self.current_side["goat"] == self.current_side["cabbage"] and self.current_side["goat"] != self.current_side["boat"]) or \
                (self.current_side["wolf"] == self.current_side["goat"] and self.current_side["wolf"] != self.current_side["boat"]):
            self.status_label.setText("Неверный ход! Один из предметов съеден.")
        else:
            self.status_label.setText("Выберите объект для перемещения.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
