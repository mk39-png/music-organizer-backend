"""
Flattens a given file directory.
"""

# NOTE: shutil's move is a godsend and performs *recursive* moving of files over!
from pathlib import Path

# NOTE: only need the directory to the album... or the folder within temp/


def flatten(directory: Path, results_directory: Path = "") -> None:
    """ Based off a particular condition, moves a subfolder to same level as current folder and then
    "deletes" parent folder.

    NOTE: this does NOT handle cases where a folder represents an album with multiple CD folders,
    for example.
    This is only for the case when an archive is extracted and its current folder name is less
    descriptive than its subfolder name.
    Hence, the need to flatten its name.

    :param directory: the folder directory to flatten.
    :type directory: Path
    """
    # assert directory.is_dir(), f"Provided argument {directory} is not a directory!"

    # # This handles case where subdirectories may be albums of a discography or perhaps
    # # multi-CD album releases.
    # subdirectories: list[Path] = [dir for dir in directory.iterdir() if dir.is_dir()]

    # # WARNING: this will delete stuff.
    # # TODO: safer to just move this stuff to a temporary "delete" folder.
    # # TODO: or confirm that this will happen with a [Y] or [N] prompt.
    # # If no files in the same directory
    # # Then move subfiles to same level as directory
    # # Remove current directory

    # # NOTE: only handling case where regular album.

    # # TODO: variable renaming
    # if (len(subdirectories) == 1) and (len(directory.stem) >= len(subdirectories[0].stem)):
    #     # TODO: rename parent entry and move the child entry to same level as parent...
    #     # OR move child entry to same level as parent and then remove the child entry directory

    #     # NOTE: can't move something up if it already exists... which means we need to rename
    #     # the parent folder as that of the sub folder and move its contents upwards.
    #     move(directory, dst=results_directory / directory_name)

    #     # Remove after moving folders
    #     # shutil.rmtree(parent_directory)
    #     print("Moving ", parent_archive_directory)
    # else:
    #     move(directory, results_directory / directory_name)
