
from typing import Any, Hashable
import pickle as pkl
from pathlib import Path

from .meta import MetaAbstractClass
from .utils_files import create_dir, check_path_exists

class GenericPersistance(MetaAbstractClass):
    def __init__(self, root_path: Path):
        self.root : Path = root_path
        self.meta : Path = Path(self.root, "meta.data")
        self.entities : dict[Hashable, Any] = dict()

        if check_path_exists(root_path):
            self._log("INIT @", root_path)
            self._load_metadata()
            self._dbg("METADATA:", self.entities)
        else:
            self._log("NEW PERSISTANCE @", root_path)
            create_dir(self.root, False)
            self._save_metadata()

    def store(self, identifier : Hashable, content: Any):
        self._dbg(f"STORING {identifier} {content}")
        self.entities[identifier] = content
        self._save_metadata()

    def load(self, identifier: Hashable):
        self._dbg(f"LOADING {identifier}")
        ret = self.entities.get(identifier)
        if ret:
            return ret
        self._warn("Accesing non-found ID:", identifier)
        return None

    def remove(self, identifier: Hashable):
        if self.exist(identifier):
            self._dbg(f"REMOVING {identifier}")
            self.entities.pop(identifier)
            self._ok(f"REMOVED {identifier}")
        self._warn(f"Removing non-found ID: {identifier}")

    def exist(self, identifier: Hashable):
        return identifier in self.entities

    def list_entities(self):
        return list(self.entities.keys())

    def _load_metadata(self):
        with open(self.meta, "rb") as md_file:
            self.entities = pkl.load(md_file)

    def _save_metadata(self):
        with open(self.meta, "wb") as md_file:
            pkl.dump(self.entities, md_file)