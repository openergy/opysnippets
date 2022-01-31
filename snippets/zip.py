"""
opysnippets/zip:1.0.0
"""
import os


def zip_dir(dir_path, open_zip_file):
    return _zip_dir(dir_path, open_zip_file)


def _zip_dir(root_path, open_zip_file, rel_path=None):
    """
    Parameters
    ----------
    root_path: base directory
    open_zip_file
    rel_path: sub-directory to zip (will be called recursively)

    Returns
    -------

    """
    # prepare paths
    dir_path = root_path if rel_path is None else os.path.join(root_path, rel_path)
    rel_path = "" if rel_path is None else rel_path

    # discover directory
    dir_path, dirs, files = next(os.walk(dir_path))

    # zip files
    for file_name in files:
        open_zip_file.write(os.path.join(dir_path, file_name), arcname=os.path.join(rel_path, file_name))

    # zip directory (recursive)
    for dir_name in dirs:
        _zip_dir(root_path, open_zip_file, rel_path=os.path.join(rel_path, dir_name))
