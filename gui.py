import exif_read_module

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMainWindow,QVBoxLayout, QPushButton, QWidget, QMessageBox, QLabel, QLineEdit, QDialog, QDialogButtonBox

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


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.target_folder = None
        self.file_name = None

        self.setWindowTitle("PhotoJourney")
        self.setWindowIcon(QIcon('D:\Projects\photograph_journey\icon.png'))

        self.button_sel = QPushButton("Select Folder")
        self.button_start = QPushButton("Start Counting")
        self.display_folder = QLabel("No Folder Selected")

        self.font = self.display_folder.font()
        self.font.setPointSize(12)
        self.display_folder.setFont(self.font)
        self.display_folder.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.button_sel.clicked.connect(self.the_botton_sel_clicked)
        self.button_start.clicked.connect(self.the_botton_start_clicked)


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
            self.file_name = dlg.filename


    def the_botton_start_clicked(self):
        func = exif_read_module.exif_reader()
        if self.target_folder is not None:
            self.show_dialog_input_file_name()
            func.file_name = self.file_name
            func.output_path = self.show_dialog_select_folder()
            if func.file_name is not None and func.output_path is not None:
                func.reader(self.target_folder)
                if func.count == 0:
                    self.finish_message(0)
                else:
                    self.finish_message(func.count)
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
        

