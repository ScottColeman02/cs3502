from pathlib import Path
import re
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QLineEdit, QFrame
import sys
import os
from FileManager import FileManager as fm
from PopUps import DeleteFilePopUp, CreateDirPopUp, RenamePopUp, ErrorPopUp


class MyWindow(QMainWindow):
    def __init__(self):
       super(MyWindow, self).__init__()

       self.fm = fm()
       self.deleteFilePopup = DeleteFilePopUp()
       self.createDirPopup = CreateDirPopUp()
       self.renamePopup = RenamePopUp()
       self.errorPopup = ErrorPopUp()
       self.deletingDir = False

       self.supportedFileTypes = {".txt", ".html", ".htm", ".md", ""}


       #Load in the .ui file generate in QtDesigner containing the GUI
       uic.loadUi("C:\\Users\Admin\OneDrive - Kennesaw State University\Fall 2025\Operating Systems\Project3_GUI\p3GUI.ui",self)

       #Create the file listing window
       self.model = QFileSystemModel()
       self.model.setRootPath("")
       self.fileListing.setModel(self.model)
       self.fileListing.setRootIndex(self.model.index(""))
       self.fileListing.setColumnWidth(0,250)

       #set the currently selected file
       self.fileListing.selectionModel().selectionChanged.connect(self.selectFile)


       self.createButton.clicked.connect(self.clickedCreate)
       self.confirmCreate.clicked.connect(self.clickedConfirmCreate)
       self.displayButton.clicked.connect(self.clickedDisplay)
       self.updateButton.clicked.connect(self.clickedUpdate)
       self.confirmUpdateButton.clicked.connect(self.clickedConfirmUpdate)
       self.deleteButton.clicked.connect(self.clickedDelete)
       self.deleteFilePopup.confirmDeleteButton.clicked.connect(self.clickedConfirmDelete)
       self.deleteFilePopup.cancelDeleteButton.clicked.connect(self.clickedCancelDelete)
       self.createDirButton.clicked.connect(self.clickedCreateDirButton)
       self.createDirPopup.confirmCreateDir.clicked.connect(self.clickedConfirmCreateDir)
       self.deleteDirButton.clicked.connect(self.clickedDeleteDir)
       self.renameButton.clicked.connect(self.clickedRenameButton)
       self.renamePopup.confirmNewNameButton.clicked.connect(self.clickedConfirmRename)
       self.renamePopup.cancelRenameButton.clicked.connect(self.clickedCancelRename)
       self.homeButton.clicked.connect(self.clickedHome)
       self.helpButton.clicked.connect(self.clickedHelpButton)
       self.errorPopup.okButton.clicked.connect(self.clickedErrorOk)




    #Method to set the currently selected file
    def selectFile(self, selected, deselected):
        index = self.fileListing.currentIndex()
        path = self.model.filePath(index)

        self.selectedFile = None
        self.selectedDir = None

        if os.path.isfile(path):
            self.selectedFile = path
            self.current_path = os.path.dirname(path)
        else:
            self.selectedDir = path
            self.current_path = path

        if not os.path.isdir(self.current_path):
            self.current_path = os.path.dirname(self.current_path)

        self.pathSegments = Path(path).parts
        self.currFile.setText(os.path.basename(path))


    def clickedHome(self):
        self.stackedWidget.setCurrentIndex(0)


    def clickedHelpButton(self):
        self.stackedWidget.setCurrentIndex(4)

    #Action listener for the create a file button
    def clickedCreate(self):
        self.confirmCreateLabel.clear()
        index = self.fileListing.currentIndex()

        if not index.isValid():
            self.errorPopup.errorDescription.setText("No directory selected. Please make a selection")
            self.errorPopup.exec_()
            return

        path = self.model.filePath(index)

        if Path(path).is_file():
            self.errorPopup.errorDescription.setText("A file is currently selected. Please select a directory.")
            self.errorPopup.exec_()
            return

        if path == "":
            self.errorPopup.errorDescription.setText("The file listing root is selected. Please select a directory.")
            self.errorPopup.exec_()
            return

        self.fileNameInput.clear()
        self.contentsInput.clear()
        self.stackedWidget.setCurrentIndex(1)


    def clickedConfirmCreate(self):
        fileName = self.fileNameInput.text().strip()

        if not self.validName(fileName):
            self.errorPopup.errorDescription.setText("Invalid file name.")
            self.errorPopup.exec_()
            return

        fullPath = os.path.join(self.current_path, fileName)

        try:
            self.fm.createFile(fullPath, self.contentsInput.toHtml())
        except(FileNotFoundError, PermissionError, OSError) as e:
            self.errorPopup.errorDescription.setText(f"Issue creating file: {e}")
            self.errorPopup.exec_()
            return


        p = Path(fullPath)
        if p.exists():
            self.confirmCreateLabel.setText("File successfully created!")


    #Action listener for display file button
    def clickedDisplay(self):
        index = self.fileListing.currentIndex()

        if not index.isValid():
            self.errorPopup.errorDescription.setText("No file selected. Please make a selection")
            self.errorPopup.exec_()
            return

        path = self.model.filePath(index)

        if Path(path).is_dir():
            self.errorPopup.errorDescription.setText("A directory is currently selected. Please select a file.")
            self.errorPopup.exec_()
            return

        if not self.validFileType(path):
            self.errorPopup.errorDescription.setText("Invalid file type selected. Please see Display File Help menu for supported file types.")
            self.errorPopup.exec_()
            return

        if path == "":
            self.errorPopup.errorDescription.setText("The file listing root is selected. Please select a file.")
            self.errorPopup.exec_()
            return

        self.displayTitle.clear()
        self.stackedWidget.setCurrentIndex(2)

        fileContents = self.fm.readFile(self.selectedFile)


        self.displayTitle.setText("Displaying: "+os.path.basename(path))
        self.fileDisplayWindow.setHtml(fileContents)


    #Action listener for update file button
    def clickedUpdate(self):
        self.updateInput.clear()
        self.confirmUpdateLabel.clear()

        index = self.fileListing.currentIndex()

        if not index.isValid():
            self.errorPopup.errorDescription.setText("No file selected. Please make a selection")
            self.errorPopup.exec_()
            return

        path = self.model.filePath(index)

        if Path(path).is_dir():
            self.errorPopup.errorDescription.setText("A directory is currently selected. Please select a file.")
            self.errorPopup.exec_()
            return

        if not self.validFileType(path):
            self.errorPopup.errorDescription.setText("Invalid file type selected. Please see Update File Help menu for supported file types.")
            self.errorPopup.exec_()
            return

        if path == "":
            self.errorPopup.errorDescription.setText("The file listing root is selected. Please select a file.")
            self.errorPopup.exec_()
            return

        self.updateTitle.clear()
        self.stackedWidget.setCurrentIndex(3)

        self.updateTitle.setText("Updating: "+os.path.basename(path))


    def clickedConfirmUpdate(self):
        newContent = self.updateInput.toHtml()
        self.confirmUpdateLabel.setText("File successfully updated!")
        self.fm.updateFile(self.selectedFile, newContent)

    #Action listener for delete file button
    def clickedDelete(self):
        index = self.fileListing.currentIndex()

        if not index.isValid():
            self.errorPopup.errorDescription.setText("No file selected. Please make a selection")
            self.errorPopup.exec_()
            return

        path = self.model.filePath(index)

        if Path(path).is_dir():
            self.errorPopup.errorDescription.setText("A directory is currently selected. Please select a file or choose Delete Directory.")
            self.errorPopup.exec_()
            return

        self.deletingDir = False
        self.deleteFilePopup.deleteName.setText(os.path.basename(path))
        self.deleteFilePopup.exec_()

    def clickedConfirmDelete(self):
        if self.deletingDir:
            self.fm.deleteDir(self.selectedDir)
        else:
            self.fm.deleteFile(self.selectedFile)

        self.deleteFilePopup.reject()

    def clickedCancelDelete(self):
        self.deleteFilePopup.reject()

    def clickedCreateDirButton(self):
        index = self.fileListing.currentIndex()

        if not index.isValid():
            self.errorPopup.errorDescription.setText("No parent directory selected. Please make a selection")
            self.errorPopup.exec_()
            return

        path = self.model.filePath(index)

        if Path(path).is_file():
            self.errorPopup.errorDescription.setText("A file is currently selected. Please select a directory")
            self.errorPopup.exec_()
            return

        self.createDirPopup.exec_()

    def clickedConfirmCreateDir(self):
        #index = self.fileListing.currentIndex()
        #path = self.model.filePath(index)

        dirName = self.createDirPopup.dirNameInput.text().strip()
        fullPath = os.path.join(self.current_path, dirName)

        self.fm.createDir(fullPath)
        self.createDirPopup.reject()

    def clickedDeleteDir(self):
        index = self.fileListing.currentIndex()

        if not index.isValid():
            self.errorPopup.errorDescription.setText("No directory selected. Please make a selection")
            self.errorPopup.exec_()
            return

        path = self.model.filePath(index)
        self.deletingDir = True
        self.deleteFilePopup.deleteName.setText(os.path.basename(path))
        self.deleteFilePopup.exec_()


    def clickedRenameButton(self):
        self.renamePopup.newNameInput.clear()
        index = self.fileListing.currentIndex()

        if not index.isValid():
            self.errorPopup.errorDescription.setText("No file or directory selected. Please make a selection")
            self.errorPopup.exec_()
            return

        self.renamePopup.exec_()

    def clickedConfirmRename(self):
        newName = self.renamePopup.newNameInput.text().strip()

        if not self.validName(newName):
            self.errorPopup.errorDescription.setText("Invalid file name.")
            self.errorPopup.exec_()
            return

        file2BRenamed = None

        if self.selectedFile:
            file2BRenamed = self.selectedFile
        elif self.selectedDir:
            file2BRenamed = self.selectedDir
        else:
            self.errorPopup.errorDescription.setText("No selection made. Please select a file or directory")
            self.errorPopup.exec_()
            return

        parentDirectory = os.path.dirname(file2BRenamed)
        fullPath = os.path.join(parentDirectory, newName)

        try:
            self.fm.rename(file2BRenamed,fullPath)

        except Exception as e:
            self.errorPopup.errorDescription.setText(f"Issue renaming: {e}")
            self.errorPopup.exec_()
            return
        self.renamePopup.reject()
    def clickedCancelRename(self):
        self.renamePopup.reject()


    def clickedErrorOk(self):
        self.errorPopup.reject()


    #Validate file name
    def validName(self,name):
        return bool(name) and not re.search(r'[<>:"/\\|?*]',name)

    #Validate file type
    def validFileType(self, path):
        fileType = os.path.splitext(path)[1].lower()
        return fileType in self.supportedFileTypes

def window():
    app = QApplication(sys.argv)
    wind = MyWindow()
    wind.show()
    sys.exit(app.exec())

window()