from django import forms
class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    role = forms.CharField()

# class SystemForm(forms.Form):
#     system = forms.CharField()

class NodeForm(forms.Form):
    ip = forms.CharField()
    port = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()


class PathForm(forms.Form):
    path = forms.CharField()
