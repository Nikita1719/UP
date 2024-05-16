import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Игра: Волк, коза и капуста")
        self.setGeometry(100, 100, 400, 200)

        self.status_label = QLabel("Перевезите волка, козу и капусту на другой берег, нажимая на объект, затем 'Перевезти'.", self)
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

        self.btn_transport = QPushButton("Перевезти", self)
        self.btn_transport.setGeometry(150, 130, 100, 30)
        self.btn_transport.clicked.connect(self.move_objects)
        self.btn_transport.setEnabled(False)

        self.btn_restart = QPushButton("Начать сначала", self)
        self.btn_restart.setGeometry(280, 130, 100, 30)
        self.btn_restart.clicked.connect(self.restart_game)
        self.btn_restart.setVisible(False)

        self.initialize_game()

    def initialize_game(self):
        self.left_bank = {"wolf", "goat", "cabbage"}  # Начальное состояние левого берега
        self.right_bank = set()  # Правый берег пустой
        self.boat = set()  # Лодка пуста
        self.status_label.setText("Перевезите волка, козу и капусту на другой берег, нажимая на объект, затем 'Перевезти'.")
        self.btn_transport.setEnabled(False)
        self.btn_restart.setVisible(False)

    def put_in_boat(self, obj):
        if obj in self.left_bank:
            if len(self.boat) < 2:  # Проверяем, есть ли свободное место на лодке
                self.left_bank.remove(obj)
                self.boat.add(obj)
                self.status_label.setText(f"Объект {obj.capitalize()} посажен в лодку.")
                self.btn_transport.setEnabled(True)
            else:
                self.status_label.setText("Лодка уже занята!")
        else:
            self.status_label.setText(f"Объект {obj.capitalize()} на противоположном берегу.")

    def move_objects(self):
        if self.boat:
            for obj in self.boat:
                self.right_bank.add(obj)
            self.boat.clear()
            self.btn_transport.setEnabled(False)
            self.check_game_status()
        else:
            self.status_label.setText("Лодка пуста. Сначала посадите объект в лодку.")

    def check_game_status(self):
        if not self.left_bank and not self.boat:  # Если левый берег и лодка пусты, игрок выиграл
            self.status_label.setText("Поздравляем! Вы выиграли!")
            return

        if ("goat" in self.left_bank and "cabbage" in self.left_bank) or \
           ("goat" in self.right_bank and "cabbage" in self.right_bank):  # Проверяем условие поражения
            self.status_label.setText("Неверный ход! Коза съела капусту. Попробуйте еще раз.")
            self.btn_restart.setVisible(True)
        else:
            self.status_label.setText("Выберите объект для перемещения.")

    def restart_game(self):
        self.initialize_game()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
