import exif_read_module

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QFileDialog, QMainWindow,QVBoxLayout, QPushButton, QWidget, QMessageBox, QLabel, QLineEdit, QDialog, QDialogButtonBox, QTextBrowser

class FileNameInput(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter the file name")
        
        self.label = QLabel("Please enter the name for the output file,\nthen select the path for the file in the following window")

        self.line_edit = QLineEdit()
        self.line_edit.textEdited.connect(self.text_edited)

        self.button = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(self.button)
        self.buttonBox.accepted.connect(self.accept)
        self.filename = None


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.setFixedSize(QtCore.QSize(800, 300))

    def text_edited(self, s):
        self.filename = s

class ReadMainWindow(QDialog):
    def __init__(self, fn, op, tf):
        super().__init__()
        self.setWindowTitle("Analyze Status")

        self.target_folder = tf
        self.file_name = fn
        self.output_path = op
        self.func = exif_read_module.exif_reader(self, self.file_name, self.output_path)

        self.label = QLabel("The file being read:")
        self.label.setFont(QFont('Arial'))
        self.button_start = QPushButton("Start")
        self.browser_label = QTextBrowser()

        self.button = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(self.button)
        self.buttonBox.accepted.connect(self.accept)

        self.button_start.clicked.connect(self.button_clicked)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button_start)
        self.layout.addWidget(self.browser_label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.setFixedSize(QtCore.QSize(1024, 768))

    def button_clicked(self):
        self.func.reader(self.target_folder)



class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.target_folder = None

        self.setWindowTitle("PhotoJourney")
        self.setWindowIcon(QIcon('D:\Projects\photograph_journey\icon.png'))

        self.button_sel = QPushButton("Select Folder")
        self.button_sel.setFont(QFont('Arial'))
        self.button_start = QPushButton("Start Counting")
        self.button_start.setFont(QFont('Arial'))
        self.display_folder = QLabel("No Folder Selected")

        self.display_folder.setFont(QFont('Arial', 12))
        self.display_folder.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.button_sel.clicked.connect(self.the_botton_sel_clicked)
        self.button_start.clicked.connect(self.the_botton_start_clicked)

        self.file_been_read = None

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button_sel)
        self.layout.addWidget(self.display_folder)
        self.layout.addWidget(self.button_start)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setFixedSize(QtCore.QSize(800, 600))
        self.setCentralWidget(self.widget)
        

    def show_dialog_select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Open Folder', "C:\\", QFileDialog.ShowDirsOnly)
        return folder
    
    def the_botton_sel_clicked(self):
        self.target_folder= self.show_dialog_select_folder()
        self.display_folder.setText("Selected Folder: %s" % self.target_folder)

    def show_dialog_input_file_name(self):
        dlg = FileNameInput()
        if dlg.exec():
            return dlg.filename


    def the_botton_start_clicked(self):
        # func = exif_read_module.exif_reader()
        if self.target_folder is not None:
            file_name = self.show_dialog_input_file_name()
            output_folder = self.show_dialog_select_folder()
            func = ReadMainWindow(file_name, output_folder, self.target_folder)
            if func.file_name is not None and func.output_path is not None:
                if func.exec():
                    if func.func.count == 0:
                        self.finish_message(0)
                    else:
                        self.finish_message(func.func.count)
            else:
                self.finish_message(-1)
        else:
            self.finish_message(-1)
            


    def finish_message(self, count):
        if count == 0:
            QMessageBox.warning(self, "Error", "No supported image found in your folder!")
        elif count == -1:
            QMessageBox.warning(self, "Error", "Please select a folder or specify the file name!")
        else:
            QMessageBox.information(self, "Notice", "%d image(s) have been counted" % count)
        

