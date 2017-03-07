
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#Import the category model
from pictaroo.models import Category
from pictaroo.models import Page
from pictaroo.forms import CategoryForm
from pictaroo.forms import PageForm
from pictaroo.forms import UserForm, UserProfileForm
from datetime import datetime

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
    page_list = Page.objects.order_by('-views')[:5]

    context_dict={'categories':category_list,'pages':page_list}
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

        #Retrieve all of the associated pages
        #note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        #add our results list to the template context under name pages
        context_dict['pages'] = pages
        #we also add the category object from
        #the databse to the context dictionary
        #we'll use this in the template to verify that the category exist
        context_dict['category'] = category
    except Category.DoesNotExist:
        #we get here if we didnt find the specified category
        #dont do anything -
        #the template will display the 'no category message for us'
        context_dict['category']=None
        context_dict['pages']=None


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

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views= 0
                page.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render (request, 'pictaroo/add_page.html', context_dict)

def register(request):
    #boolean value for telling the template
    #whether the registration was successful
    #set to false initially. Code changes value to
    #true when registration succeeds
    registered = False

    #uf uts a HTTP post, we're interested in processing form data
    if request.method == 'POST':
        #Attempt to grab infomration from the raw form information
        #note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #If the two forms are valid

        if user_form.is_valid() and profile_form.is_valid():
                #save the users form data to the data
                user = user_form.save()

                #Now sort out the user profile instance
                #since we need to set the user attribute ourselves
                #we set commit=False. This delays saving the model
                #until we're ready to avoid integrity problems
                profile = profile_form.save(commit=False)
                profile.user = user

                #did the user provide a profile picture?
                #if so, we need to get it from the input form and
                #put it in the UserProfile model
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

                #now we save the user profile model instance
                profile.save()

                #Update our variable to indicate that the template
                #regustration was successful
                registered = True;
        else:
                #Invalid form or forms - mistkaes or something else?
                #print problems to the terminal
                print(user_form.errors, profile_form.errors)
    else:
            #Not a HTTP POST, so we render our form using two modelForm instances
            #these forms will be blank for user input
            user_form = UserForm()
            profile_form = UserProfileForm()

        #Render the template depending on the context
    return render(request, 'pictaroo/register.html', {'user_form': user_form,
                                                       'profile_form': profile_form,
                                                       'registered': registered })

def user_login(request):
    #if the request is a HTTP post, try to pull out the relevant information
            if request.method =='POST':
                #gather the username and password provided by the user
                #this information is obtained from the login form
                #we use request.POST.get('<variable>') as opposed
                #to request.POST['<variable>'], because the
                #request.POST.get('<variable>') returns None if the
                #value does not exist, while request.POST['<variable>']
                #will raise a keyError exception
                username = request.POST.get('username')
                password = request.POST.get('password')

                #User django machinery to attempt to see if the username/passwprd
                #combination is valid - a user  object is returned of it is
                user = authenticate(username=username, password=password)

                #if we have a User object, the detais are correct
                #if none. no user with matching credentials was found

                if user:
                        #is the account active? it could have been disabled
                        if user.is_active:
                            #if the account is valid and active, we can log the user in
                            #we'll send the user back to the homepage
                            login(request, user)
                            return HttpResponseRedirect(reverse('index'))
                        else:
                            #an inactive account was used - no logging in
                            return HttpResponse("Your Pictaroo Account is Disabled")
                else:
                    #bad login details were provided, so we cant log the user in
                    print("Invalid Login details: {0}, {1}".format(username,password))
                    return HttpResponse("Invalid login details suppplied.")
                #the request is not a HTTP POST, so display the login form
                #this scenario would most likley be a HTTP GET
            else:
                #No context variables to pass to the template system, hence the
                #blank dictionary object..
                return render(request, 'pictaroo/login.html', {})

@login_required
def restricted(request):
    return render(request, 'pictaroo/restricted.html')

#Use the login_required() decorator to ensure only those loggin can acces the view
@login_required
def user_logout(request):
    #since we know the user is logged in, we can now just log them out
    logout(request)
    #take the user back to the homepage
    return HttpResponseRedirect(reverse('index'))