import os
import subprocess
import sys
from PyQt6.QtWidgets import QApplication, QFrame
from PyQt6 import uic

class Window(QFrame):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("afp.ui", self)
        self.show()

        self.ui.addButton.clicked.connect(self.addButton_click)
        self.ui.refreshConsoleButton.clicked.connect(self.refreshButton_click)

        self.updateConsole()

    def refreshButton_click(self):
        self.updateConsole()

    def addButton_click(self):
        address = self.ui.add_AddressLineEdit.text()
        port = self.ui.add_PortLineEdit.text()

        print(address, port)

        if self.ui.iptablesRadioButton.isChecked():
            # Проброс с помощью iptables
            command_firewall = f"sudo iptables -A INPUT -p tcp --dport {port} -j ACCEPT"
            os.system(command_firewall)

            command_portproxy = f"sudo iptables -t nat -A PREROUTING -p tcp -d {address} --dport {port} -j DNAT --to-destination {address}:{port}"
            os.system(command_portproxy)

        elif self.ui.nftablesRadioButton.isChecked():
            # Проброс с помощью nftables
            command_nft = f"sudo nft add rule ip nat prerouting tcp dport {port} dnat to {address}:{port}"
            os.system(command_nft)

        self.updateConsole()

    def updateConsole(self):
        command_update = "sudo iptables -t nat -L -n -v"
        self.ui.ConsoleOutput.setText("")
        result = subprocess.run(command_update, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            self.ui.ConsoleOutput.setText(result.stdout)
        else:
            self.ui.ConsoleOutput.setText(f"Ошибка: {result.stderr}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
