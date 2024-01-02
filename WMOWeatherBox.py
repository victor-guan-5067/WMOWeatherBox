import Categories
from datetime import date


def makeTable(file_path, location):
    months = Categories.month
    codeText = {'1':'precipitation mm', '2':'precipitation days', '3':'high C', '4':'low C', '5':'mean C', '8':"sun", '22': 'record high C', '23': 'record low C', '37': 'snow cm', '38': 'humidity', '39': 'dew point C'}
    code_order = ['22', '3', '5', '4', '23', '1', '37', '2', '38', '39', '8']
    text_dict = {}

    header = Categories.header.format(location)
    date_string = date.today().strftime("%B %-d, %Y")
    footer = Categories.footer.format(location, date_string)

    weather_box = header

    climate_data = open(file_path, newline='')
    climate_data.readline()

    for row in climate_data:
        split_row = row.split(",")

        code = split_row[1].strip()

        if code in codeText and split_row[2].strip() != "NOY":
            curr_text = codeText[code]
            
            i = 4
            month_num = 1

            if len(split_row[i:]) >= 13:
                new_section = ""
                if curr_text == "precipitation mm":
                    new_section = " | precipitation colour = green\n"
                if curr_text == "precipitation days":
                    new_section = " | unit precipitation days = 1.0 mm\n"

                while month_num <= 12:
                    month = months[month_num]
                    new_line = " | {} {} = {}\n".format(month, curr_text, split_row[i])
                    new_section += new_line
                    i += 1
                    month_num += 1

                new_section += " | year {} = {}\n".format(curr_text, split_row[i])
                text_dict[code] = new_section

    climate_data.close()

    for code in code_order:
        if code in text_dict:
            weather_box += text_dict[code]

    weather_box += footer

    path = location + '.txt'
    
    with open(path, "w") as weatherBoxes:
        print(weather_box, file=weatherBoxes)


if __name__ == '__main__':
    filePath = input("File path: ")
    location = input("location: ")
    makeTable(filePath, location)