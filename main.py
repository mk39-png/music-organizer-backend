#!/usr/bin/env python3


# GOAL: with this script, the music unarchiving process is automated and reduces the need to
#       manually go through each archived file and extract metadata and many other chores.

import argparse
import os
from pathlib import Path
import shutil
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


def get_entries(directory: Path) -> list[Path]:
    """Get entries within a given directory. 

    :param directory: given directory to check
    :type directory: Path
    :return: list of entries within a directory. Includes child files and child directories.
    :rtype: list[Path]
    """


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

    # 1. Extract the folders, using the password file when needed.
    # TODO: check if parent folder name is the same as parent folder. If so, then flatten the directory.
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

                # TODO: could make a STDOUT parser in the future that parses the contents of
                #       the archived file and operates with that as an optimization
                # patoolib.list_archive(archive=child_str, verbosity=1,
                #                       interactive=False, password=password)
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

    # NOTE: I know the base directory is in tmp, but it's much easier to work with for now.
    temp_directory: Path = input_directory / "tmp"
    # NOTE: it's much easier to then put out results here
    results_directory: Path = input_directory / "results"

    # FIX: deal with case where there might be MULTIPLE folders inside an unarchived folder
    for parent_directory in temp_directory.iterdir():
        parent_directory_name = parent_directory.stem
        # NOTE: make any UX modular so that we can plug in some GUI and it'd work fine without major retooling/code reworking

        # This should deal with a majority of albums.
        # Anything else would be an outlier, but they should be a lot less than the majority of the files.

        # Simple counter to see if we have more than 1 child directory
        child_entries: list[Path] = [
            child_entry for child_entry in parent_directory.iterdir() if child_entry.is_dir()]
        num_child_directories: int = len(child_entries)

        child_entry_names: list[str] = os.listdir(parent_directory)

        # 0. ignore any folders with multiple subfolders (e.g. multi-CD sets)
        #    or maybe flatten the structure of multiple CD sets

        # 1. move any files into the folder at the same level

        # 2. decide on foldername and which one to keep

        # 3. extract metadata from folder name

        # 4. store metadata into some local database

        print("parent directory name: ", parent_directory.stem)
        print("parent directory: ", parent_directory)
        print("entries are the following: ", child_entry_names)

        # IF MULTIPLE CHILD DIRECTORIES, THEN SKIP

        for child_entry_name in child_entry_names:

            child_entry: Path = parent_directory / child_entry_name

            # TODO: for now, operate in the land of filenames
            # Then, when done comparing filenames and whatnot, then create the path
            # Because when we start working with paths right now, then things get super messy.
            # if child entry is the same name as the parent directory (meaning)
            print("child entry name: ", child_entry_name)
            print("child entry: ", child_entry)
            print(child_entry.is_file())

            # 1. check if there are other non-directory entries.
            # TODO: make a function that handles subfolders...
            # Or rather, given

            exit(67)

            # TODO: deal with case where entry is the same name as the parent...
            # But that would mean recursively moving contents of child directory to parent directory

            # Handle case where child directory has the same name as the parent directory.
            # In this case, we would have to run the script twice... or something like that.

            # TODO: move stuff from parent folder into new folder!
            if child_entry.is_dir() and (len(child_entry.stem) >= len(parent_directory.stem)):
                # TODO: rename parent entry and move the child entry to same level as parent...
                # OR move child entry to same level as parent and then remove the child entry directory

                # NOTE: can't move something up if it already exists... which means we need to rename the parent folder as that of the sub folder and move its contents upwards.
                shutil.move(child_entry, results_directory / child_entry_name)

                # Remove after moving folders
                # shutil.rmtree(parent_directory)
                print("Moving ", parent_directory)
            else:
                shutil.move(child_entry, results_directory / child_entry_name)

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
