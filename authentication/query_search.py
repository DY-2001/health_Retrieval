def query_finding():
    query = input('Search for your Doctor : ')
    return query

def filter1():
    asking_for_filter_experiance = input('If you want filter by Year of Experiance type yes otherwise no : ')
    filter_experiance = ""
    if(asking_for_filter_experiance.lower() == "yes"):
        filter_experiance = input('Type the year of experiance Doctor should have :')
    return filter_experiance

def filter2():    
    asking_for_filter_fees = input('If you want filter by consultation fees type yes otherwise no : ')
    filter_fees = ""
    if(asking_for_filter_fees.lower() == "yes"):
        filter_fees = input('Type the atmost fees Doctor should have :')    
    return filter_fees