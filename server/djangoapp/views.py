from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import  get_dealers_from_cf,get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, analyze_review_sentiments, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime, date
import logging
import json


# Get an instance of a logger
logger = logging.getLogger(__name__)


# `about` view to render a static about page
def about(request):
    return render(request, 'static/about.html')


# `contact` view to return a static contact page
def contact(request):
   return render(request, 'static/contact.html')

# `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'static/registration.html', context)
    else:
        return render(request, 'static/registration.html', context)

# `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')
    

# `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    if request.method == 'GET' :
        return render(request, 'static/registration.html', context)
    elif request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try: 
            User.objects.get(username=username)
            user_exist = True
        except:   
            logger.debug("{} is new user".format(username))
        if not user_exist:
           user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            # might have to use redirect function
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)


# `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/75bcf489-4367-4f44-bc60-f2601af99c15/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)




#  `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/75bcf489-4367-4f44-bc60-f2601af99c15/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(url, id)
        context["dealer"] = dealer
    
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/75bcf489-4367-4f44-bc60-f2601af99c15/dealership-package/get-reviews"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)

#  `add_review` view to submit a review
def add_review(request, id):
    if request.user.is_authenticated:
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/75bcf489-4367-4f44-bc60-f2601af99c15/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
        if request.method == "GET":
            cars = CarModel.objects.all()
            context["cars"] = cars
            print(context)
            return render(request, 'djangoapp/add_review.html', context)
        
        if request.method == "POST":
            review = {}
            review["name"] = request.user.first_name + " " + request.user.last_name
            form = request.POST
            review["dealership"] = id
            review["review"] = form["content"]
            if(form.get("purchasecheck") == "on"):
                review["purchase"] = True
            else:
                review["purchase"] = False
            if(review["purchase"]):
                datetime = form["purchasedate"]
                review["purchase_date"] = datetime#.strftime("%Y-%m-%d")
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year.strftime("%Y")
            post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/75bcf489-4367-4f44-bc60-f2601af99c15/dealership-package/post-review"
            json_payload = { "review": review }
            post_request(post_url, json_payload, id=id)
            return redirect("djangoapp:dealer_details", id=id)
    else:
        return redirect("/djangoapp/login")

