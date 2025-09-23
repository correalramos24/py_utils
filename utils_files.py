from .utils_py import pathfy
from .utils_print import MyLogger

from functools import wraps
from typing import Callable
from pathlib import Path
import os, shutil

# ========================CHECK PRESENCE========================================
def file_exists(f_path: Path | str) -> bool:
    return pathfy(f_path).is_file()

def check_file_exists_exception(f_path: Path):
    if not file_exists(f_path):
        raise Exception(f"{f_path} not found!")

def check_path_exists(fldr_path: Path | str) -> bool:
    return pathfy(fldr_path).exists()

def check_path_exists_exception(fldr_path: Path) -> None:
    if not check_path_exists(fldr_path):
        raise Exception(f"{fldr_path} not found!")

# ========================CREATE DIRS===========================================
def create_dir(fldr_path: Path, overwrite: bool = False):
    fldr_path = pathfy(fldr_path)
    if fldr_path.exists() and overwrite:
        MyLogger.warning("existing directory:", str(fldr_path))
    if not fldr_path.exists():
        fldr_path.mkdir(parents=True, exist_ok=True)
        MyLogger.success(f"Dir {fldr_path} created.")
    else:
        raise Exception(f"create_dir {fldr_path} already existing!")

# ========================COPY FILES============================================
def copy_folder(ref_fldr: Path, dest_fldr: Path,
                force: bool, keep_sym: bool = False):

    bad_symlinks_excp = False
    _ = shutil.copytree(
        src = ref_fldr, dst = dest_fldr, symlinks=keep_sym,
        dirs_exist_ok=force, ignore_dangling_symlinks = bad_symlinks_excp
    )
    MyLogger.success(f"Generated '{dest_fldr}' from '{ref_fldr}'.")

def copy_folder_content(ref_folder: Path,dest_fldr: Path,
                        force: bool, preserve_symlinks: bool = False,
                        only_big_files: bool = True,
                        big_file_threshold: int = 2 * 1024 * 1024):
    #TODO: Check usage of this
    ref_folder = pathfy(ref_folder)
    dest_fldr = pathfy(dest_fldr)

    if not ref_folder.exists():
        raise Exception(f"Ref. folder '{ref_folder}' not found")

    dest_fldr.mkdir(parents=True, exist_ok=True)
    for item in ref_folder.rglob('*'):
        rel_path = item.relative_to(ref_folder)
        dest_path = dest_fldr / rel_path

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
                _ = shutil.copy2(resolved, dest_path)

        elif item.is_file():
            if only_big_files and item.stat().st_size >= big_file_threshold:
                # Create a relative symlink to the source file from dest
                relative_target = os.path.relpath(item.resolve(), start=dest_path.parent)
                dest_path.symlink_to(relative_target)
            else:
                _ = shutil.copy2(item, dest_path)

def copy_file(src: Path, dst: Path):
    if not src.is_file():
        raise FileNotFoundError(f"Unable to find {src}")
    try:
        _ = shutil.copy2(src, dst)
    except PermissionError:
        print(f"Bad permissions either for {src} or {dst}.")
    except FileExistsError:
        print(f"{dst} already exists")
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
