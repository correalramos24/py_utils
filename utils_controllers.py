
from .utils_print import info, info2, warning
from .utils_files import create_dir, check_path_exists
from abc import ABC, abstractmethod

from pathlib import Path
import pickle as pkl

class AbstractFrontend(ABC):
    @abstractmethod
    def loop(self):
        pass

class AbstractPersistance(ABC):
    
    def __init__(self, root_path: Path):
        self.root : Path = root_path
        self.meta : Path = Path(self.root, "meta.data")
        self.entities : dict[str, any] = dict()
        
        if check_path_exists(root_path):  
            self._info("INIT @", root_path)
            self._load_metadata()
            self._info2("METADATA:", self.entities)
        else:
            self._info("NEW PERSISTANCE @", root_path)
            create_dir(self.root, False)
            self._save_metadata()

    #========================INTERFACE METHODS==================================
    @abstractmethod
    def store(self, content: any, pers_id : str):
        pass
    
    @abstractmethod
    def load(self, pers_id: str):
        pass
    
    def exist(self, pers_id):
        return pers_id in self.entities
    
    def list_entities(self):
        return list(self.entities.keys())
    
    #==========================PRIVATE METHODS==================================
    def _load_metadata(self):
        with open(self.meta, "rb") as md_file:
            self.entities = pkl.load(md_file)

    def _save_metadata(self):
        with open(self.meta, "wb") as md_file:
            pkl.dump(self.entities, md_file)
            

    @staticmethod
    def _info(*args): info("DATABS:", *args)
    @staticmethod
    def _info2(*args): info2("DATABS:", *args)
    @staticmethod
    def _warn(*args): warning("DATABS:", *args)
    