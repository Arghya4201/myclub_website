>>>>>
Things to do to start a django project
-> Start the project using "django-admin startproject PROJECT_NAME"
-> Make the app using "python manage.py startapp APP_NAME"
-> Then apply migrations using "python manage.py makemigrations" and then "python manage.py migrate" this will generate the migrations and the db i.e sqlLite
-> Then register the app ins Installed apps of settings.py eg: APPNAME.apps.homeconfig (will get the app name from apps.py of the app)
-> Make the static and template folders
-> Set those directories in setting.py

>>>>>
Steps to make the db:

-> create the table and define the cols in models.py
-> register the model in admin.py
-> Copy app name (className) from apps.py and copy paste that name in the INSTALLED APPS array in setting.py (This step is like adding our manually made app into the installed apps list of our project)
-> The run these 2 commands:
     i> python manage.py makemigrations #To generate migration files i.e make the changes and store in a file based on your model

     ii> python manage.py migrate #to apply those migrations to the database
     
>>>>>
To access the objects in the databases, we run the command "python manage.py shell" to enter query mode
  after this we can run queries in the terminal to access the objects as shown below

  from home.models import contact (imports the contact table)
  Contact.objects.all() (gives list of all objects in Contact table)
  Contact.objects.all()[0] (Gives first object)
  Contact.objects.filter(name="Arghya) (Filters out the objects where name="Arghya")

  How to change an instance:

  ins = Contact.objects.filter(name="Arghya) //get the instance
  ins.name = "Arghya Bhowmick" // change the value
  ins.save() //save

  exit() //to exit query mode
  There are many more in "Making queries django webpage"

>>>>>
Path Converters:
int: numbers
str: strings
path: whole urls/
slug: underscore and hyphened stuffs
UUID: universally unique ID

>>>>>
Safe rendering
-> typing {{calender}} would just print the HTML
-> typing {{calender|safe}} renders the calender

>>>>>
ReadMe_MyclubWesite 1
      We are mentioning 'home' inside that url tag is beacause we want to render the home page and in urls.py we have path('',views.home, name='home') i.e we mention whatever is there in the name attribute

>>>>>
Readme_myClubWebsite2
    same as ReadMe MyclubWesite 1 but now we are passing parameters,so same views.home funtion will be called but now with manually sent parameters (function overloading)

>>>>>
Readme_myClubWebsite3
    one event will have only one venue so one to one relationship, hence using foreign key() method to connect the tables.
    The ondeletemodelCascade denotes that if an event is deleted also delete the venue table associated with it.

    but one event can have many users attendting it so its a many to many relationship
    Here we are not using ondeleteCascade because event if event is deleted, the users would remain in the website we donot want to kick them out of website

>>>>>
    In views.py file we can import models by writing .models as models.py and views.py are in same directory. But for templates like home.html and event.html, we write events/home.html because views.py is not in the same directory as those pages. Hence its foldername/filename.html. These are the paths of the file from templates folder (templates is in same directory as views.py)

>>>>>
Readme_myClubWebsite4
    -> Changing the admin area a bit
    -> Now the admin page will display the 3 cols of name address and zip code and they -> will be displayed in alphabetical order of the col 'name'
    -> Also added 2 search fields
    ->All these changes would be reflected in 'venue' page of the admin page since we made these after registering the venue model

>>>>>
Readme_myClubWebsite4
    ->We want only users with admin access to be able to be manager
    ->Since its a major and internal change so we first delete all the events
    ->So we imported the django User at top

    models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    ->The 'User' in the argument links it to those admin users
    ->on_delete=models.SET_NULL means that if the manager gets deleted then just set the namager fileds to NULL for all those events where that person was the manager
    ->on_delete=models.CASCADE would have deleted those events if the manager got deleted
    Note* Since its a change to our models.py file so we need to do 'python manage.py makemigrations' and 'python manage.py migrate'

>>>>>
Readme_myClubWebsite5
    ->Creating a form for venue model that is why we mention 'model=Venue'
    ->fields = '__all__' creates a form with all the fields in the Venue model. We can also mention seperately if we want
    -> This is a vustom form class named VenueForm and we can call an instance of this in our views methods like in add_venue and update_venue function function

>>>>>
Readme_myClubWebsite6
    ->This method is first checking if form is already submitted or not, initially not submitted hence submitted = false
    ->If the method is POST(i.e when data is sent) and the data sent is valid(i.e all fields are filled appropriately) then the data is saved and the user is redirected to the URL '/add_venue?submitted=True'
    ->The form is also instantiated with the data submitted by the user 
    form = VenueForm(request.POST)

    ->Now in the else part if form is not submitted, then it means form had been submitted previously so we instantiate the 'form' variable with default/no value 
    form = VenueForm(). 
    Hence the form is empty and ready to accept new entry. Its kind of making an int variable 0 and re-initializing it
    
    ->To check if its submitted we use 
      if 'submitted' in request.GET
    This GET method would check the things after ? in URL and if it finds submitted (which it will due to form redirection URL after submission) then we set submitted= TRUE
    ->If nothing of these 2 happens i.e neither details are submitted nor we have submitted in URL so GET method doesn't get submitted, we again just render the venuw form page with default form and submitted value

>>>>>
Readme_myClubWebsite7

->Every object in a model has an uniqueID. So we use that to display each of them seperately
->The flow used here is
   . Pass the id in the URL as done in urls.py file "show_venue/venueID"
   . Then pass that venueID in the view method
   . Get that particular venue by using the passed venuwID of that particular object using the venueID as a primaryKey (pk)
   . The get method gets the venueID from the URL 
   . Return and render the particular venue page and pass the venue as context

>>>>>
Readme_myClubWebsite8

->Making another instance of Venueform class. Since its the instance of the same class that we used to add the venue so we dont have to create the form structure again, just re-use it
->The prev line had the details/instance of a particular venue stored in the 'venue' variable using the respective primary key, so we pass that in the form so that the generated form would already have the details filled of that form
->Update function means update the data and then submit
  . When updating then no data is posted so method = none (filling out the form)
  . When submitting the updated data the for type is post (submitting the filled form)
  In case of update in both these cases we want to render the update_venue html page so we included both condition in the form, (post and none)
-> When someone submits data to the form we heck if its valid, save the form and redirect back to the venue list page

Readme_myClubWebsite9
-> since the UserCreationForm is given by django and there is no html written by us so we add the attribute of class=form-control in the way shown in the above lines. This would bootstrap-ify the attributes
-> We had added the first_name , last_name and email fields in the registration form by ourselves. But the fields of username , password1 and password2 are auto given by UserCreationForm class so to add attributes to them we need to do it inside the in__it() method as shown
