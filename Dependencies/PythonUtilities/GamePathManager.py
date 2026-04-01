from pathlib import Path

class GamePathManager:
    def __init__(self, rpcs3Path : Path):
        self.rpcs3Path = rpcs3Path
        self.gamesConfigPath = Path(rpcs3Path / "config" / "games.yml")
    
    def getSkate3RomPaths(self) -> list | None: 
        try:
            paths = []
            with open(self.gamesConfigPath, "r") as f:
                for line in f:
                    splitLine = line.split(":",1)
                    
                    if splitLine[0] == "BLUS30464":
                        paths.append(Path(splitLine[1].strip()))
                    elif splitLine[0] == "BLES00760":
                        paths.append(Path(splitLine[1].strip()))
            return paths
        except Exception as e:
            print(f"there was an error gettings the the rom paths {e}")
            return None
    

    def getSkate3RomEbootPaths(self)->list | None:

        romPaths = self.getSkate3RomPaths()
        if romPaths != None:
            ebootPaths = []

            for rompath in romPaths:
                ebootPath = Path(rompath / "PS3_GAME" / "USRDIR" / "EBOOT.BIN")
                if ebootPath.exists():
                    ebootPaths.append(ebootPath)
            
            BLUS = self.rpcs3Path / "dev_hdd0/game/BLUS30464/USRDIR//EBOOT.BIN"
            BLES = self .rpcs3Path / "dev_hdd0/game/BLES00760/USRDIR/EBOOT.BIN"
            
            if BLUS.exists():
                ebootPaths.append(BLUS)
            elif BLES.exists():
                ebootPaths.append(BLES)

            return ebootPaths
        else:
            return None
        