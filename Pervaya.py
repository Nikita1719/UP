import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_location = {'farmer': 'left', 'sheep': 'left', 'wolf': 'left', 'cabbage': 'left'}

    def initUI(self):
        self.setWindowTitle('Игра "Овца, капуста, коза и волк"')
        self.message = QLabel('Переведите всех на другой берег без потерь')
        self.button_move = QPushButton('Перевести')
        self.button_move.clicked.connect(self.move_action)

        layout = QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(self.button_move)
        self.setLayout(layout)

    def move_action(self):
        farmer_pos = self.current_location['farmer']
        sheep_pos = self.current_location['sheep']
        wolf_pos = self.current_location['wolf']
        cabbage_pos = self.current_location['cabbage']

        if (sheep_pos == 'left' and cabbage_pos == 'left' and farmer_pos == 'left') or \
           (sheep_pos == 'right' and cabbage_pos == 'right' and farmer_pos == 'right'):
            self.message.setText('Нельзя оставлять овцу с капустой одних!')
        elif (sheep_pos == 'left' and wolf_pos == 'left' and farmer_pos == 'left') or \
             (sheep_pos == 'right' and wolf_pos == 'right' and farmer_pos == 'right'):
            self.message.setText('Нельзя оставлять овцу с волком одних!')
        else:
            self.current_location['farmer'] = 'right' if farmer_pos == 'left' else 'left'
            self.current_location['sheep'] = 'right' if sheep_pos == 'left' else 'left'
            self.current_location['wolf'] = 'right' if wolf_pos == 'left' else 'left'
            self.current_location['cabbage'] = 'right' if cabbage_pos == 'left' else 'left'

            if self.current_location == {'farmer': 'right', 'sheep': 'right', 'wolf': 'right', 'cabbage': 'right'}:
                self.message.setText('Поздравляю! Все участники перевезены без потерь!')
            else:
                self.message.setText('Успешно перевезено на другой берег!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
