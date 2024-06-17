import Categories
from datetime import date
import os
import re


def textDict(climate_data):
    for row in climate_data:
        split_row = row.split(",")

        if len(split_row) < 17:
            continue

        code = split_row[1].strip()
        if code not in code_text:
            continue

        calculations = ['count', 'count %', 'sum', 'mean', 'max', 'min']
        if split_row[2].strip().lower() not in calculations:
            continue

        empty = True
        for i in range(4, len(split_row)):
            if re.search('[0-9]', split_row[i]):
                empty = False
                break
        if empty:
            continue

        curr_text = code_text[code]
        
        i = 4
        month_num = 1

        new_section = ""
        if curr_text == "precipitation mm":
            new_section = "| precipitation colour = green\n"
        if curr_text == "precipitation days":
            new_section = "| unit precipitation days = 1.0 mm\n"

        while month_num <= 13:
            month = months[month_num]
            data = split_row[i].strip()
            if '.' in data:
                data = float(data)
                data = round(data, 1)
            if data != '':
                new_section += "| {} {} = {}\n".format(month, curr_text, data)

            i += 1
            month_num += 1

        text_dict[code] = new_section

    return text_dict


if __name__ == '__main__':
    file_path = input("File path: ")
    url = input("URL: ")
    location = input("location: ")
    country = input("country: ")

    months = Categories.month
    code_text = {
        '1':'precipitation mm', 
        '2':'precipitation days', 
        '3':'high C', 
        '4':'low C', 
        '5':'mean C', 
        '8':"sun", 
        '22': 'record high C', 
        '23': 'record low C', 
        '37': 'snow cm', 
        '38': 'humidity', 
        '39': 'dew point C'
    }
    code_order = ['22', '3', '5', '4', '23', '1', '37', '2', '38', '39', '8']
    text_dict = {}

    header = Categories.header.format(location)
    date_string = date.today().strftime("%B %-d, %Y")
    footer = Categories.footer.format(url, location, date_string)

    weather_box = header

    climate_data = open(file_path, newline='')
    climate_data.readline()

    text_dict = textDict(climate_data)

    climate_data.close()

    for code in code_order:
        if code in text_dict:
            weather_box += text_dict[code]

    weather_box += footer

    if country == "":
        path = location + '.txt'
    else:
        path = country + '/' + location + '.txt'

    parent_dir = os.getcwd()

    if not os.path.exists(parent_dir+'/'+country+'/'):
        os.makedirs(parent_dir+'/'+country+'/')
    
    with open(path, "w") as weatherBoxes:
        print(weather_box, file=weatherBoxes)
