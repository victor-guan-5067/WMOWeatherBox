import Categories
from datetime import date


def aggYear(months, temp, decPlaces) :
    divideBy = 12 if temp else 1
    
    total = 0
    places = ''
    if decPlaces == 1:
        places = '{:.1f}'
    elif decPlaces == 2:
        places = '{:.2f}'

    for i in range(len(months)):
        month = float(months[i])
        total += month
    
    year_avg = places.format(total/divideBy)
    return float(year_avg)


def work(file_path):
    if ".txt" in file_path:
        txtSort(file_path)
    else:
        print("invalid file type")


def csvSort(file_path):

    catNums = {2:'precipitation inch', 3:'snow inch', 4:'mean F', 5:'high F', 6:'low F'}

    precips = []
    means = []

    climate_data = open(file_path, newline='')
    climate_data.readline()

    for row in climate_data:
        split_row = row.split(",")
        
        for i in range(2, len(split_row)):
            month_data = split_row[i].replace(' ','')
            month_data = month_data.replace('"','')
            month_data = month_data.replace('\n', "")

            cat = catNums[i]

            if (cat == 'precipitation inch'):
                precips.append(month_data)
            if (cat == 'mean F'):
                means.append(month_data)
        
    climate_data.close()

    mean_temp = aggYear(means, True, 1)
    mean_precip = aggYear(precips, False, 2)

    print(calculateKoppen(means, precips, mean_temp, mean_precip))


def txtSort(file_path):
    climate_data = open(file_path, 'r')
    lines = climate_data.readlines()

    temps = []
    precips = []
    mean_temp = 0
    mean_precip = 0
    for line in lines:
        place = line.rfind('=') + 1

        if len(temps) < 12 and "mean" in line:
            temp = float(line[place:-1])
            temps.append(temp)
        elif "year mean" in line:
            mean_temp = float(line[place:-1])
        if len(precips) < 12 and "precipitation" in line:
            precip = float(line[place:-1])
            precips.append(precip)
        elif "year precipitation " in line:
            mean_precip = float(line[place:-1])
    
    print(calculateKoppen(temps, precips, mean_temp, mean_precip))


def calculateKoppen(temps, precips, mean_temp, mean_precip):
    if max(temps) < 10:
        if 0 < max(temps) < 10:
            return "ET (tundra)"
        else:
            return "EF (ice cap)"
        
    total_precip = 0
    summer_precip = 0

    for precip in precips:
        total_precip += precip
    
    for i in range(4, 10):
        summer_precip += precips[i]
    
    summer_p_ratio = summer_precip/total_precip

    if summer_p_ratio >= 0.7:
        arid_limit = (mean_temp * 20) + 280
    elif 0.3 < summer_p_ratio < 0.7:
        arid_limit = (mean_temp * 20) + 140
    else:
        arid_limit = mean_temp * 20

    print(summer_p_ratio)
    print(arid_limit)

    if total_precip/arid_limit < 0.5:
        if mean_temp >= 18:
            return "BWh (hot desert)"
        else:
            return "BWk (cold desert)"
    elif 0.5 <= total_precip/arid_limit < 1:
        if mean_temp >= 18:
            return "BSh (hot steppe)"
        else:
            return "BSk (cold steppe)"
    
    if min(temps) >= 18:
        if min(precips) >= 60:
            return "Af (tropical rainforest)"
        elif min(precips) >= (100 - mean_precip/25):
            return "Am (tropical monsoon)"
        else:
            return "Aw (tropical savanna)"

    if min(temps) <= -3:
        classification = "D"
    elif -3 < min(temps) <=0:
        classification = "C/D"
    else:
        classification = "C"

    summer_half = precips[4:10]
    winter_half = precips[1:4] + precips[10:]
        
    if min(summer_half) < 0.33 * max(winter_half) and min(summer_half) < 30:
        classification += "s"
    elif min(winter_half) < max(summer_half)/10:
        classification += "w"
    else:
        classification += "f"

    list.sort(temps, reverse=True)
    if max(temps) >= 22:
        classification += "a"
    elif temps[3] >= 10:
        classification += "b"
    elif min(temps) <= -38:
        classification += "d"
    else:
        classification += "c"

    return classification


if __name__ == '__main__':
    file_path = input("File path: ")
    work(file_path)
