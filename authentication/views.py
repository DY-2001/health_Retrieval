# from contextlib import _RedirectStream
import django
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.http import HttpResponse
# django.setup()
import json
# from similarity import feedback_relevent


# from myapp.models import MyModel
# from django.contrib.auth.models import User
# from django.contrib import messages
import os
# from similarity import doctors_fill

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def searching(request):
    if request.method == "POST":
        inputID = request.POST['inputID']
        ageID = request.POST['ageID']
        feesID = request.POST['feesID']
        
        print("both ageID and feesID in views" + " " + ageID + " " + feesID)
        # myuser = User.objects.create_user(inputID)
        # myuser.save()
        
        # messages.success(request, "your Account has been successfully created.")
        file = open("./authentication/query.txt","w") 
        file.write(inputID) 
        file = open("./authentication/fees.txt","w") 
        file.write(feesID)
        print("both ageID and feesID in views" + " " + ageID + " " + feesID)
        file = open("./authentication/age.txt","w") 
        file.write(ageID)
        file.close()
        print("both ageID and feesID in views" + " " + ageID + " " + feesID)
        
        os.system('python ./authentication/similarity.py')
        with open("./authentication/result_doctors.json", "r") as file:
            doctors = json.load(file) 
        return render(request, "authentication/result.html", {'doctors': doctors}) 
       
def relevent(request):     
    if request.method == "POST":
        releventID = request.POST['releventID']
        
        file = open("./authentication/relevent.txt","w") 
        file.write(releventID)
        return render(request, "authentication/relevent.html")

