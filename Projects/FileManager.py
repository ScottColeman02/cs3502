import os
import shutil
from pathlib import Path
from tkinter.messagebox import showerror

class FileManager:
    #Method to create a new file
    def createFile(self,path,content):
        try:
            with open(path, 'w') as f:
                f.write(content)
        except Exception as e:
            raise e


    #Method to read a file
    def readFile(self, path):
        p = Path(path)
        if not p.exists():
            return None

        try:
            with open(path, 'r') as f:
                content = f.read()
                return content
        except Exception as e:
            showerror("Error",str(e))
            return None


    #Method to update a file
    def updateFile(self, path, newContent):
        with open(path, 'w') as f:
            f.write(newContent)



    #Method to delete a file
    def deleteFile(self, path):
        try:
            os.remove(path)
        except PermissionError:
            raise self.shower
    def deleteDir(self, path):
        if any(Path(path).iterdir()):
            shutil.rmtree(path)
        else:
            os.rmdir(path)

    #Method to create a new directory
    def createDir(self,path):
        os.mkdir(path)

    #Method to rename file or directory
    def rename(self,oldName,newName):
        os.rename(oldName,newName)