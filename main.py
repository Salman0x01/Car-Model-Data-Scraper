import requests
import csv
import re
from prettytable import PrettyTable
from tqdm import tqdm

def fetch_models(make, timeout=10):
    url = f"https://www.carqueryapi.com/api/0.3/?cmd=getModels&make={make}"
    # print("Query URL:", url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an exception for bad response status
        data = response.json()

        if 'Models' in data:
            return [model['model_name'] for model in data['Models']]
        else:
            print("No models found for the provided manufacturer.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def fetch_car_data(make="", model="", variant="", from_year=None, to_year=None, sold_in_us=None, timeout=50):
    car_data = []
    if model:
        car_data.extend(fetch_variants(make, model, variant, from_year, to_year, sold_in_us, timeout))
    else:
        models = fetch_models(make, timeout)
        for model_name in tqdm(models, desc="Fetching variants"):
            car_data.extend(fetch_variants(make, model_name, variant, from_year, to_year, sold_in_us, timeout))
    return car_data

def fetch_variants(make, model, variant="", from_year=None, to_year=None, sold_in_us=None, timeout=50):
    url = f"https://www.carqueryapi.com/api/0.3/?cmd=getTrims&make={make}&model={model}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an exception for bad response status
        data = response.json()

        variants = []

        if 'Trims' in data:
            for variant_info in tqdm(data['Trims'], desc="Processing variants"):
                model_year = int(variant_info['model_year'])
                sold_in_us_bool = variant_info.get('sold_in_us', '').lower() == 'yes'
                if (variant == "" or variant.lower() == variant_info['model_trim'].lower()) and \
                   ((from_year is None or model_year >= from_year) and (to_year is None or model_year <= to_year)) and \
                   (sold_in_us is None or sold_in_us_bool == sold_in_us):
                    variants.append({
                        'vehicle_produced_since': variant_info['model_year'],
                        'vehicle_produced_until': "",  # Not provided by API
                        'vehicle_brand': make,
                        'vehicle_model': model,
                        'vehicle_variant': variant_info['model_trim']
                    })
    except requests.exceptions.RequestException as e:
        print(f"Error fetching variants: {e}")
    return variants

def write_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['vehicle_produced_since', 'vehicle_produced_until', 'vehicle_brand', 'vehicle_model', 'vehicle_variant']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in data:
            writer.writerow(item)

def sanitize_filename(filename):
    # Remove non-alphanumeric characters and replace spaces with hyphens
    return re.sub(r'[^a-zA-Z0-9]+', '-', filename.strip())

def print_table(data):
    table = PrettyTable()
    table.field_names = ["Model"]
    for item in data:
        table.add_row([item])
    print(table)

if __name__ == "__main__":
    make = input("Enter the manufacturer (e.g., Honda): ")
    models = fetch_models(make)
    if models:
        print("\nAvailable Models:")
        print_table(models)
        
        model = input("Enter the model (leave blank for all): ")
        variant = input("Enter the variant (leave blank for all): ")
        from_year = input("Enter the from year (leave blank for all): ")
        to_year = input("Enter the to year (leave blank for all): ")
        sold_in_us_input = input("Sold in US? (yes/no, leave blank for all): ")

        # Convert input years to integers or leave them as None
        from_year = int(from_year) if from_year else None
        to_year = int(to_year) if to_year else None

        # Convert sold_in_us_input to boolean or leave it as None
        if sold_in_us_input.lower() == 'yes':
            sold_in_us = True
        elif sold_in_us_input.lower() == 'no':
            sold_in_us = False
        else:
            sold_in_us = None

        car_data = fetch_car_data(make, model, variant, from_year, to_year, sold_in_us, timeout=50)  # Increased timeout to 30 seconds
        if car_data:
            # Generate filename based on make and model
            if model:
                filename = f"{sanitize_filename(make)}-{sanitize_filename(model)}.csv"
            else:
                filename = f"{sanitize_filename(make)}.csv"
            
            write_to_csv(filename, car_data)
            print(f"\nData has been written to {filename}")
        else:
            print("\nNo data found matching the provided criteria.")
    else:
        print("No models found for the provided manufacturer.")
