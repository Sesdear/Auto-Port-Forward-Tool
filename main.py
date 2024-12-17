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
        self.ui.removeButton.clicked.connect(self.removeButton_click)
        self.ui.refreshConsoleButton.clicked.connect(self.refreshButton_click)

        self.updateConsole()


    def refreshButton_click(self):
        self.updateConsole()
    def addButton_click(self):
        listenaddress = self.ui.add_listenAddressLineEdit.text()
        listenport = self.ui.add_listenPortLineEdit.text()
        connectaddress = self.ui.add_connectAddressLineEdit.text()
        connectport = self.ui.add_connectPortLineEdit.text()

        print(listenaddress, listenport, connectaddress, connectport)

        if self.ui.addFirewallcheck.isChecked():
            command_firewall = f"netsh advfirewall firewall add rule name='AFP_Tcp{listenport}' protocol=TCP localport={listenport} action=allow"
            os.system(command_firewall)

        command = f"netsh interface portproxy add v4tov4 listenaddress={listenaddress} listenport={listenport} connectaddress={connectaddress} connectport={connectport}"
        os.system(command)
        self.updateConsole()

    def removeButton_click(self):
        listenaddress = self.ui.add_listenAddressLineEdit.text()
        listenport = self.ui.add_listenPortLineEdit.text()
        command_layout = f"netsh interface portproxy delete v4tov4 listenaddress={listenaddress} listenport={listenport}"
        os.system(command_layout)
        self.updateConsole()

    def updateConsole(self):
        command_update = "netsh interface portproxy show all"
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