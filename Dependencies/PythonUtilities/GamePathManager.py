from pathlib import Path
from .gamePath import GameEbootPaths

class GamePathManager:
    def __init__(self, rpcs3Path : Path):
        self.rpcs3Path = rpcs3Path
        self.gamesConfigPath = Path(rpcs3Path / "config" / "games.yml")
    
    def getAllGamePaths(self)-> list:
        unresolvedPaths = []
        unresolvedPaths.append(self.resolveEbootPaths("BLUS30464"))
        unresolvedPaths.append(self.resolveEbootPaths("BLES00760"))

        paths = []
        for path in unresolvedPaths:
            if path != None:
                paths.append(path)
        
        return paths
        
    
    def resolveEbootPaths(self, target :str) -> GameEbootPaths | None:

        gameEbootPaths = GameEbootPaths()
        gameEbootPaths.name = target
        romPath = self.resolveRomPath(target)

        if romPath != None:
            romEbootPath = Path(romPath / "PS3_GAME" / "USRDIR" / "EBOOT.BIN")
            if romEbootPath.exists():
                gameEbootPaths.ebootDiskPath = romEbootPath
        
        ebootInstallPath = self.resolveInstallPath(target)
        if ebootInstallPath != None:
            gameEbootPaths.ebootInstallPath = ebootInstallPath
        
        if gameEbootPaths.ebootDiskPath is None and gameEbootPaths.ebootInstallPath is None:
            return None
        else:
            return gameEbootPaths
            
        
    def resolveRomPath(self, target :str) -> Path | None:
        try:
            with open(self.gamesConfigPath, "r") as f:
                for line in f:
                    splitLine = line.split(":",1)
                    if splitLine[0] == target:
                        return Path(splitLine[1].strip())    
                return None
        
        except Exception as e:
            print(f"there was an error gettings the the rom path({e})")
            return None

    def resolveInstallPath(self, target:str)-> Path | None:
        ebootInstallPath = Path(self.rpcs3Path / "dev_hdd0" / "game" / target / "USRDIR" / "EBOOT.BIN")
        if ebootInstallPath.exists():
            return ebootInstallPath
        else:
            return None
        