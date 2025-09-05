from pathlib import Path
import shutil
import os

# ========================CHECK PRESENCE========================================
def check_file_exists(file_path: Path):
    return file_path.is_file()

def check_file_exists_exception(file_path: Path):
    if not file_path.is_file():
        raise Exception(file_path, "not found!")

def check_path_exists(folder_path: Path):
    if isinstance(folder_path, str):
        folder_path = Path(folder_path)
    return folder_path.exists()

def check_path_exists_exception(folder_path: Path):
    if isinstance(folder_path, str): folder_path = Path(folder_path)
    if not folder_path.exists():
        raise Exception(f"{folder_path} not found!")

# ========================CREATE DIRS===========================================
def create_dir(folder_path: Path, overwrite: bool = False):
    if isinstance(folder_path, str): folder_path = Path(folder_path)    
    if folder_path.exists() and overwrite: 
        shutil.rmtree(folder_path)
    if (not folder_path.exists()) or overwrite:
        folder_path.mkdir(parents=True, exist_ok=True)
    else:
        raise Exception("Creating an already existing dir!")

# ========================COPY FILES============================================
def copy_folder(reference_folder: Path, 
                destination_folder: Path, 
                force: bool, 
                preserve_symlinks: bool = False):
    if not reference_folder.exists():
        raise FileNotFoundError(f"Reference folder '{reference_folder}' not found.")
    
    if not reference_folder.is_dir():
        raise NotADirectoryError(f"'{reference_folder}' isn't a folder.")

    if destination_folder.exists():
        if not force:
            raise FileExistsError(f"Destination folder '{destination_folder}' exists, use force.")
    
    shutil.copytree(reference_folder, destination_folder, 
                    symlinks=preserve_symlinks, 
                    dirs_exist_ok=True)
    
    print(f"Generated '{destination_folder}' from '{reference_folder}'.")

def copy_folder_content(ref_folder: Path,trg_folder: Path,
                        force: bool, preserve_symlinks: bool = False,
                        only_big_files: bool = True,
                        big_file_threshold: int = 2 * 1024 * 1024):
    
    if isinstance(ref_folder, str): ref_folder = Path(ref_folder)
    if isinstance(trg_folder, str): trg_folder = Path(trg_folder)
    
    if not ref_folder.exists(): 
        raise Exception(f"Ref. folder '{ref_folder}' not found")
    
    trg_folder.mkdir(parents=True, exist_ok=True)
    for item in ref_folder.rglob('*'):
        rel_path = item.relative_to(ref_folder)
        dest_path = trg_folder / rel_path

        if item.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
            continue

        if dest_path.exists() or dest_path.is_symlink():
            if force:
                if dest_path.is_dir():
                    shutil.rmtree(dest_path)
                else:
                    dest_path.unlink()
            else:
                continue  # skip if not forcing overwrite

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if item.is_symlink():
            if preserve_symlinks:
                link_target = os.readlink(item)  # Gets the raw link path (could be relative)
                dest_path.symlink_to(link_target)
            else:
                resolved = item.resolve()
                shutil.copy2(resolved, dest_path)

        elif item.is_file():
            if only_big_files and item.stat().st_size >= big_file_threshold:
                # Create a relative symlink to the source file from dest
                relative_target = os.path.relpath(item.resolve(), start=dest_path.parent)
                dest_path.symlink_to(relative_target)
            else:
                shutil.copy2(item, dest_path)

def copy_file(source: Path, destination: Path):
    if not source.is_file():
        raise FileNotFoundError(f"Unable to find {source}")
    try:
        shutil.copy2(source, destination)
    except PermissionError:
        print(f"Bad permissions either for {source} or {destination}.")
    except FileExistsError:
        print(f"{destination} already exists")
    except Exception as e:
        print(f"Error: {e}")

# =======================GEN SYMLINKS===========================================

def gen_symlink(source: Path, destination: Path):
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Si ya existe algo en destination, lo quitamos
        if destination.exists() or destination.is_symlink():
            destination.unlink()

        # Crear symlink relativo si es posible
        relative_target = source.relative_to(destination.parent) if source.is_absolute() and destination.parent in source.parents else source
        destination.symlink_to(relative_target)

    except Exception as e:
        raise RuntimeError(f"Failed to create symlink from {destination} to {source}: {e}")

def gen_symlink_from_folder(source: Path, destination: Path, only_big_files: bool = False):
    """
    Create a symlink for each file/folder in the source folder to the destination folder.
    """
    if not source.is_dir():
        raise NotADirectoryError(f"Source '{source}' is not a directory.")

    destination.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        src_item = item
        dest_item = destination / item.name
        if only_big_files:
            if item.is_file() and item.stat().st_size > 10 * 1024 * 1024:
                gen_symlink(src_item, dest_item)
            else:
                # Copy the file instead of creating a symlink
                copy_file(src_item, dest_item)
        else:
            gen_symlink(src_item, dest_item)
