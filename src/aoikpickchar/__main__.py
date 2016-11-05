# coding: utf-8
"""
This module is the program's main module.
"""
from __future__ import absolute_import

# Standard imports
import os.path
import sys
from traceback import format_exc


def run_setup_syspath(package_root, current_dir=None):
    """
    Run function `setup_syspath` to set up `sys.path` for import resolution.

    This function loads function `setup_syspath` by executing its containing \
        module's code in a context dict. Function `setup_syspath` can not be \
        imported directly because `sys.path` has not been set up yet.

    :param package_root: Package root directory path. Will be added to \
        `sys.path`. In the repository the package root directory is `src`. \
        After installation the package root directory is `site-packages`.

    :param current_dir: Current directory path. If given, will be removed \
        from `sys.path`.

    :return: None.
    """
    # Convert package root directory path to normalized absolute path
    package_root = os.path.abspath(package_root)

    # Ensure package root directory path is absolute
    assert os.path.isabs(package_root), package_root

    # Get `main_init.py` file path
    main_init_file_path = os.path.join(
        package_root, 'aoikpickchar', 'main_init.py'
    )

    # Ensure `main_init.py` file path is absolute
    assert os.path.isabs(main_init_file_path), main_init_file_path

    # Ensure `main_init.py` file exists
    assert os.path.isfile(main_init_file_path), main_init_file_path

    # Open `main_init.py` file
    with open(main_init_file_path) as file:
        # Get code in the file
        main_init_module_code = file.read()

        # Create context dict for `exec` below
        context_dict = {}

        # Run the code in the context
        exec(main_init_module_code, None, context_dict)

        # Get `setup_syspath` function
        setup_syspath = context_dict['setup_syspath']

    # Delegate call to `setup_syspath`
    setup_syspath(package_root=package_root, current_dir=current_dir)


def check_deps():
    """
    Check whether dependency packages have been installed.

    :return: Error message for missing dependency, otherwise None.
    """
    try:
        # Import dependency module
        import PIL

        # Suppress linter error
        id(PIL)

    # If the dependency module is not found
    except ImportError:
        # Get error message
        msg = (
            'Error: Package `PIL` is not installed. Try:\n'
            'pip install pillow\n'
        )

        # Return error message
        return msg

    # Return None to mean no missing dependency
    return None


def main(args=None):
    """
    This program's main function.

    :param args: Command argument list. Default is use `sys.argv[1:]`.

    :return: Exit code.
    """
    try:
        # Run function `setup_syspath` to set up `sys.path` for import
        # resolution
        run_setup_syspath(
            package_root=os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            ),
            current_dir=os.path.dirname(os.path.abspath(__file__)),
        )

        # Check whether dependency packages are installed
        error_msg = check_deps()

        # If have error message for missing dependency
        if error_msg is not None:
            # Print error message
            sys.stderr.write(error_msg)

            # Return exit code
            return -100

        # If not have error message for missing dependency
        else:
            # Import `main_inner` function
            from aoikpickchar.main_inner import main_inner

            # Delegate call to `main_inner`
            return main_inner(args)

    # If have `SystemExit`
    except SystemExit:
        # Raise as-is
        raise

    # If have `KeyboardInterrupt`
    except KeyboardInterrupt:
        # Return exit code
        return 0

    # If have other exceptions
    except BaseException:
        # Get traceback message
        tb_msg = format_exc()

        # Get error message
        error_msg = 'Traceback:\n---\n{0}---\n'.format(tb_msg)

        # Print error message
        sys.stderr.write(error_msg)

        # Return exit code
        return -1


# If this module is run as main module
if __name__ == '__main__':
    # Call main function
    exit(main())
