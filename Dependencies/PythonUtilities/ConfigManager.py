import json
from pathlib import Path
class ConfigManager:
    def __init__(self, jsonPath : Path):
        self.jsonPath = str(jsonPath)
    
    def dumpJsonFile(self, rpcs3Path: str):
        try:
            with open(self.jsonPath, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"error getting dumpingRpcs3Path {e}")

        data["RPCS3Path"] = rpcs3Path

        with open(self.jsonPath, "w") as f:
            json.dump(data, f, indent=4)
    
    def getRPCS3Path(self)-> str | None:
        try:
            with open(self.jsonPath, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"error getting rpcs3 path {e}")
            return None
        
        path = data["RPCS3Path"].strip()
        
        if path != "":
            return path
        else:
            return None
            