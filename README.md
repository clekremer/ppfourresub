# Osteopathy Patient Booking System

The Osteopathy Patient Booking System is web app for rquesting and scheduling Osteopathy appointment between Doctor and Patient. 

The live app can be accessed here - [Osteopathy Patient Booking System](https://pp4-pbooking-ea6d40f1e5c0.herokuapp.com/)

## Table of Contents

- [Patient Booking System](#patient-booking-system)
  * [User Experience](#user-experience)
    + [User Stories](#user-stories)
    + [Design](#design)
      - [Colours](#colours)
      - [Imagery](#imagery)
      - [Fonts](#fonts)
      - [Wireframes](#wireframes)
  * [Agile Methodology](#agile-methodology)
  * [Data Model](#data-model)
  * [Testing](#testing)
  * [Security Features and Defensive Design](#security-features-and-defensive-design)
    + [User Authentication](#user-authentication)
    + [Form Validation](#form-validation)
    + [Database Security](#database-security)
    + [Custom error pages:](#custom-error-pages-)
  * [Features](#features)
    + [Header](#header)
    + [Footer](#footer)
    + [Home Page](#home-page)
    + [Register Patient Page](#register-patient-page)
    + [Request Appointments](#request-appointments)
    + [Register Doctor](#register-doctor)
    + [Patient Dashboard](#patient-dashboard)
    + [Doctor Dashboard](#doctor-dashboard)
    + [Edit Appointment](#edit-appointment)
    + [Cancel Appointment](#cancel-appointment)
    + [Approve Appointment](#approve-appointment)
    + [Reject Appointment](#reject-appointment)

  * [Deployment - Heroku](#deployment---heroku)
  * [Languages](#languages)
  * [Frameworks - Libraries - Programs Used](#frameworks---libraries---programs-used)
  * [Credits](#credits)
  * [Acknowledgments](#acknowledgments)


## User Experience

The user is patient who want to get brief information about the service. He wants to have the possibility to request and manage Osteopathy appointments. 

### User Stories

#### EPIC | Register Patient
 - As a Patient I can register an account so that I can request/edit/cancel an appointment with a specific doctor.
 - As a Patient I can log in or log out of my account so that I can keep my account secure.
 - As a Patient I can access my Patient Dashboard
 - As a Patient I can see my login status so that I know if I'm logged in or out.

#### EPIC | Register Doctor 
 - As a Doctor I can register as doctor so that I receive and manage (approve, reject or cancel) appointment requests from Patients
 - As a Doctor I can log in or log out of my account so that I can keep my account secure.
 - As a Doctor I can access my doctor dashboard
 - As a Doctor I can see my login status so that I know if I'm logged in or out.

#### EPIC | Manage Appointments as Patient
 - As a Patient I can create and submit appointment requests so that I can create appointments with specific doctors.
 - As a Patient I can edit existing appointments and appointment request so that I can change date, time and reason for my appointment.
 - As a Patient I can cancel appointment requests and approved appointments so that I can cancel appointments when I don´t need them anymore.

#### EPIC | Mangae Appointments as Doctor 
 - As a Doctor I can approve appointment requests so that I can confirm an appointment to a patient.
 - As a Doctor I can reject appointment request so that I can tell the patient that he needs to suggest another date and time.
 - As a Doctor I can cancel an already answered appointment request when I cannot attend them.

#### EPIC | Patient Dashboard
 - As a Patient I can access my Patient Dashboard
 - As a Patient I can view my Patient details on Patient Dashboard
 - As a Patient I can view my appointment requests and my approved, rejected and canceled appointments on Patient Dashboard

#### EPIC | Doctor Dashboard
 - As a Doctor I can access my Doctor Dashboard
 - As a Doctor I can view my Doctor details on Doctor Dashboard
 - As a Doctor I can view my appointment requests and my approved, rejected and canceled appointments on Doctor Dashboard

#### EPIC | User Navigation 
 - As a Site User I can easily understand the Use Case of the site 
 - As a Site User I can intuitively navigate on the site and find the content and functionality I´m looking for 
 - As a Site User (Doctor or Patient) I can view the respective dashboard and view a paginated list of appointment requests and appointments

#### Not implemented User Stories 
 - As a patient or doctor I can edit my user details 
 - As a doctor I can enter my availabilities to show my patients when I have available appointments 
 - As patient I can view available time slots in a calender view for each doctor 

### Design

The page has a very simple design. Focus lies on the functionality and providing basic information to the patients. 

#### Colour 

#### Imagery

#### Fonts

#### Wireframes

Wireframes were created with Balsamiq.

<summary>Desktop Wireframe</summary>

![Desktop Wireframe - Home Login ](docs/readme_images/wireframe_home_login.png)
</details>

![Desktop Wireframe - Home Logout](docs/readme_images/wireframe_home_logout.png)
</details>

![Desktop Wireframe - Dashboard](docs/readme_images/wireframe_dashboard.png)
</details>

![Mobile Wireframe - Home](docs/readme_images/wireframe_mobile.png)
</details>

## Agile Methodology

Github projects was used to manage agile development.

## Data Model

![Database Schema](docs/readme_images/datamodel.png)

## Testing

Testing document and the testing results can be found [here](/TESTING.md)


## Security Features and Defensive Design

### User Authentication


### Form Validation


### Database Security

### Custom error pages

## Features

### Header

### Footer

### Home Page

### Register Patient Page

### Request Appointment

### Register Doctor

### Patient Dashboard

### Doctor Dashboard

### Edit Appointment

### Cancel Appointment

### Approve Appointment

### Reject Appointment


## Deployment - Heroku

The was deployed on Heroku by the following steps: 


### Create the Heroku App:
- Log in to [Heroku](https://dashboard.heroku.com/apps) 
- click button "Create New App"
- Enter a unique app name
- Select region (Europe)
- Click "Create App" button

### Setting tab:
- add DATABASE_URL in the Config Vars 
- add DISABLE_COLLECTSTATIC = 1 in the Config Vars 


### Prepare the env and settings.py file:
- In GitPod workspace, create an env.py file 
- Add the DATABASE_URL value and SECRET_KEY value to the env.py file 
- Update the settings.py to import the env.py file and add SECRETKEY and DATABASE_URL file paths
- Comment out the default database configuration
- Save files and make migrations
- Add the STATIC files settings - the url, storage path, directory path, root path and default file storage path.
- Link the file to the templates directory in Heroku.
- Change the templates directory to TEMPLATES_DIR
- Add Heroku to the ALLOWED_HOSTS list the format ['app_name.heroku.com', 'localhost']

### Create files / directories
- Create requirements.txt file
!!!- Create three directories in the main directory; media, storage and templates.???
- Create a file named "Procfile" in the main directory and add the following: web: gunicorn project-name.wsgi


### Deploy
- Ensure in Django settings, DEBUG is False
- Go to the deploy tab on Heroku and connect to the GitHub project 
- deploy the app by Automatic Deploys or deploy it manually
- Click View or open app button to load the deployed site.


## Languages

- Python
- HTML
- CSS
- Javascript

## Frameworks - Libraries - Programs Used
- [Django](https://www.djangoproject.com/): Framework to develop the app.
- [Heroku](https://dashboard.heroku.com/login) Cloud based platform for deployment of the app. 
- [Font Awesome](https://fontawesome.com/) Icons. 
- [GitHub](https://github.com/) Repository, version control and agile tool.
- [Google Fonts](https://fonts.google.com/) Fonts
- [W3C](https://www.w3.org/) Validation of HTML & CSS
- [PEP8 Online](http://pep8online.com/) Validation of Python code
- [Jshint](https://jshint.com/) Validation of javascript
- [Stack Overflow](https://stackoverflow.com/)
- [Update View](https://pytutorial.com/django-updateview-example)


## Acknowledgments

