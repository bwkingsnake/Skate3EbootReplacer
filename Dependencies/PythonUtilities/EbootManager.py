from pathlib import Path
from os import listdir
import shutil

class EbootManager:
    def __init__(self, ebootFolderPath : Path):
        self.ebootFolderPath = ebootFolderPath
    
    def GetEboots(self)-> dict | None:

        Eboots = {}

        try:
            files = listdir(self.ebootFolderPath)
        except Exception as e:
            print(f"error getting eboots {e}")
            return None

        for file in files:
            Eboots[file] = Path(self.ebootFolderPath / file)
        
        return Eboots
    
    def copyEboot(self, Eboot : Path, outPutPath : Path):
        try:
            shutil.copy(Eboot, outPutPath)
        except Exception as e:
            print(f"failed to copy eboot {e}")
            


