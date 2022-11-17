from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot
from software import Network
import subprocess


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.icon = 'wifi.ico'
        self.__select_text = '--select--'

        # App Window
        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle('Network Config')
        self.setGeometry(800, 450, 300, 250)  # X, Y, W, H
        self.setFixedWidth(300)
        self.setFixedHeight(250)

        # Canvas
        stylesheet = ('''
            QWidget {
                font-size: 16px;
            }

            QPushButton {
                font-size: 20px;
            }
        ''')
        self.setStyleSheet(stylesheet)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # widgets

        # Interface Alias Dropdown
        interface_alias_label = QLabel('Select Interface Alias')
        self.interface_alias = QComboBox()
        self.interface_alias.addItem(self.__select_text)
        self.interface_alias.addItems(self.__get_interface_indices())

        # Network Category Dropdown
        net_cat_label = QLabel('Select Network Category')
        self.net_cat = QComboBox()
        self.net_cat.addItem(self.__select_text)
        self.net_cat.addItems(['public', 'private'])
        # self.net_cat.setDisabled(True)

        self.convert_button = QPushButton('Convert')
        # self.convert_button.setDisabled(True)

        self.reset_button = QPushButton('Reset')

        self.status_label = QLabel()

        # Add widgets to layout
        layout.addWidget(interface_alias_label)
        layout.addWidget(self.interface_alias)
        layout.addWidget(net_cat_label)
        layout.addWidget(self.net_cat)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.status_label)

        # self.on_combo_box_current_value_changed(0)

        self.convert_button.clicked.connect(self.__change_network_category)
        self.reset_button.clicked.connect(self.__reset_app)

    def __reset_app(self):
        self.interface_alias.setCurrentIndex(0)
        self.net_cat.setCurrentIndex(0)
        self.__display_status('')

    def __change_network_category(self):
        interface_alias = self.interface_alias.currentText()
        net_cat = self.net_cat.currentText()
        net = Network()
        res = net.change_network_category(interface_alias=interface_alias, network_category_change_to=net_cat)
        if res:
            self.__display_status(f'Converted {interface_alias} to {net_cat}')
        else:
            self.__display_status('ERROR!')

    def __get_interface_indices(self):
        result = subprocess.run(['powershell', '-Command', 'Get-NetConnectionProfile'], capture_output=True)
        lines = result.stdout.splitlines()
        lines = [str(x, 'UTF-8') for x in lines]
        values = []
        for line in lines:
            if 'InterfaceAlias' in line:
                values.append(line.split(':')[-1].strip())
        return values

    def __display_status(self, msg: str):
        self.status_label.setText(msg)

    @pyqtSlot(int)
    def on_combo_box_current_value_changed(self, index):
        if index > 0:
            self.net_cat.setDisabled(False)
            self.convert_button.setDisabled(False)
