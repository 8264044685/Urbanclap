from django import forms
from account.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'user_type', 'password']

        def clean_user_type(self,*args,**kwargs):
            user_type = self.cleaned_data.get('user_type')
            if user_type == 'as_a':
                raise forms.ValidationError("Please select valid usertype")
            return  user_type

        def clean_username(self,*args,**kwargs):
            username = self.cleaned_data.get('username')

            if username == 'jaydeep':
                raise forms.ValidationError("please enter another name")

        def clean(self, *args, **kwargs):
            data = self.cleaned_data
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            user_type = data.get('user_type')
            return super().clean(*args,**kwargs)

