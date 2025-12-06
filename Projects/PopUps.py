from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class DeleteFilePopUp(QDialog):
    def __init__(self):
        super(DeleteFilePopUp,self).__init__()
        uic.loadUi("C:\\Users\Admin\OneDrive - Kennesaw State University\Fall 2025\Operating Systems\Project3_GUI\deleteFilePopup.ui",self)

class CreateDirPopUp(QDialog):
    def __init__(self):
        super(CreateDirPopUp,self).__init__()
        uic.loadUi("C:\\Users\Admin\OneDrive - Kennesaw State University\Fall 2025\Operating Systems\Project3_GUI\createDirPopup.ui",self)

class RenamePopUp(QDialog):
    def __init__(self):
        super(RenamePopUp,self).__init__()
        uic.loadUi("C:\\Users\Admin\OneDrive - Kennesaw State University\Fall 2025\Operating Systems\Project3_GUI\\renamePopup.ui",self)

class ErrorPopUp(QDialog):
    def __init__(self):
        super(ErrorPopUp,self).__init__()
        uic.loadUi("C:\\Users\Admin\OneDrive - Kennesaw State University\Fall 2025\Operating Systems\Project3_GUI\errorPopup.ui",self)
