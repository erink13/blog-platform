from django import forms

#inherit base form class
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) #input type as text html, and 25 length is validation
    email = forms.EmailField() #validation is done here as it is an email field
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea) #we set the widget here to override the default one
