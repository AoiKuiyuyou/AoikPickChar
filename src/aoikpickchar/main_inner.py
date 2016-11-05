# coding: utf-8
"""
This module contains the main inner function called by the main module.
"""
from __future__ import absolute_import

# Standard imports
from argparse import ArgumentParser
from argparse import ArgumentTypeError
import os
import subprocess
import sys
import webbrowser

# External imports
from aoikimportutil import load_obj

# Local imports
from .renderer import chars_to_combo_image
from .renderer import chars_to_images
from .renderer import get_font


class AttrDict(dict):
    """
    Attribute dict.

    Getting and setting attributes will get and set dict values.
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def str_strip_nonempty(text):
    """
    Strip white-spaces on both sides of given argument, and ensure the result \
        is not empty.

    Used as `type` argument of `argparse.ArgumentParser.add_argument`.

    @param text: Argument text.

    @return: Stripped argument text.
    """
    # Strip given argument text
    stripped_text = text.strip()

    # If the stripped text is not empty
    if stripped_text != '':
        # Return the stripped text
        return stripped_text

    # If the stripped text is empty
    else:
        # Get error message
        error_msg = 'Expected a non-empty and non-whitespace-only string.'\
            ' Got: {0}.'.format(repr(text))

        # Raise error
        raise ArgumentTypeError(error_msg)


def bool_0or1(text):
    """
    Convert given argument text '0' and '1' to False and True, respectively.

    Used as `type` argument of `argparse.ArgumentParser.add_argument`.

    @param text: Argument text.

    @return: False or True.
    """
    # If given argument text is '0'
    if text == '0':
        # Return False
        return False

    # If given argument text is '1'
    elif text == '1':
        # Return True
        return True

    # If given argument text is not '0' or '1'
    else:
        # Get error message
        error_msg = "Expected '0' or '1'. Got: {0}.".format(repr(text))

        # Raise error
        raise ArgumentTypeError(error_msg)


def int_ge0(text):
    """
    Convert given argument text to integer and ensure the integer is >=0.

    Used as `type` argument of `argparse.ArgumentParser.add_argument`.

    @param text: Argument text.

    @return: Integer >=0.
    """
    try:
        # Convert given argument text to integer.
        # May raise error.
        value = int(text)

        # Assert the value is >=0.
        # May raise error.
        assert value >= 0, value

    # If have error
    except Exception:
        # Get error message
        error_msg = 'Expected an integer >=0. Got: {0}.'.format(repr(text))

        # Raise error
        raise ArgumentTypeError(error_msg)

    # If not have error
    else:
        # Return the value
        return value


def int_gt0(text):
    """
    Convert given argument text to integer and ensure the integer is >0.

    Used as `type` argument of `argparse.ArgumentParser.add_argument`.

    @param text: Argument text.

    @return: Integer >0.
    """
    try:
        # Convert given argument text to integer.
        # May raise error.
        value = int(text)

        # Assert the value is >0.
        # May raise error.
        assert value > 0, value

    # If have error
    except Exception:
        # Get error message
        error_msg = 'Expected an integer >0. Got: {0}.'.format(repr(text))

        # Raise error
        raise ArgumentTypeError(error_msg)

    # If not have error
    else:
        # Return the value
        return value


def makedir(dir_path):
    """
    Make directory.

    :param dir_path: Directory path.

    :return: None.
    """
    # If the directory is not existing
    if not os.path.isdir(dir_path):
        try:
            # Make directories along the path
            os.makedirs(dir_path)

        # If have error.
        # Notice if the directory exists, error will be raised.
        except Exception:
            # If the directory not exists.
            # It means the error is not caused by existing directory.
            if not os.path.isdir(dir_path):
                # Raise the error
                raise

            # If the directory exists.
            else:
                # Ignore the error
                pass


def main_inner(args=None):
    """
    Main function's inner function.

    @param args: Command line argument list. Default is use `sys.argv[1:]`.

    @return: Exit code.
    """
    # Create command line arguments parser
    args_parser = ArgumentParser(prog='aoikpickchar', add_help=True)

    args_parser.add_argument(
        '-f', '--font',
        dest='font_file_path',
        type=str_strip_nonempty,
        required=True,
        metavar='PATH',
        help='Font file path. Must be given.',
    )

    args_parser.add_argument(
        '-s', '--font-size',
        dest='font_size',
        type=int_gt0,
        default=36,
        metavar='N',
        help='Font size. Default is 36.',
    )

    args_parser.add_argument(
        '-e', '--font-encoding',
        dest='font_encoding',
        default=None,
        choices=('ADBE', 'ADOB', 'armn', 'symb', 'unic'),
        metavar='ENCODING',
        help='Font encoding, one of ["ADBE", "ADOB", "armn", "symb", "unic"].'
        ' Default is try each in order.',
    )

    args_parser.add_argument(
        '-p', '--pick-func',
        dest='char_pick_func_uri',
        type=str_strip_nonempty,
        default=None,
        metavar='URI',
        help='Function to pick characters. Default is pick character points '
        ' 0 to 255.',
    )

    args_parser.add_argument(
        '-a', '--min',
        dest='char_point_min',
        type=int_ge0,
        default=None,
        metavar='N',
        help='Limit min character point. Default is no limit.',
    )

    args_parser.add_argument(
        '-b', '--max',
        dest='char_point_max',
        type=int_ge0,
        default=None,
        metavar='N',
        help='Limit max character point. Default is no limit.',
    )

    args_parser.add_argument(
        '-j', '--draw-combo',
        dest='draw_combo',
        action='store_true',
        help='Whether draw all picked characters to a combo image.',
    )

    args_parser.add_argument(
        '-k', '--draw-each',
        dest='draw_each',
        action='store_true',
        help='Whether draw each picked character to a separate image.',
    )

    args_parser.add_argument(
        '-d', '--out-dir',
        dest='out_dir',
        type=str_strip_nonempty,
        default=None,
        metavar='PATH',
        help='Output directory. Default is current directory.',
    )

    args_parser.add_argument(
        '-i', '--image',
        dest='combo_image_path',
        type=str_strip_nonempty,
        default=None,
        metavar='PATH',
        help='Combo image path. Default is output directory plus font'
        " file's name plus `.png`.",
    )

    args_parser.add_argument(
        '-c', '--xcount',
        dest='char_xcount',
        type=int_gt0,
        default=16,
        metavar='N',
        help="Number of characters per row. Default is 16.",
    )

    args_parser.add_argument(
        '-x', '--xpad',
        dest='char_xpad',
        type=str_strip_nonempty,
        default='0,0',
        metavar='N|N,N',
        help="Each character's X padding before and after. Default is `0,0`.",
    )

    args_parser.add_argument(
        '-y', '--ypad',
        dest='char_ypad',
        type=str_strip_nonempty,
        default='0,0',
        metavar='N|N,N',
        help="Each character's Y padding before and after. Default is `0,0`.",
    )

    args_parser.add_argument(
        '-m', '--mark-radix',
        dest='point_mark_radix',
        choices=('hex', 'dec', 'oct', 'bin'),
        default=None,
        metavar='RADIX',
        help='Each character\'s point mark\'s radix. one of ["hex", "dec",'
        ' "oct", "bin"]. Default is no point mark.',
    )

    args_parser.add_argument(
        '-z', '--mark-zfill',
        dest='point_mark_zfill',
        type=int_ge0,
        default=None,
        metavar='N',
        help="Each character's point mark's zero-fill length. Default is 2"
        ' for `hex`, 0 for `dec`, 3 for `oct`, and 8 for `bin`.',
    )

    args_parser.add_argument(
        '-g', '--mark-font',
        dest='point_mark_font_file_path',
        type=str_strip_nonempty,
        default=None,
        metavar='PATH',
        help="Each character's point mark's font file path. Default is use"
        ' the character font.',
    )

    args_parser.add_argument(
        '-t', '--mark-font-size',
        dest='point_mark_font_size',
        type=int_gt0,
        default=10,
        metavar='N',
        help="Each character's point mark's font size. Default is 10.",
    )

    args_parser.add_argument(
        '-u', '--mark-font-encoding',
        dest='point_mark_font_encoding',
        choices=('ADBE', 'ADOB', 'armn', 'symb', 'unic'),
        default=None,
        metavar='ENCODING',
        help="Each character's point mark's font file's encoding,"
        ' one of ["ADBE", "ADOB", "armn", "symb", "unic"].'
        ' Default is try each in order.',
    )

    args_parser.add_argument(
        '-v', '--view-combo',
        dest='view_combo',
        action='store_true',
        help='Whether view combo image. Default is not view.',
    )

    # Parse arguments
    args = args_parser.parse_args(args)

    # If `--draw-combo` and `--draw-each` are not given
    if not args.draw_combo and not args.draw_each:
        # Get error message
        error_msg = \
            'Error: Please specify `--draw-combo` and/or `--draw-each`.\n'

        # Print error message
        sys.stderr.write(error_msg)

        # Return exit code
        return -1

    # Ensure either `--draw-combo` or `--draw-each` is given
    assert args.draw_combo or args.draw_each, args

    # Get font file path
    font_file_path = args.font_file_path

    # Ensure font file path is not empty
    assert font_file_path, font_file_path

    # Get font size
    font_size = args.font_size

    # Ensure font size is GT 0
    assert font_size > 0, font_size

    # Get font encoding
    font_encoding = args.font_encoding

    # Get character point min
    char_point_min = args.char_point_min

    # Get character point max
    char_point_max = args.char_point_max

    # Get character pick function URI
    char_pick_func_uri = args.char_pick_func_uri

    # If character pick function URI is not given
    if char_pick_func_uri is None:
        # Use default
        char_pick_func = (lambda info: range(
            char_point_min if char_point_min is not None else 0,
            char_point_max + 1 if char_point_max is not None else 256
        ))

    # If character pick function URI is given
    else:
        try:
            # Load character pick function
            char_pick_func = load_obj(
                char_pick_func_uri,
                mod_name='aoikpickchar._char_pick_func'
            )

        # If have error
        except Exception:
            # Get error message
            error_msg = \
                'Error: Failed loading character pick function: {}.\n'\
                .format(repr(char_pick_func_uri))

            # Print error message
            sys.stderr.write(error_msg)

            # Raise original error
            raise

    # Get output directory path
    out_dir = args.out_dir

    # If output directory path is empty
    if not out_dir:
        # Use current directory path
        out_dir = '.'

    # Ensure output directory path is not empty
    assert out_dir, out_dir

    # Convert output directory path to absolute path
    out_dir = os.path.abspath(out_dir)

    # Ensure output directory path is absolute
    assert os.path.isabs(out_dir), out_dir

    # Get character pick function calling info
    call_info = AttrDict()

    # Set font file path
    call_info.font_file_path = font_file_path

    # Set output directory
    call_info.out_dir = out_dir

    try:
        # Call character pick function
        orig_pick_info_s = char_pick_func(call_info)

    # If have error
    except Exception:
        # Get error message
        error_msg = 'Error: Failed calling character pick function: {}.\n'\
            .format(repr(char_pick_func_uri))

        # Print error message
        sys.stderr.write(error_msg)

        # Raise original error
        raise

    # Get font file name
    font_file_name = os.path.split(font_file_path)[1]

    # Normalized pick info list
    pick_info_s = []

    # For each pick info returned by the character pick function
    for orig_pick_info in orig_pick_info_s:
        # If the pick info is int.
        # It means character point.
        if isinstance(orig_pick_info, int):
            # Create pick info dict
            pick_info = AttrDict()

            # Set character point
            pick_info.char_point = orig_pick_info

        # If the pick info is dict.
        # It means pick info dict.
        elif isinstance(orig_pick_info, dict):
            # Use as pick info
            pick_info = orig_pick_info

        # If the pick info is none of above
        else:
            # Get error message
            error_msg = 'Error: Invalid pick info: {}.\n'\
                .format(repr(orig_pick_info))

            # Print error message
            sys.stderr.write(error_msg)

            # Raise error
            raise ValueError(orig_pick_info)

        # Ensure the pick info is dict
        assert isinstance(pick_info, dict), pick_info

        # Ensure the pick info has `char_point` key
        assert 'char_point' in pick_info, pick_info

        # Get character point
        char_point = pick_info['char_point']

        # Ensure the character point is int
        assert isinstance(char_point, int), char_point

        # Ensure the character point is GE 0
        assert char_point >= 0, char_point

        # If the pick info not has `char_image_path` key
        if 'char_image_path' not in pick_info:
            # Get character image file name
            char_image_file_name = '{}.{}.png'.format(
                font_file_name,
                hex(char_point)[2:].zfill(2).upper(),
            )

            # Get character image file path
            char_image_path = os.path.join(out_dir, char_image_file_name)

            # Set character image file path
            pick_info['char_image_path'] = char_image_path

        # Ensure the pick info has `char_image_path` key
        assert 'char_image_path' in pick_info, pick_info

        # Get character image file path
        char_image_path = pick_info['char_image_path']

        # Convert character image file path to absolute path
        char_image_path = os.path.abspath(char_image_path)

        # Set character image file path
        pick_info['char_image_path'] = char_image_path

        # Add the pick info to the list
        pick_info_s.append(pick_info)

    # Limit character points within min and max
    pick_info_s = [
        i for i in pick_info_s if
        (char_point_min is None or i['char_point'] >= char_point_min) and
        (char_point_max is None or i['char_point'] <= char_point_max)
    ]

    # Get character points
    char_point_s = [i['char_point'] for i in pick_info_s]

    # Get character x-padding argument
    char_xpad_arg = args.char_xpad

    try:
        # If the argument not has `,`.
        # It means a single value.
        if ',' not in char_xpad_arg:
            # Get padding value
            padding_value = int(char_xpad_arg)

            # Get padding tuple
            char_xpad = (padding_value, padding_value)

        # If the argument has `,`.
        # It means a tuple value.
        else:
            # Get padding tuple
            char_xpad = tuple(int(v) for v in char_xpad_arg.split(',', 2))

    # If have error
    except Exception:
        # Get error message
        error_msg = 'Error: Invalid x padding value: {}.\n'\
            .format(repr(char_xpad_arg))

        # Print error message
        sys.stderr.write(error_msg)

        # Raise original error
        raise

    # Get character y-padding argument
    char_ypad_arg = args.char_ypad

    try:
        # If the argument not has `,`.
        # It means a single value.
        if ',' not in char_ypad_arg:
            # Get padding value
            padding_value = int(char_ypad_arg)

            # Get padding tuple
            char_ypad = (padding_value, padding_value)

        # If the argument has `,`.
        # It means a tuple value.
        else:
            # Get padding tuple
            char_ypad = tuple(int(v) for v in char_ypad_arg.split(',', 2))

    # If have error
    except Exception:
        # Get error message
        error_msg = 'Error: Invalid y padding value: {}.\n'\
            .format(repr(char_ypad_arg))

        # Print error message
        sys.stderr.write(error_msg)

        # Raise original error
        raise

    try:
        # Load character font
        char_font = get_font(
            font_file_path=font_file_path,
            font_size=font_size,
            font_encoding=font_encoding,
        )

    # If have error
    except Exception:
        # Get error message
        error_msg = 'Error: Failed loading character font: {}.\n'\
            .format(repr(font_file_path))

        # Print error message
        sys.stderr.write(error_msg)

        # Raise original error
        raise

    # If need draw combo image
    if args.draw_combo:
        # Get number of characters per row
        char_xcount = args.char_xcount

        # Ensure valid
        assert char_xcount > 0, char_xcount

        # Get point mark font file path
        point_mark_font_file_path = args.point_mark_font_file_path

        # If point mark font file path is not given
        if point_mark_font_file_path is None:
            # Use character font file path
            point_mark_font_file_path = font_file_path

        # Get point mark font size
        point_mark_font_size = args.point_mark_font_size

        # Ensure valid
        assert point_mark_font_size > 0, point_mark_font_size

        # Get point mark font encoding
        point_mark_font_encoding = args.point_mark_font_encoding

        try:
            # Load point mark font
            point_mark_font = get_font(
                font_file_path=point_mark_font_file_path,
                font_size=point_mark_font_size,
                font_encoding=point_mark_font_encoding,
            )

        # If have error
        except Exception:
            # Get error message
            error_msg = \
                'Error: Failed loading character point mark font: {}.\n'\
                .format(repr(font_file_path))

            # Print error message
            sys.stderr.write(error_msg)

            # Raise original error
            raise

        # Get character point mark's radix
        point_mark_radix = args.point_mark_radix

        # Ensure valid
        assert point_mark_radix in (None, 'hex', 'dec', 'oct', 'bin'), \
            point_mark_radix

        # Get character point mark's zero-fill length
        point_mark_zfill = args.point_mark_zfill

        # Ensure valid
        assert point_mark_zfill is None or point_mark_zfill >= 0, \
            point_mark_zfill

        # Convert characters to combo image
        combo_image = chars_to_combo_image(
            char_points=char_point_s,
            char_font=char_font,
            char_xcount=char_xcount,
            char_xpad=char_xpad,
            char_ypad=char_ypad,
            point_mark_font=point_mark_font,
            point_mark_radix=point_mark_radix,
            point_mark_zfill=point_mark_zfill,
        )

        # Get combo image path
        combo_image_path = args.combo_image_path

        # Ensure combo image path is not empty
        assert combo_image_path != '', combo_image_path

        # If combo image path is not given
        if combo_image_path is None:
            # Get combo image file name
            combo_image_file_name = font_file_name + '.png'

            # Get combo image file path
            combo_image_path = os.path.join(out_dir, combo_image_file_name)

        # If combo image path is given
        else:
            # If given combo image path is not absolute path
            if not os.path.isabs(combo_image_path):
                # Use output directory as base directory
                combo_image_path = os.path.join(out_dir, combo_image_path)

        # Convert combo image path to absolute path
        combo_image_path = os.path.abspath(combo_image_path)

        # Ensure combo image path is absolute path
        assert os.path.isabs(combo_image_path), combo_image_path

        # Create containing directory
        makedir(os.path.dirname(combo_image_path))

        # Create combo image file
        combo_image.save(combo_image_path)

        # Print message
        sys.stderr.write('Created combo image: {}\n'.format(combo_image_path))

        # If need view combo image
        if args.view_combo:
            # If the OS platform is Darwin,
            # and `open` program exists.
            #
            # Notice `webbrowser.open` somehow does not work in Darwin.
            if sys.platform == 'darwin' and os.path.isfile('/usr/bin/open'):
                # Open combo image
                subprocess.Popen(['/usr/bin/open', combo_image_path])

            # If the OS platform is not Darwin,
            # or `open` program not exists.
            else:
                # Open combo image
                webbrowser.open(combo_image_path)

    # If need draw each character
    if args.draw_each:
        # Draw characters to images
        char_image_s = chars_to_images(
            char_points=char_point_s,
            char_font=char_font,
            char_xpad=char_xpad,
            char_ypad=char_ypad,
        )

        # For each character image
        for pick_info, char_image in zip(pick_info_s, char_image_s):
            # Get character point
            char_point = pick_info['char_point']

            # Get character image file path
            char_image_path = pick_info['char_image_path']

            # Ensure character image file path is absolute path
            assert os.path.isabs(char_image_path)

            # Create containing directory
            makedir(os.path.dirname(char_image_path))

            # Create character image file
            char_image.save(char_image_path)

            # Print message
            sys.stderr.write(
                'Created character image: {}\n'.format(char_image_path)
            )

    # Return exit code
    return 0
