#!/usr/bin/env python3

# GOAL: with this script, the music unarchiving process is automated and reduces the need to
#       manually go through each archived file and extract metadata and many other chores.

import argparse
import os
from pathlib import Path
from typing import Literal
import sys

# Extractors
import csv
import logging
from datetime import datetime
from util.extractor import extract
from util.flatten import flatten
from util.settings import Settings

# TODO: make a wrapper of the extract_archive function?
#       which is so that it performs additional functionalities...
logger: logging.Logger = logging.getLogger(__name__)
timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename: str = f"experiments_{timestamp}.log"
log_filepath: Path = Path(__file__).parent / "logs" / log_filename
log_filepath.parent.mkdir(parents=True, exist_ok=True)  # make log directory forcefully

logging.basicConfig(
    level=logging.NOTSET,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filepath, mode="w"),  # Overwriting runs
    ]
)


def main(args: argparse.Namespace) -> Literal[0]:
    """
    Views files and folders in a chosen directory.

    :param args: input directory
    :type args: _type_
    :return: _description_
    :rtype: Literal[0]
    """
    # Extract temporarily, then be sure to flatten structure if archived file contains
    #   more than just a folder and its subfolders...
    # Be sure to prompt the user "y/n" if they would like to unarchive the folder or not.
    # Move the original archived file to a "/done" folder

    #
    # PART 1. FILE EXTRACTION
    #
    # 0. Read in list of passwords if there is such a thing.
    base_dir: Path = Path(args.input)  # e.g. test/music/
    passwords_dir: Path = args.passwords

    passwords_file = open(passwords_dir)
    reader = csv.reader(passwords_file)
    passwords: list[str] = next(reader)  # NOTE: passwords.csv should be a single, continuous line

    settings: Settings = Settings(temp_dir_in=base_dir / "temp",
                                  results_dir_in=base_dir / "results",
                                  complete_dir_in=base_dir / "complete")

    # 1. Extract the folders, using the password file when needed.
    for sub_dir in base_dir.iterdir():
        extract(sub_dir, passwords, settings)

    #
    # PART 2. HANDLING NESTED FOLDERS
    #
    # 2. Check contents of folders
    # a. see if subfolder name is longer than parent folder name
    # b. if same length, then extract as is, being sure to flatten folder structure
    # c. if NOT the same length, inherit the filename of whatever is longer.

    # 3. handle encrypted files by moving them to a "rejected" folder... or leaving them as is.
    # TODO: try from a list of passwords that are from a read-in JSON file (rather than having
    #       them hard-coded)
    # TODO: handle case where unarchived folder but it's the discography of an artist, so there
    # are a BUNCH of folders within the archive.
    # TODO: deal with case where there might be MULTIPLE folders inside an unarchived folder
    # TODO: test the code above. when  done working, make sure the below works.
    # TODO: check if parent folder name is the same as parent folder.
    #       If so, then flatten the directory.
    for album_dir in settings.temp_dir.iterdir():
        # Check if album has CD subfolders or is actually a discography of many albums.
        sub_album_dir: list[Path] = [
            album for album in album_dir.iterdir() if
            album.is_dir()
        ]
        num_album_dir: int = len(sub_album_dir)
        album_folder_names: list[str] = os.listdir(album_dir)
        print("Sub-albums are the following are the following: ", album_folder_names)
        print("Album dir is this: ", album_dir)

        # 0. ignore any folders with multiple subfolders (e.g. multi-CD sets)
        #    or maybe flatten the structure of multiple CD sets
        # 1. move any files into the folder at the same level
        # 2. decide on foldername and which one to keep
        # 3. extract metadata from folder name
        # 4. store metadata into some local database
        # for album_folder in sub_album_dir:
        #     flatten(album_folder)

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="music-organizer",
        description="Given a folderpath, view compressed files contents and see if parent folder "
        "has more metadata than archived folder contents.")

    parser.add_argument("-i", "--input", type=str, help="Parent directory.", required=True)
    parser.add_argument("-p", "--passwords", type=str, help="Filepath to passwords.", required=True)

    args: argparse.Namespace = parser.parse_args()

    sys.exit(main(args))
