"""
Retrieves archived files
"""
from pathlib import Path
import logging
import os
import patoolib
from .settings import Settings


# TODO: implement multiprocessing for file extraction in parallel
def extract(file_src_dir: Path, passwords: list[str], settings: Settings) -> None:
    """ Extracts archived file.
    WARNING: passwords should NOT be anything sensitive. 

    :param directory: filepath directory (e.g. test/music/archive.7z)
    :type directory: Path
    """

    # TODO: replace assert with a logging warning or error
    # TODO: error if there is already a file in tmp
    # assert not os.path.exists(file_directory.parent / "tmp"), "Temporary directory already exists!"

    # TODO: if already extracted file, then move it somewhere better.
    # As in, leave it alone.
    if os.path.isdir(file_src_dir):
        # TODO: use log instead...
        print(f"Directory {file_src_dir} is not a file!")
        return

    # Wait, could forcefully use a password loop, with break after extract_archive
    # to exit the loop of passwords early  (avoiding complex recursion or tracking)
    file_out_dir: Path = settings.temp_dir / file_src_dir.stem

    for password in passwords:
        # TODO: try below chunk of code with non-functional password entry attempt.
        try:
            logging.info("Trying password %s", password)

            # TODO: if it already exists, then DO NOT EXTRACT IT AGAIN!
            if file_out_dir.exists():
                print(f"{file_out_dir} already exists in temp/!")
                break

            patoolib.extract_archive(
                archive=file_src_dir.as_posix(),
                verbosity=0,
                outdir=file_out_dir.as_posix(),
                interactive=False,
                password=password
            )

            # TODO: upon successful extraction, remove the archived folder by placing it inside a
            # "complete" bin.
            # move(file_directory, str(parent_directory / "trash"))
            break
        except Exception as e:
            logging.error(f"Password \"{password}\"failed, continue with next password %s", e)
