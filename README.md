# Scraping Giallo Zafferano

This project aims at downloading every recipe from [Giallo Zafferano](https://www.giallozafferano.it/) using Python with the [Requests](https://pypi.org/project/requests/) package, analyzing them with [Beautifoul Soup](https://pypi.org/project/beautifulsoup4/) and then saving them in [JSON](https://www.json.org/json-en.html) format.

## How to use

To use this project you'll need [Python3](https://www.python.org/) and [Pip](https://pypi.org/project/pip/) installed.

1. Clone this repo in a folder of your choice.
2. Install the necessary packages using ` pip install -r requirements.txt `.
3. Run `runme.py` using `py runme.py`. The time needed to download all the recipes can vary. In my case it took ~4 hours.

Additionally you can:

- Count how many recipe you managed to download by running `count_downloaded_pages.py` with `py count_downloaded_pages.py`.
- Order the recipe based on their category by running `find_categories.py` with `py find_categories.py`

## How to contribute

If you want to contribute: **thank you!**

To contribute just clone this repo and once you're done open a Pull Request.

Right now it would be very good to improve the download speed (maybe using multi threading?) and create a list of all the ingredients.

The problem with the second objective is that a certain ingredient (e.g. _zucchina_) can be found in multiple forms and may be misspelled (e.g. _Zuchina_).
