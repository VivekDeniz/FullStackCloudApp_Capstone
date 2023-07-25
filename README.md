# Full Stack Cloud Application Project

**Web Application to review fictious car dealerships**

## Context

As part of the final Capstone Project within the IBM Full Stack Cloud Developer Professional Certificate on Coursera, I developed an application. Initially, I received a basic version of the Django application from Coursera, lacking central functionality and templates. My responsibility entailed crafting the front-end views, implementing back-end services, and establishing cloud functions, all while seamlessly integrating them using the Django framework.

## Project Objective

The main objective was to create a website enabling users to select one of the fictional company "Best Car's" dealerships in the US. On this site, users can access reviews submitted by other users regarding the dealership's cars, and they can also contribute their own reviews. Additionally, the website included essential features such as a navigation bar and static pages for "about" and "contact" information. The project mandated the use of the Python-Django full stack web development framework and required deployment on Red Hat Openshift/Kubernetes hosted on the IBM Cloud.

## Architecture

The dealership and review data are stored in an IBM Cloudant database, while information about users and cars resides in a simple SQLite database. To retrieve data from IBM Cloudant, I developed three IBM Cloud Functions that were accessible through an API.

Furthermore, every review undergoes analysis by IBM Watson to determine its overall sentiment, classifying it as negative, neutral, or positive before being displayed.

![image](https://github.com/VivekDeniz/FullStackCloudApp_Capstone/assets/133251644/b55a4adb-8666-4bb8-b9d8-67caa10a97aa)

## Run on your machine 

**Clone project:**
 
 git clone https://github.com/VivekDeniz/agfzb-CloudAppDevelopment_Capstone.git

 cd FullStackCloudApp_Capstone/server

 python3 -m pip install -U -r requirements.txt 

**Start server:**

 python3 manage.py makemigrations djangoapp

 python3 manage.py migrate

 python3 manage.py runserver

**Create superuser:**
 
 python3 manage.py createsuperuser

 (add /admin at the end of url to access admin site)
 
 
 
