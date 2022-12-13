from indexing import main_query_fill
from indexing import dictionary_fill
from indexing import doctors_fill
from indexing import filter1
from indexing import filter2
# import nltk
import os
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
import math
import re
from collections import Counter
import requests
from bs4 import BeautifulSoup
import json

def modify_relevant_score(right_doctor_id):
    with open("./authentication/psuedo_relevant_score.txt", "r+") as myfile:
        relevant_score = myfile.read()
    relevant_score = relevant_score.split('\n')

    relevant_score[right_doctor_id] = int(relevant_score[right_doctor_id]) + 1
    f = open("./authentication/psuedo_relevant_score.txt", "w")
    for item in relevant_score:
        f.write(str(item) + "\n")
    f.close()

relevent = 0
with open("./authentication/relevent.txt", "r") as myfile:
    relevent = myfile.read()
    
with open("./authentication/doctor_order.txt", "r") as myfile:
    data = myfile.read()

my_order = data.split(' ')
my_order.pop()  
  

with open("./authentication/doctor_filter.txt", "r") as myfile:
    data = myfile.read()

my_filter = data.split(' ')
my_filter.pop()  

    
def feedback_relevent(relevent, my_order, my_filter) :
    id_doctor = relevent
    right_doctor = my_filter[int(id_doctor) - 1]
    right_doctor_id = my_order[int(right_doctor)]
    
    modify_relevant_score(int(right_doctor_id)) 
feedback_relevent(relevent, my_order, my_filter) 

filter_experiance = filter1()
filter_fees = filter2()

print("this is age", filter_experiance)
print("this is fees", filter_fees)

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
cities = cities[:100]
specialities = ['dentist', 'dermatologist', 'homoeopath', 'ayurveda']
# print(specialities)
# print(cities)

with open("./authentication/Data/input.txt", "r") as myfile:
    data = myfile.read().lower()

data = data.split('\n')
for i in range(0, len(data)):
    data[i] = data[i].split('\'')

doctors = []
doctors = doctors_fill(doctors, data)
# print(doctors)

dictionary = {}
dictionary = dictionary_fill(dictionary, doctors, cities, specialities)

main_query = []
main_query = main_query_fill(main_query)

WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


intersection_list = []
new_string_query = ""

found = 0
for item in main_query:
    for city in cities:
        if (city.lower() == item):
            found = 1
    for speciality in specialities:
        if (speciality.lower() == item):
            found = 1
    if (found == 0):
        file = open("./authentication/query.txt","w") 
        file.write("") 

        file = open("./authentication/age.txt","w") 
        file.write("")

        file = open("./authentication/fees.txt","w") 
        file.write("")
        print("Sorry, search again with better keywords!")
        exit()
    else:
        found = 0

if (len(main_query) == 0):
    file = open("./authentication/query.txt","w") 
    file.write("") 

    file = open("./authentication/age.txt","w") 
    file.write("")

    file = open("./authentication/fees.txt","w") 
    file.write("")
    print("Sorry! We couldn't find Doctor.")
    exit()
elif (len(main_query) == 1):
    intersection_list = dictionary[main_query[0]]
    new_string_query = new_string_query + main_query[0]
elif (len(main_query) == 2):
    intersection_list = list(
        set(dictionary[main_query[0]]) & set(dictionary[main_query[1]]))
    new_string_query = new_string_query + main_query[0]
    new_string_query = new_string_query + " " + main_query[1]
elif (len(main_query) > 2):
    file = open("./authentication/query.txt","w") 
    file.write("") 

    file = open("./authentication/age.txt","w") 
    file.write("")

    file = open("./authentication/fees.txt","w") 
    file.write("")
    print("Sorry, Query is not Searchable!")
    exit()

main_doctors = []
only_main_doctor = ""
if (len(intersection_list) > 0):
    for i in range(0, len(intersection_list)):
        for j in range(0, 7):
            if (j == 0):
                only_main_doctor = only_main_doctor + \
                    str(doctors[intersection_list[i]][j])
            else:
                only_main_doctor = only_main_doctor + " " + \
                    str(doctors[intersection_list[i]][j])
        main_doctors.append(only_main_doctor)
        only_main_doctor = ""

cosine_values = []
for i in range(0, len(main_doctors)):
    vector1 = text_to_vector(main_doctors[i])
    vector2 = text_to_vector(new_string_query)
    cosine = get_cosine(vector1, vector2)
    cosine_values.append([cosine, intersection_list[i]])

sorted(cosine_values)

with open("./authentication/psuedo_relevant_score.txt", "r+") as myfile:
    relevant_score_doctor = myfile.read()
relevant_score_doctor = relevant_score_doctor.split('\n')

matching_doctors_cosine = []
for item in cosine_values:
    matching_doctors_cosine.append(item[1])

matching_doctors_with_score = []
for item in matching_doctors_cosine:
    matching_doctors_with_score.append([[relevant_score_doctor[item]], item])
matching_doctors_with_score = sorted(matching_doctors_with_score, reverse=True)


matching_doctors = []
for item in matching_doctors_with_score:
    matching_doctors.append(item[1])

need_doctors = []
for item in matching_doctors:
    need_doctors.append(doctors[item])

filter_by_experiance = []
filter_by_fees = []
filter_by_both = []

if (len(filter_experiance) > 0 and len(filter_fees) > 0):
    j = 0
    for item in need_doctors:
        if ((int(item[1]) >= int(filter_experiance)) and (int(item[3]) <= int(filter_fees))):
            filter_by_both.append([item, j])
        j = j + 1
elif (len(filter_experiance) > 0):
    j = 0
    for item in need_doctors:
        if (int(item[1]) >= int(filter_experiance)):
            filter_by_experiance.append([item, j])
        j = j + 1
elif (len(filter_fees) > 0):
    j = 0
    for item in need_doctors:
        if (int(item[3]) <= int(filter_fees)):
            filter_by_experiance.append([item, j])
        j = j + 1

file = open("./authentication/query.txt","w") 
file.write("") 

file = open("./authentication/fees.txt","w") 
file.write("")

file = open("./authentication/age.txt","w") 
file.write("")

json_emp = None

# with open("./authentication/result_doctors.json", 'w') as outfile:
#     json.loads('') 

jsonlist = []          

f = open("./authentication/doctor_order.txt", "w")
for item in matching_doctors:
   f.write(str(item) + " ")
f.close()
   
f = open("./authentication/doctor_filter.txt", "w")
for item in filter_by_both:
   f.write(str(item[1]) + " ")
f.close()
    

if (len(filter_by_both) > 0):
    i = 1
    print("\n")
    for item in filter_by_both:
        print(i)
        
        json_string_one = { 
            "name" : item[0][0], 
            "speciality" : item[0][2], 
            "experiance" : item[0][1], 
            "fees" : item[0][3],
            "rating": item[0][4],
            "locality": item[0][5],
            "city": item[0][6]
        } 
        jsonlist.append(json_string_one)
        
        i = i + 1
        if (i == 11):
            with open("./authentication/relevent.txt", "r") as myfile:
                releventID = myfile.read()   
        
            with open("./authentication/result_doctors.json", 'w') as outfile:
                json.dump(jsonlist, outfile)
            exit()     
    with open("./authentication/result_doctors.json", 'w') as outfile:
        json.dump(jsonlist, outfile)        
    with open("./authentication/relevent.txt", "r") as myfile:
        releventID = myfile.read()
    recall = i / filter_by_both    
    precision = i / len(matching_doctors)
    exit()

elif (len(filter_by_experiance) > 0):
    i = 1
    print("\n")
    for item in filter_by_experiance:
        print(i)
        json_string_one = { 
            "name" : item[0][0], 
            "speciality" : item[0][2], 
            "experiance" : item[0][1], 
            "fees" : item[0][3],
            "rating": item[0][4],
            "locality": item[0][5],
            "city": item[0][6]
        } 
        jsonlist.append(json_string_one)
        i = i + 1
        if (i == 11):
            with open("./authentication/relevent.txt", "r") as myfile:
                releventID = myfile.read()        
            with open("./authentication/result_doctors.json", 'w') as outfile:
                json.dump(jsonlist, outfile)
            exit()
    with open("./authentication/relevent.txt", "r") as myfile:
        releventID = myfile.read()        
    with open("./authentication/result_doctors.json", 'w') as outfile:
        json.dump(jsonlist, outfile)
    recall = i / filter_by_both    
    precision = i / len(matching_doctors)    
    exit()

elif (len(filter_by_fees) > 0):
    i = 1
    print("\n")
    for item in filter_by_fees:
        print(i)
        json_string_one = { 
            "name" : item[0][0], 
            "speciality" : item[0][2], 
            "experiance" : item[0][1], 
            "fees" : item[0][3],
            "rating": item[0][4],
            "locality": item[0][5],
            "city": item[0][6]
        } 
        jsonlist.append(json_string_one)
        i = i + 1
        if (i == 11):
            with open("./authentication/relevent.txt", "r") as myfile:
                releventID = myfile.read()        
            with open("./authentication/result_doctors.json", 'w') as outfile:
                json.dump(jsonlist, outfile)
            exit()
    with open("./authentication/relevent.txt", "r") as myfile:
        releventID = myfile.read()    
    
    with open("./authentication/result_doctors.json", 'w') as outfile:
        json.dump(jsonlist, outfile)
    recall = i / filter_by_both    
    precision = i / len(matching_doctors)    
    exit()

if ((len(filter_by_both) == 0) and (len(filter_by_experiance) == 0) and (len(filter_by_fees) == 0)):
    i = 1
    print("\n")
    for item in need_doctors:
        print(i)
        json_string_one = { 
            "name" : item[0][0], 
            "speciality" : item[0][2], 
            "experiance" : item[0][1], 
            "fees" : item[0][3],
            "rating": item[0][4],
            "locality": item[0][5],
            "city": item[0][6]
        } 
        jsonlist.append(json_string_one)
        
        i = i + 1
        if (i == 11):
            with open("./authentication/relevent.txt", "r") as myfile:
                releventID = myfile.read()        
            with open("./authentication/result_doctors.json", 'w') as outfile:
                json.dump(jsonlist, outfile)
            exit()
    with open("./authentication/relevent.txt", "r") as myfile:
        releventID = myfile.read()        
    with open("./authentication/result_doctors.json", 'w') as outfile:
        json.dump(jsonlist, outfile)
    recall = i / filter_by_both    
    precision = i / len(matching_doctors)    
    exit()
       
