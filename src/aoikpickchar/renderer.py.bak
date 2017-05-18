# coding: utf-8
"""
This module contains functions that render characters to images.
"""
from __future__ import absolute_import

# External imports
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def get_font(
    font_file_path,
    font_size,
    font_encoding=None,
):
    """
    Get font object.

    :param font_file_path: Font file path.

    :param font_size: Font size.

    :param font_encoding: Font encoding, one of ["ADBE", "ADOB", "armn", \
        "symb", "unic"]. Default is try each in order.

    :return: Font object.
    """
    # If font encoding is given
    if font_encoding is not None:
        # Load the font with the given encoding
        font = ImageFont.truetype(
            font_file_path,
            font_size,
            encoding=font_encoding,
        )

    # If font encoding is not given
    else:
        # For each candidate encoding.
        #
        # Notice `armn` is put before `symb` because some fonts in `armn`
        # encoding can be loaded with 'symb' encoding without raising an error.
        for font_encoding in ['ADBE', 'ADOB', 'armn', 'symb', 'unic']:
            try:
                # Load the font with the candidate encoding
                font = ImageFont.truetype(
                    font_file_path,
                    font_size,
                    encoding=font_encoding,
                )

                # Stop trying next candidate encoding
                break

            # If have error
            except Exception:
                # Continue to try next candidate encoding
                continue

        # If none of the candidate encodings above works
        else:
            # Load as bitmap font
            font = ImageFont.load(
                font_file_path,
            )

    # Return font object
    return font


def chars_to_combo_image(
    char_points,
    char_font,
    char_xcount,
    char_xpad=None,
    char_ypad=None,
    point_mark_font=None,
    point_mark_radix=None,
    point_mark_zfill=None,
):
    """
    Render characters to a combo image.

    :param char_points: Character point list.

    :param char_font: Character font object.

    :param char_xcount: Number of characters per row.

    :param char_xpad: Each character's X padding before and after. Format is \
        a tuple of two values.

    :param char_ypad: Each character's Y padding before and after. Format is \
        a tuple of two values.

    :param point_mark_font: Each character's point mark's font object.

    :param point_mark_radix: Each character's point mark's radix, one of \
        ["hex", "dec", "oct", "bin"].

    :param point_mark_zfill: Each character's point mark's zero-fill length.

    :return: Combo image.
    """
    # Get font size
    font_size = char_font.size

    # Get number of rows, and last row's cell count
    ycell_count, last_row_cell_count = \
        divmod(len(char_points), char_xcount)

    # If last row's cell count is GT 0
    if last_row_cell_count > 0:
        # Add one more row
        ycell_count += 1

    # If character X-padding is not given
    if char_xpad is None:
        # Use default
        char_xpad = (0, 0)

    # Ensure valid
    assert isinstance(char_xpad, tuple)

    assert len(char_xpad) == 2

    # If character Y-padding is not given
    if char_ypad is None:
        # Use default
        char_ypad = (0, 0)

    # Ensure valid
    assert isinstance(char_ypad, tuple)

    assert len(char_ypad) == 2

    # Get cell xspan
    cell_xspan = char_xpad[0] + font_size + char_xpad[1]

    # Get cell yspan
    cell_yspan = char_ypad[0] + font_size + char_ypad[1]

    # Get combo image xspan
    combo_image_xspan = cell_xspan * char_xcount

    # Get combo image yspan
    combo_image_yspan = cell_yspan * ycell_count

    # Create combo image
    combo_image = Image.new(
        mode='RGB',
        size=(combo_image_xspan, combo_image_yspan),
        color='white'
    )

    # Create combo image's ImageDraw object
    combo_imagedraw = ImageDraw.Draw(combo_image)

    # If point mark zfill length is not given
    if point_mark_zfill is None:
        # If radix is hex
        if point_mark_radix == 'hex':
            # Set zfill length
            point_mark_zfill = 2

        # If radix is decimal
        elif point_mark_radix == 'dec':
            # Set zfill length
            point_mark_zfill = 0

        # If radix is octal
        elif point_mark_radix == 'oct':
            # Set zfill length
            point_mark_zfill = 3

        # If radix is binary
        elif point_mark_radix == 'bin':
            # Set zfill length
            point_mark_zfill = 8

        # If radix is none of above
        else:
            # Set zfill length
            point_mark_zfill = 0

    # For each character point
    for cell_index, char_point in enumerate(char_points):
        # Get character
        char = chr(char_point)

        # Get cell y position, i.e. the row index
        cell_ypos = cell_index // char_xcount

        # Get cell x position in the row, i.e. the column index
        cell_xpos = cell_index % char_xcount

        # Get pixel x position, not including char_xpad[0]
        pixel_xpos = cell_xspan * cell_xpos

        # Get pixel y position, not including char_ypad[0]
        pixel_ypos = cell_yspan * cell_ypos

        # Draw the character to the combo image
        combo_imagedraw.text(
            xy=(pixel_xpos + char_xpad[0], pixel_ypos + char_ypad[0]),
            text=char,
            font=char_font,
            fill='black',
        )

        # If point mark radix is given
        if point_mark_radix is not None:
            # Ensure valid
            assert point_mark_radix in ('hex', 'dec', 'oct', 'bin')

            # If radix is hex
            if point_mark_radix == 'hex':
                # Get point mark text
                point_mark_text = hex(char_point)[2:].zfill(point_mark_zfill)\
                    .upper()

            # If radix is decimal
            elif point_mark_radix == 'dec':
                # Get point mark text
                point_mark_text = str(char_point)

            # If radix is octal
            elif point_mark_radix == 'oct':
                # Get point mark text
                point_mark_text = oct(char_point)[2:].zfill(point_mark_zfill)

            # If radix is binary
            elif point_mark_radix == 'bin':
                # Get point mark text
                point_mark_text = bin(char_point)[2:].zfill(point_mark_zfill)

            # If radix is none of above
            else:
                # Get error message
                error_msg = 'Invalid radix: {}'.format(repr(point_mark_radix))

                # Raise error
                raise ValueError(error_msg)

            # Draw point mark text
            combo_imagedraw.text(
                xy=(pixel_xpos, pixel_ypos),
                text=point_mark_text,
                font=point_mark_font,
                fill='red'
            )

    # Return combo image
    return combo_image


def chars_to_images(
    char_points,
    char_font,
    char_xpad=None,
    char_ypad=None,
):
    """
    Render characters to images.

    :param char_points: Character point list.

    :param char_font: Character font.

    :param char_xpad: Each character's X padding before and after. Format is \
        a tuple of two values.

    :param char_ypad: Each character's Y padding before and after. Format is \
        a tuple of two values.

    :return: Image list.
    """
    # Get font size
    font_size = char_font.size

    # If character x-padding is not given
    if char_xpad is None:
        # Use default
        char_xpad = (0, 0)

    # Ensure valid
    assert isinstance(char_xpad, tuple)

    assert len(char_xpad) == 2

    # If character y-padding is not given
    if char_ypad is None:
        # Use default
        char_ypad = (0, 0)

    # Ensure valid
    assert isinstance(char_ypad, tuple)

    assert len(char_ypad) == 2

    # Get cell xspan
    cell_xspan = char_xpad[0] + font_size + char_xpad[1]

    # Get cell yspan
    cell_yspan = char_ypad[0] + font_size + char_ypad[1]

    # Character image list
    char_image_s = []

    # For each character point
    for char_point in char_points:
        # Create character image
        char_image = Image.new(
            mode='RGBA',
            size=(cell_xspan, cell_yspan),
            color=(0, 0, 0, 0)
        )

        # Create character image's ImageDraw object
        char_imagedraw = ImageDraw.Draw(char_image)

        # Get character
        char = chr(char_point)

        # Draw the character to the character image
        char_imagedraw.text(
            xy=(char_xpad[0], char_ypad[0]),
            text=char,
            font=char_font,
            fill='black',
        )

        # Add the character image to list
        char_image_s.append(char_image)

    # Return character image list
    return char_image_s
