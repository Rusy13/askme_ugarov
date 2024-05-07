from django import forms

class QuestionForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=1000)
    tags = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))




class LoginForm(forms.Form):
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 3}), label='')




class SettingsForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(label='NickName', widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(label='Upload avatar', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))



class SignupForm(forms.Form):
    login = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(label='NickName', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(label='Upload avatar', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
