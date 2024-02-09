# 🚗 Car Model Data Scraper 📊

This Python script enables you to effortlessly gather comprehensive car model data from the Car Query API and export it into a CSV format. With robust filtering capabilities, you can refine your search based on manufacturer, model, variant, production year, and more. Dive into the world of automotive data with ease and flexibility!

## Features

- **Comprehensive Data:** Fetch detailed car model information from the Car Query API.
- **Flexible Filtering:** Refine your search by specifying manufacturer, model, variant, production year range, and whether the car is sold in the US.
- **Exclusion Words:** Exclude specific words from variant names to tailor your results.
- **Export to CSV:** Save filtered data to a CSV file for further analysis and visualization.

## Installation

1. **Clone the Repository:** 
    ```bash
    git clone https://github.com/Salman0x01/Car-Model-Data-Scraper.git
    ```

2. **Navigate to the Project Directory:** 
    ```bash
    cd Car-Model-Data-Scrapper
    ```

3. **Install Dependencies:** 
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Script:** 
    ```bash
    python main.py
    ```

2. **Follow the Prompts:** 
    - Enter the manufacturer, model, variant, production year range, and whether the car is sold in the US.
    - Leave fields blank to include all values or specify exclusion words in a file named `exclude_words.txt`.

3. **Review Results:** 
    - The script will fetch the data, apply your filters, and save it to a CSV file in the project directory.

## Example

Here's an example of using the script:

1. **Enter Manufacturer:** Honda
2. **Choose Model:** Civic
3. **Enter Variant:** 
4. **Production Year Range:** 2016 to 2021
5. **Sold in US:** Yes
6. **Exclusion Words:** Create a file named `exclude_words.txt` with words to exclude, one per line.
7. **Review Output:** The script will fetch, filter, and save the data to `honda-civic.csv`.

## Why Use This Script?

Online car data is often behind a paywall, but with this script, you can access it for free and with amazing filtering capabilities. 

## Credits

This script is developed by [Salman Arif Khan](https://sprotechs.com) from [Sprotechs](https://sprotechs.com).

## Fork and Contribute

Feel free to fork this repository and contribute to its development! Your contributions are greatly appreciated.
## Credits

This script utilizes the [Car Query API](https://www.carqueryapi.com/) to access car model data.
