from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

#Import the category model
from pictaroo.models import Category, Image, UserProfile
from pictaroo.forms import CategoryForm, ImageForm, UserProfileForm
from datetime import datetime

#geez dem cookies
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val =default_val
    return val

def visitor_cookie_handler(request):
    #get the number of visits to the site
    #we use the COOKIES.get() function to obtain the visits cookie
    #if the cookie exists, the value returned is casted to an integer.
    #if the cookie doesn't exist, then the default value of 1 is used
    visits = int(request.COOKIES.get('visits', '1'))

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    #if its been more than a day since the last visit
    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        #update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits=1
        #set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    #Update/set the visits cookie
    request.session['visits'] = visits

def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    image_list = Image.objects.order_by('-views')[:5]

    context_dict={'categories':category_list,'images':image_list}
    #call function to handle the cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # obtain our Response object early so we can add cookie information
    response = render(request, 'pictaroo/index.html', context_dict)

    #return response back to the user, updateing any cookies that need changed
    return response


#Create a new view method called about which return the below Http response
def about(request):
    visitor_cookie_handler(request)
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    #print out whether the method is GET or a POST
    print(request.method)
    #print out the user name, if no one is logged in it prints 'AnonymousUser'
    print(request.user)

    context_dict={}
    context_dict['visits'] = request.session.get('visits',0)


    response = render(request, 'pictaroo/about.html', context_dict)

    return response

def show_category(request, category_name_slug):
    #create a context dictionary which we can pass
    #to the template rendering engine
    context_dict = {}

    try:
        #can we find a category name slug with the given name?
        #if we can't the .get() method raises a does not exist exception
        #so the .get() method returns one model instance or riases an exception
        category = Category.objects.get(slug=category_name_slug)

        #Retrieve all of the associated images
        #note that filter() will return a list of image objects or an empty list
        images = Image.objects.filter(category=category)

        #add our results list to the template context under name images
        context_dict['images'] = images
        #we also add the category object from
        #the databse to the context dictionary
        #we'll use this in the template to verify that the category exist
        context_dict['category'] = category
    except Category.DoesNotExist:
        #we get here if we didnt find the specified category
        #dont do anything -
        #the template will display the 'no category message for us'
        context_dict['category']=None
        context_dict['images']=None


        # Return a render response to send to the client
        # we make use of the shortcut function to make our lives easier
        # note that the first parameter is the template we wish to use
    return render(request, 'pictaroo/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    # A HTTP post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # HAVE WE BEEN PROVIDED WITH A VALID FORM?
        if form.is_valid():
            # save the new category to the databse
            form.save(commit=True)
            # Now that the category is saved
            # we could give a cofirmation mesage
            # but since the most recent category added is on the index page
            # then we can direct the user back to the index page
            return index(request)
        else:
            # the supplied form contained errors
            # just print them to the terminal
            print(form.errors)

        # Will handle the bad form, new form or no form supplied cases
        # render the form with error message (if any)
    return render(request, 'pictaroo/add_category.html', {'form': form})

def add_image(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            if category:
                image = form.save(commit=False)
                image.category = category
                image.views= 0
                image.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render (request, 'pictaroo/add_images.html', context_dict)


@login_required
def my_account(request, username):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form =UserProfileForm({'picture':userprofile.picture })

    if request.method =='POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('my_account', user.username)
        else:
            print(form.errors)


    return render(request, 'pictaroo/myAccount.html', {'userprofile': userprofile, 'selecteduser': user, 'form':form})


@login_required
def my_comments(request):
    return render(request, 'pictaroo/myComments.html')

@login_required
def my_favourites(request):
    return render(request, 'pictaroo/myFavourites.html')

@login_required
def my_uploads(request):
    return render(request, 'pictaroo/myUploads.html')


# Chapter 14 Make Rango Tango - Create a Profile Registration view, corresponding view to handle the processing
# of a UserProfileForm. the subsequent creation of a new UserProfile instance and instructing Django to
# render any response with the new profile registration.
@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('my_account')
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'pictaroo/profile_registration.html', context_dict)


