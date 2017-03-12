from django import forms
from pictaroo.models import Image, Category, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length =128,
                           help_text="Please enter the category name.")
    view = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput, required=False)

    #An inline class to provide additional information on the form
    class Meta:
        #provide an association between the ModelForm andn a model
        model = Category
        fields = ('name',)

class ImageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the Image.")
    url= forms.URLField(max_length=200,
                        help_text="Please enter the URL of the image.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    #This method is called upon before saving form data to a new model instance and thus
    #provides us with a logical place to insert code which can verify and even fix any form data the user inputs
    def clean(self):
        cleaned_data= self.cleaned_data
        url = cleaned_data.get('url')

        #if url is not empty and doesnt start with http://
        #then prepend 'http://'
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url']=url

            return cleaned_data


    class Meta:
            #Provide an association between the ModelForm and a model
            model = Image

            #what fields do we want to include in our form?
            #this way we dont need every field in the model present
            #some fields may allow NULL values, so we may not want to include them
            #Here, we are hiding the foreign key
            #we can either exclude the category field from the form
            exclude = ('category',)
            # or specify the fields to include (i.e. not include the category field)
            #fields = ('title', 'url', views)


#Chapter 14 - Creating the User Profile Form class
class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)


    class Meta:
        model = UserProfile
        exclude = ('user',)