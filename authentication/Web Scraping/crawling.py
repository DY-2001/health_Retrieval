import requests
from bs4 import BeautifulSoup
import re


def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def get_cities():
    response = requests.get(
        'https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population')
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='wikitable sortable')
    cities = []
    for row in table.find_all('tr')[1:]:
        city = row.find_all('td')[1].text
        res = city.split('[')[0]
        cities.append(res)
    return cities


cities = get_cities()
specialities = ['Dentist','Dermatologist', 'Homoeopath', 'Ayurveda']

url = 'https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22${speciality}%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22subspeciality%22%7D%5D&city=${city}&page=${page}'
full_Data = []
doctor_experiance = []
doctor_fees = []
doctor_city = []
doctor_speciality = []
doctor_name = []
doctor_rating = []
doctor_locality = []
fees_consultation = []

for city in cities[:100]:
    for page in range(1, 10):
        for speciality in specialities:
            if (check_url(url.replace('${city}', city).replace('${page}', str(page)).replace('${speciality}', speciality))):
                response = requests.get(url.replace('${page}', str(page)).replace(
                    '${city}', city).replace('${speciality}', speciality))
                htmlContent = response.content
                soup = BeautifulSoup(htmlContent, 'html.parser')
                
                list_name = soup.find_all("h2", class_="doctor-name")
                for t in list_name:
                    doctor_name.append(t.get_text())
                    
                
                
                list_fees = soup.find_all("div", class_="uv2-spacer--xs-top")
                for t in list_fees: 
                    if(re.search(r'\d+', t.get_text())):
                        fees_consultation.append(re.search(r'\d+', t.get_text()).group())
                for t in fees_consultation:
                    if(int(t) < 60): 
                        doctor_experiance.append(t)
                    else: 
                        doctor_fees.append(t)    
                
                
                doctor_city.append(city)
                doctor_speciality.append(speciality)
                
                
                list_rating = soup.find_all("span", class_="o-label--success u-bold")
                for t in list_rating:
                    doctor_rating.append(t.get_text())
                
                
                list_locality = soup.find_all("div", class_="u-bold u-d-inlineblock u-valign--middle")
                for t in list_locality: 
                    doctor_locality.append((t.get_text()).split(',')[0])
                    
# print(doctor_fees)
# print(doctor_experiance)                
# print(doctor_name)
# print(doctor_rating)
# print(doctor_locality)

# print(len(doctor_fees))
# print(len(doctor_experiance))                
# print(len(doctor_name))
# print(len(doctor_rating))
# print(len(doctor_locality))

length_of_features = []
length_of_features.append(len(doctor_city))
length_of_features.append(len(doctor_experiance))
length_of_features.append(len(doctor_fees))
length_of_features.append(len(doctor_locality))
length_of_features.append(len(doctor_name))
length_of_features.append(len(doctor_speciality))
length_of_features.append(len(doctor_rating))

lowest_length = min(length_of_features)

doctors = []
for i in range(0, lowest_length):
    doctors.append([doctor_name[i], doctor_experiance[i], doctor_speciality[i], doctor_fees[i], doctor_rating[i], doctor_locality[i], doctor_city[i]])

f = open("./Data/input.txt", "w")
for item in doctors:
   f.write(str(item) + "\n")
f.close()

