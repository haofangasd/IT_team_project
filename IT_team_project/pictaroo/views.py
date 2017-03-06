from django.shortcuts import render
from django.http import HttpResponse
from pictaroo.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# Create your views here.

#Main index view page
def index(request):

    # if the request is a HTTP post, try to pull out the relevant information
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # User django machinery to attempt to see if the username/passwprd
        # combination is valid - a user  object is returned of it is
        user = authenticate(username=username, password=password)

        # if we have a User object, the detais are correct
        # if none. no user with matching credentials was found
        if user:
            # is the account active? it could have been disabled
            if user.is_active:
                # if the account is valid and active, we can log the user in
                # we'll send the user back to the homepage
                login(request, user)
                return HttpResponseRedirect(reverse('my_account'))
            else:
                # an inactive account was used - no logging in
                return HttpResponse("Your Rango Account is Disabled")
        else:
            # bad login details were provided, so we cant log the user in
            print("Invalid Login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details suppplied.")
            # the request is not a HTTP POST, so display the login form
            # this scenario would most likley be a HTTP GET
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object..
        return render (request, 'pictaroo/index.html', {})






#View to display the Registered User their account page
def my_account(request):
    return render(request, 'pictaroo/myAccount.html')

def register(request):
    #boolean value for telling the template
    #whether the registration was successful
    #set to false initially. Code changes value to
    #true when registration succeeds
    registered = False

    #if its a HTTP post, we're interested in processing form data
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

def my_comments(request):

    return render(request, 'pictaroo/myComments.html')


# View to display the registered user their favourite pictures shared by other users
def my_favourites(request):

    return render(request, 'pictaroo/myFavourites.html')


# view to store the registered user pictures they have uploaded.

def my_uploads(request):

    return render(request, 'pictaroo/myUploads.html')


