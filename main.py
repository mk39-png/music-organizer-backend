#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import Literal
import sys

# Extractors
import patoolib
import csv
import logging
from datetime import datetime

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

    # NOTE: we need Path so that we can check for the file extension
    #       and since Path gives us many good quality-of-life features
    #       for listing out folders in a directory.

    # Extract temporarily, then be sure to flatten structure if archived file contains
    #   more than just a folder and its subfolders...
    # Be sure to prompt the user "y/n" if they would like to unarchive the folder or not.
    # Move the original archived file to a "/done" folder

    #
    # PART 1. FILE EXTRACTION
    #
    # 0. Read in list of passwords if there is such a thing.
    # NOTE: extract the folders, keeping the parent name. Deal with metadata afterwards.
    input_directory: Path = Path(args.input)
    passwords_directory: Path = args.passwords

    print(input_directory.absolute())
    passwords_file = open(passwords_directory)
    reader = csv.reader(passwords_file)
    passwords: list[str] = next(reader)  # NOTE: passwords.csv should be a single, continuous line

    print(input_directory)
    # 1. Extract the folders, using the password file when needed
    for child in input_directory.iterdir():

        # Skip folders
        if not child.is_file():
            continue

        print(child.stem)
        child_str = str(child)

        # Wait, could forcefully use a password loop, with break after extract_archive
        # to exit the loop of passwords early  (avoiding complex recursion or tracking)
        for password in passwords:
            try:
                logging.info("Trying password %s", password)
                patoolib.extract_archive(archive=child_str, verbosity=1, outdir=str(
                    input_directory / "tmp" / child.stem), interactive=False, password=password)
                break
            except Exception as e:
                logging.error("failed force usage of password, continue with next password %s", e)

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
    temp_directory: Path = input_directory / "tmp"
    for child in temp_directory.iterdir():
        """
        Now, go through and look at the metadata of the folders, performing checks and whatnot, 
        flattening structures, etc...

        """

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
