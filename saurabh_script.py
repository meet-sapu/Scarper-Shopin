import csv
import json
import requests
import os

# this will be global variable

# gender = "WOMAN" 
gender = "MAN" 

# output_file = "saurabh_output_woman.csv"
output_file = "saurabh_output_man.csv"

# file_path = './WomanAll.json'
input_file_path = './ManAll.json'


size_codes = ["01", "02", "03", "04", "05", "06", "07", "26", "28", "30", "32", "34", "36", "38", "40", "42", "44", "46", "48"]
try_with = ["I2024", "I2025"]


headers = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

def append_size_codes(zara_code, api_string):
    api1 = api_string
    api2 = api_string
    for size_code in size_codes:
        api1 += f"&references={zara_code}{size_code}-{try_with[0]}"
        api2 += f"&references={zara_code}{size_code}-{try_with[1]}"
    return api1, api2
        

def create_api_string(zaraCode):
    s = "https://www.zara.com/in/en/store-stock?physicalStoreIds=16156"
    api1, api2 = append_size_codes(zaraCode, s)
    api1 += f"&sectionName={gender}&ajax=true"
    api2 += f"&sectionName={gender}&ajax=true"
    return api1, api2

# fetch data from any one of the apis
def fetch_data_from_apis(api1, api2):
    response1 = requests.get(api1, headers=headers)
    response2 = requests.get(api2, headers=headers)
    data1 = response1.json()
    data2 = response2.json()
    x = data1.get("productAvailability", [])
    y = data2.get("productAvailability", [])
    if(len(x)>0):
        return x
    if(len(y)>0):
        return y
    return "NA"


def write_data_to_csv(sku_id, color_code, size_code, size, stock, file_path=output_file):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["SKU ID", "Color Code", "Size Code", "Size", "Stock"])
        writer.writerow([sku_id, color_code, size_code, size, stock])

 
def process_product_availability(zara_product):
    print(zara_product)
    print("\n")
    for store in zara_product:
        available_products = store.get('availableProducts', [])
        for product in available_products:
            reference = product.get('reference')
            size = product.get('size')
            stock = product.get('stock')
            reference = reference.split('-')[0]
            sku_id = reference[:-5]
            size_code = reference[-2:]
            color_code = reference[-5:-2]
            # print(f"SKU: {sku_id}, Color: {size_code}, Size: {size}, Stock: {stock}, Color Code: {color_code}")
            write_data_to_csv(sku_id, color_code, size_code, size, stock)


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for json_object in data:
            zaraCode = json_object['sku_id'] + json_object['color_code'] 
            api1, api2 = create_api_string(zaraCode)
            data = fetch_data_from_apis(api1, api2)
            if data == "NA":
                print(f"No data fetched for {zaraCode}")
                continue
            else:
                process_product_availability(data)


if __name__ == "__main__":
    read_json_file(input_file_path)

