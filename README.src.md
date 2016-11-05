[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
# AoikPickChar
Render picked font characters to images.

Tested working with:
- Python 2.7 and 3.5
- Linux
- MacOS
- Windows

![Image](https://raw.githubusercontent.com/AoiKuiyuyou/AoikPickChar/0.1.0/screenshot/screenshot.png)

## Table of Contents
[:toc(beg='next', indent=-1)]

## Setup
[:tod()]

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikPickChar
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikPickChar

cd AoikPickChar

python setup.py install
```

## Usage
[:tod()]

### Run program
Run:
```
aoikpickchar
```
Or:
```
python -m aoikpickchar
```
Or:
```
python AoikPickChar/src/aoikpickchar/__main__.py
```

### Create combo image
Run:
```
aoikpickchar --min 0 --max 255 --font DejaVuSans.ttf --font-size 30 --xpad 12 --ypad 12 --mark-radix hex --draw-combo --view-combo
```

### Create character images
Run:
```
aoikpickchar --min 0 --max 255 --font DejaVuSans.ttf --font-size 30 --xpad 12 --ypad 12 --draw-each
```
