# coding: utf-8
"""
This module contains function that sets up `sys.path` for import resolution.
"""
from __future__ import absolute_import

# Standard imports
import os
import os.path
import sys


def setup_syspath(package_root, current_dir=None):
    """
    Set up `sys.path` for import resolution.

    :param package_root: Package root directory path. Will be added to \
        `sys.path`. In the repository the package root directory is `src`. \
        After installation the package root directory is `site-packages`.

    :param current_dir: Current directory path. If given, will be removed \
        from `sys.path`.

    :return: None.
    """
    # Directory paths to remove from `sys.path`
    removing_dir_s = ['', '.']

    # If current directory is given
    if current_dir is not None:
        # Convert current directory path to normalized absolute path
        current_dir = os.path.abspath(current_dir)

        # Add to removing paths
        removing_dir_s.append(current_dir)

    # Remove paths from `sys.path` to avoid unexpected import resolution.
    #
    # For each removing path.
    for path in removing_dir_s:
        # Use loop to handle multiple occurrences of same path
        while True:
            try:
                # Remove the path from `sys.path`
                sys.path.remove(path)

            # If have error.
            # It means the path is not in `sys.path`.
            except ValueError:
                # Stop the while loop
                break

    # Convert package root directory path to normalized absolute path
    package_root = os.path.abspath(package_root)

    # Ensure the path is absolute
    assert os.path.isabs(package_root), package_root

    # Ensure the directory exists
    assert os.path.isdir(package_root), package_root

    # If the directory path is not in `sys.path`
    if package_root not in sys.path:
        # Prepend it to `sys.path`
        sys.path.insert(0, package_root)

    # Get dependency root directory path
    dep_root = os.path.join(package_root, 'aoikpickchardep')

    # Convert dependency root directory path to normalized absolute path
    dep_root = os.path.abspath(dep_root)

    # Ensure the path is absolute
    assert os.path.isabs(dep_root), dep_root

    # Ensure the directory exists
    assert os.path.isdir(dep_root), dep_root

    # If the directory path is not in `sys.path`
    if dep_root not in sys.path:
        # Prepend it to `sys.path`
        sys.path.insert(0, dep_root)

    # Get current PYTHONPATH
    pythonpath = os.environ.get('PYTHONPATH', '')

    # Get paths in PYTHONPATH
    pythonpath_dir_s = pythonpath.split(os.pathsep)

    # Convert the paths to normalized absolute paths
    pythonpath_dir_s = [os.path.abspath(p) for p in pythonpath_dir_s]

    # If package root directory path is not in the paths
    if package_root not in pythonpath_dir_s:
        # Prepend it to the paths
        pythonpath_dir_s.insert(0, package_root)

    # If dependency directory path is not in the paths
    if dep_root not in pythonpath_dir_s:
        # Prepend it to the paths
        pythonpath_dir_s.insert(0, dep_root)

    # Get new PYTHONPATH
    new_pythonpath = os.pathsep.join(pythonpath_dir_s)

    # Set new PYTHONPATH
    os.environ['PYTHONPATH'] = new_pythonpath
