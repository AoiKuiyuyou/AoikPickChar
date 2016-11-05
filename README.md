# AoikPickChar
Render picked font characters to images.

Tested working with:
- Python 2.7 and 3.5
- Linux
- MacOS
- Windows

![Image](https://raw.githubusercontent.com/AoiKuiyuyou/AoikPickChar/0.1.0/screenshot/screenshot.png)

## Table of Contents
- [Setup](#setup)
  - [Setup via pip](#setup-via-pip)
  - [Setup via git](#setup-via-git)
- [Usage](#usage)
  - [Run program](#run-program)
  - [Create combo image](#create-combo-image)
  - [Create character images](#create-character-images)

## Setup
- [Setup via pip](#setup-via-pip)
- [Setup via git](#setup-via-git)

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
- [Run program](#run-program)
- [Create combo image](#create-combo-image)
- [Create character images](#create-character-images)

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
