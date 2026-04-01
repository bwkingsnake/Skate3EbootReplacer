from pathlib import Path
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from Dependencies.GUI.mainUI import Ui_MainWindow

from Dependencies.PythonUtilities.ConfigManager import ConfigManager
from Dependencies.PythonUtilities.EbootManager import EbootManager
from Dependencies.PythonUtilities.GamePathManager import GamePathManager

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

class MainWindow(QMainWindow):
    def __init__(self, BASE_PATH):
        super().__init__()
        self.BASE_PATH = BASE_PATH
        
        #setupGUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(str(BASE_PATH / "Dependencies" / "Images" / "skate3logo.png")))
        self.setWindowTitle("BWKingsnakes EBOOT Changer")
        self.ui.pathLineEdit.setReadOnly(True)
        self.connectSignalsToSlots()

        #Logic
        self.configManager = ConfigManager(self.BASE_PATH / "config.json")
        self.ebootmanager = EbootManager(self.BASE_PATH / "Eboots")
        self.eboots = self.ebootmanager.GetEboots()

        self.ConfigRpcs3Path = self.configManager.getRPCS3Path()
        
        if self.eboots != None:
            self.updateComoBox(self.eboots)
        
        if self.ConfigRpcs3Path != None:
            print("Loading Config Path")
            self.updatePathLineEdit(self.ConfigRpcs3Path)
        
    def connectSignalsToSlots(self):
        self.ui.BrowseButton.clicked.connect(self.browseButtonClicked)
        self.ui.apllyButton.clicked.connect(self.applyButtonClicked)
    
    def updateComoBox(self, eboots : list):
        ebootNames = []
        for name in eboots:
            ebootNames.append(name)
        
        self.ui.comboBox.addItems(ebootNames)

    def getRpcs3Path(self)-> None | Path:
        try:
            rpcs3Path = QFileDialog.getOpenFileName(parent=self,caption="Select RPCS3.exe", filter=("Executable Files (*.exe)"))[0]
            newFilePath = rpcs3Path.replace("/rpcs3.exe", "")
            if rpcs3Path:
                return Path(newFilePath)
            else:
                return None
        except Exception as e:
            print(f"ERROR getting the rpcs3 path :{e}")
            return None
    
    def popUp(self,text : str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.NoIcon)  
        msg.exec_()

    def updatePathLineEdit(self, text):
        self.ui.pathLineEdit.setText(str(text))

    def browseButtonClicked(self):
        rpcs3Path = self.getRpcs3Path()
        if rpcs3Path != None:
            self.updatePathLineEdit(rpcs3Path)
            self.ConfigRpcs3Path = rpcs3Path
            print(f"updating JSON with {rpcs3Path}")
            self.configManager.dumpJsonFile(str(rpcs3Path))
        else:
            self.popUp("Please select your rpcs3 path pwetty pwease owo :3")
    
    def applyButtonClicked(self):

        ebootName = (self.ui.comboBox.currentText())
        ebootPath = Path(self.eboots[ebootName])
    
        if self.ConfigRpcs3Path != None:
            gamePathManager = GamePathManager(Path(self.ConfigRpcs3Path))
            gameEbootPaths = gamePathManager.getSkate3RomEbootPaths()
            if gameEbootPaths != None:
                for path in gameEbootPaths:
                    print(f"replacing ({path}) with {ebootName}")
                    self.ebootmanager.copyEboot(ebootPath, path)
        else:
            self.popUp("Please select your rpcs3 path pwetty pwease owo :3")
    
def main():

    BASE_PATH = get_base_path()

    app = QApplication(sys.argv)     
    window = MainWindow(BASE_PATH)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()