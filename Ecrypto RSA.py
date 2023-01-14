from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os, rsa
from PyQt5.QtCore import Qt

class EncryptoRSA(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ul/crypto.xml', self)
        self.random_key_button.clicked.connect(self.create_keys)
        self.load_public_key_button.clicked.connect(self.load_public_key)
        self.load_private_key_button.clicked.connect(self.load_private_key)
        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)
        self.save_result.clicked.connect(self.save_text)
        self.load_result.clicked.connect(self.load_text)

        

    def load_text(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Text", "","Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                text = f.read()
                self.input.setText(text)


    def create_keys(self):
        public_key_file = 'key.public'
        private_key_file = 'key.private'
        if os.path.exists(public_key_file) or os.path.exists(private_key_file):
            answer = QtWidgets.QMessageBox.question(self, "Replace Keys", "A public or private key already exists, do you want to replace it?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.No:
                return
        (public_key, private_key) = rsa.newkeys(2048)
        with open(public_key_file, 'wb') as f:
            f.write(public_key.save_pkcs1())
        with open(private_key_file, 'wb') as f:
            f.write(private_key.save_pkcs1())

    def load_public_key(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_public, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Public Key", "","Public Key Files (*.public);;All Files (*)", options=options)
        if file_public:
            with open(file_public, 'rb') as f:
                self.public_key = rsa.PublicKey.load_pkcs1(f.read())
                self.public_key_filename.setText(os.path.basename(file_public))
                

    def load_private_key(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_private, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Private Key", "","Private Key Files (*.private);;All Files (*)", options=options)
        if file_private:
            with open(file_private, 'rb') as f:
                self.private_key = rsa.PrivateKey.load_pkcs1(f.read())
                self.private_key_filename.setText(os.path.basename(file_private))

    def save_text(self):
        result = self.result.text()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save result", "result.txt", "text files (*.txt)")
        if filename:
            with open(filename, "w") as f:
                f.write(result)

    def encrypt(self):
        try:
            if not hasattr(self, 'public_key'):
                self.result.setText("Please select a public key first")
                return
            message = self.input.text().encode('utf-8')
            encrypted_data = rsa.encrypt(message, self.public_key)
            self.result.setText(encrypted_data.hex())
        except:
            self.result.setText("Failed to encrypt")

    def decrypt(self):
        try:
            if not hasattr(self, 'private_key'):
                self.result.setText("Please select a private key first")
                return
            encrypted_data = bytes.fromhex(self.input.text())
            decrypted_data = rsa.decrypt(encrypted_data, self.private_key).decode('utf-8')
            self.result.setText(decrypted_data)
        except:
            self.result.setText("Failed to decrypt message")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = EncryptoRSA()
    window.show()
    app.exec_()
