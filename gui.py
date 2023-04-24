import exif_read_module

from math import pow

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QFileDialog, QMainWindow,QVBoxLayout, QPushButton, QWidget, QMessageBox, QLabel, QLineEdit, QDialog, QDialogButtonBox, QTextBrowser, QCheckBox


class FileNameInputWindow(QDialog):
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


class ReaderMenu(QDialog):
    def __init__(self, fn, op, tf, opt):
        super().__init__()

        self.file_name = fn
        self.output_path = op
        self.target_folder = tf
        self.option = opt

        self.setWindowTitle("Analyze Status")

        self.func = exif_read_module.exif_reader(self, self.file_name, self.output_path, self.option)

        self.label = QLabel("The file being read:")
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
        self.setFixedSize(QtCore.QSize(1280, 768))

    def button_clicked(self):
        self.func.reader(self.target_folder)



class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.target_folder = None

        self.setWindowTitle("PhotoJourney")
        self.setWindowIcon(QIcon('D:\Projects\photograph_journey\icon.png'))

        self.button_sel_folder = QPushButton("Select Folder")
        self.button_start = QPushButton("Start Counting")
        self.display_folder = QLabel("No Folder Selected")

        self.display_folder.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.metadata_label = QLabel("Please choose the metadata you want to analyze.")

        self.check_status = [1, 1, 1, 1]

        self.checkbox_layout = QVBoxLayout()
        self.sel_focal = QCheckBox("Focal Length")
        self.sel_focal.setCheckState(QtCore.Qt.Checked)
        self.sel_focal.stateChanged.connect(lambda: self.change_state(self.sel_focal.isChecked(), 3))

        self.sel_aperature = QCheckBox("F Stops")
        self.sel_aperature.setCheckState(QtCore.Qt.Checked)
        self.sel_aperature.stateChanged.connect(lambda: self.change_state(self.sel_aperature.isChecked(), 2))

        self.sel_camera = QCheckBox("Camera Model")
        self.sel_camera.setCheckState(QtCore.Qt.Checked)
        self.sel_camera.stateChanged.connect(lambda: self.change_state(self.sel_camera.isChecked(), 1))

        self.sel_lensmodel = QCheckBox("Lens Model")
        self.sel_lensmodel.setCheckState(QtCore.Qt.Checked)
        self.sel_lensmodel.stateChanged.connect(lambda: self.change_state(self.sel_lensmodel.isChecked(), 0))

        self.checkbox_layout.addWidget(self.sel_focal)
        self.checkbox_layout.addWidget(self.sel_aperature)
        self.checkbox_layout.addWidget(self.sel_camera)
        self.checkbox_layout.addWidget(self.sel_lensmodel)

        self.button_sel_folder.clicked.connect(self.the_botton_sel_clicked)
        self.button_start.clicked.connect(self.the_botton_start_clicked)

        self.file_been_read = None

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button_sel_folder)
        self.layout.addWidget(self.metadata_label)
        self.layout.addLayout(self.checkbox_layout)
        self.layout.addWidget(self.display_folder)
        self.layout.addWidget(self.button_start)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setFixedSize(QtCore.QSize(800, 600))
        self.setCentralWidget(self.widget)
        

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Open Folder', "C:\\", QFileDialog.ShowDirsOnly)
        return folder
    
    def the_botton_sel_clicked(self):
        self.target_folder= self.select_folder()
        self.display_folder.setText("Selected Folder: %s" % self.target_folder)

    def name_file(self):
        dlg = FileNameInputWindow()
        if dlg.exec():
            return dlg.filename


    def the_botton_start_clicked(self):
        
        def bin2dec(arr):
            n = 0
            for i in range(0, 4):
                n += arr[i] * pow(2, i)
            return n


        if self.target_folder is not None:
            file_name = self.name_file()
            output_folder = self.select_folder()
            opt = int(bin2dec(self.check_status))
            print(opt)
            reader_menu = ReaderMenu(file_name, output_folder, self.target_folder, opt)
            if reader_menu.file_name is not None and reader_menu.output_path is not None:
                if reader_menu.exec():
                    if reader_menu.func.count == 0:
                        self.notice(0)
                    else:
                        self.notice(reader_menu.func.count)
            else:
                self.notice(-1)
        else:
            self.notice(-1)
            


    def notice(self, count):
        if count == 0:
            QMessageBox.warning(self, "Error", "No supported image in your folder!")
        elif count == -1:
            QMessageBox.warning(self, "Error", "Please select a folder or name the output file!")
        else:
            QMessageBox.information(self, "Notice", "%d image(s) have been counted" % count)
        
    def change_state(self, s, n):
        self.check_status[n] = s
        print(self.check_status[n])
