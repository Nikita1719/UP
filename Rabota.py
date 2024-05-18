import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Игра: Волк, коза и капуста")
        self.setGeometry(100, 100, 400, 250)

        self.status_label = QLabel("Перевезите волка, козу и капусту на другой берег, нажимая на объект, затем 'Перевезти'.", self)
        self.status_label.setGeometry(20, 20, 360, 50)

        self.btn_wolf_left = QPushButton("Волк", self)
        self.btn_wolf_left.setGeometry(20, 90, 100, 30)
        self.btn_wolf_left.clicked.connect(lambda: self.put_in_boat("wolf", "left"))

        self.btn_goat_left = QPushButton("Коза", self)
        self.btn_goat_left.setStyleSheet("QPushButton{background-image: url(image_49.png)}")
        self.btn_goat_left.setGeometry(150, 90, 200, 200)
        self.btn_goat_left.clicked.connect(lambda: self.put_in_boat("goat", "left"))

        self.btn_cabbage_left = QPushButton("Капуста", self)
        self.btn_cabbage_left.setGeometry(280, 90, 100, 30)
        self.btn_cabbage_left.clicked.connect(lambda: self.put_in_boat("cabbage", "left"))

        self.btn_wolf_right = QPushButton("Волк", self)
        self.btn_wolf_right.setGeometry(20, 160, 100, 30)
        self.btn_wolf_right.clicked.connect(lambda: self.put_in_boat("wolf", "right"))

        self.btn_goat_right = QPushButton("Коза", self)
        self.btn_goat_right.setGeometry(150, 160, 100, 30)
        self.btn_goat_right.clicked.connect(lambda: self.put_in_boat("goat", "right"))

        self.btn_cabbage_right = QPushButton("Капуста", self)
        self.btn_cabbage_right.setGeometry(280, 160, 100, 30)
        self.btn_cabbage_right.clicked.connect(lambda: self.put_in_boat("cabbage", "right"))

        self.btn_transport = QPushButton("Перевезти", self)
        self.btn_transport.setGeometry(20, 200, 100, 30)
        self.btn_transport.clicked.connect(self.move_objects)
        self.btn_transport.setEnabled(False)

        self.btn_return_boat = QPushButton("Лодка назад", self)
        self.btn_return_boat.setGeometry(150, 200, 100, 30)
        self.btn_return_boat.clicked.connect(self.return_boat)
        self.btn_return_boat.setEnabled(False)

        self.btn_restart = QPushButton("Начать сначала", self)
        self.btn_restart.setGeometry(280, 200, 100, 30)
        self.btn_restart.clicked.connect(self.restart_game)
        self.btn_restart.setVisible(False)

        self.initialize_game()

    def initialize_game(self):
        self.left_bank = {"wolf", "goat", "cabbage"}  # Начальное состояние левого берега
        self.right_bank = set()  # Правый берег пустой
        self.boat = set()  # Лодка пуста
        self.boat_location = "left"  # Лодка начинает на левом берегу
        self.update_buttons()
        self.status_label.setText("Перевезите волка, козу и капусту на другой берег, нажимая на объект, затем 'Перевезти'.")
        self.btn_transport.setEnabled(False)
        self.btn_return_boat.setEnabled(False)
        self.btn_restart.setVisible(False)

    def update_buttons(self):
        for obj in ["wolf", "goat", "cabbage"]:
            getattr(self, f"btn_{obj}_left").setEnabled(obj in self.left_bank and self.boat_location == "left")
            getattr(self, f"btn_{obj}_right").setEnabled(obj in self.right_bank and self.boat_location == "right")
        self.btn_transport.setEnabled(len(self.boat) > 0)
        self.btn_return_boat.setEnabled(len(self.boat) == 0 and self.boat_location == "right")

    def put_in_boat(self, obj, side):
        if side == "left" and self.boat_location == "left" and obj in self.left_bank:
            if len(self.boat) < 2:
                self.left_bank.remove(obj)
                self.boat.add(obj)
                self.status_label.setText(f"Объект {obj.capitalize()} посажен в лодку.")
            else:
                self.status_label.setText("Лодка уже занята!")
        elif side == "right" and self.boat_location == "right" and obj in self.right_bank:
            if len(self.boat) < 2:
                self.right_bank.remove(obj)
                self.boat.add(obj)
                self.status_label.setText(f"Объект {obj.capitalize()} посажен в лодку.")
            else:
                self.status_label.setText("Лодка уже занята!")
        else:
            self.status_label.setText(f"Объект {obj.capitalize()} на противоположном берегу.")
        self.update_buttons()

    def move_objects(self):
        if self.boat:
            if self.boat_location == "left":
                for obj in self.boat:
                    self.right_bank.add(obj)
                self.boat_location = "right"
            else:
                for obj in self.boat:
                    self.left_bank.add(obj)
                self.boat_location = "left"
            self.boat.clear()
            self.check_game_status()
            self.update_buttons()
        else:
            self.status_label.setText("Лодка пуста. Сначала посадите объект в лодку.")

    def return_boat(self):
        if len(self.boat) == 0 and self.boat_location == "right":
            self.boat_location = "left"
            self.update_buttons()
            self.status_label.setText("Лодка возвращена на левый берег.")
        else:
            self.status_label.setText("Лодка не пуста или уже находится на левом берегу.")

    def check_game_status(self):
        if not self.left_bank and not self.boat:  # Если левый берег и лодка пусты, игрок выиграл
            self.status_label.setText("Поздравляем! Вы выиграли!")
            self.btn_restart.setVisible(True)
            return

        if len(self.boat) == 0:  # Проверка только если лодка пуста
            if (("goat" in self.left_bank and "cabbage" in self.left_bank and "wolf" not in self.left_bank) or
                ("goat" in self.right_bank and "cabbage" in self.right_bank and "wolf" not in self.right_bank)) and \
                ("goat" not in self.boat):
                self.status_label.setText("Неверный ход! Коза съела капусту. Попробуйте еще раз.")
                self.btn_restart.setVisible(True)
                return

            if (("goat" in self.left_bank and "wolf" in self.left_bank and "cabbage" not in self.left_bank) or
                ("goat" in self.right_bank and "wolf" in self.right_bank and "cabbage" not in self.right_bank)) and \
                ("goat" not in self.boat):
                self.status_label.setText("Неверный ход! Волк съел козу. Попробуйте еще раз.")
                self.btn_restart.setVisible(True)
                return

        if len(self.boat) == 0:  # Проверка обоих берегов
            if (("goat" in self.left_bank and "cabbage" in self.left_bank) and "wolf" not in self.left_bank) or \
               (("goat" in self.right_bank and "cabbage" in self.right_bank) and "wolf" not in self.right_bank) or \
               (("goat" in self.left_bank and "wolf" in self.left_bank) and "cabbage" not in self.left_bank) or \
               (("goat" in self.right_bank and "wolf" in self.right_bank) and "cabbage" not in self.right_bank):
                self.status_label.setText("Неверный ход! Вы проиграли. Попробуйте еще раз.")
                self.btn_restart.setVisible(True)
                return

        self.status_label.setText("Выберите объект для перемещения.")

    def restart_game(self):
        self.initialize_game()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
