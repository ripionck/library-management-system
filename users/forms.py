from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .constants import GENDER_TYPE, PROFESSION_TYPE
from .models import UserProfile


# Form for user registration, inherits from UserCreationForm
class UserRegistrationForm(UserCreationForm):
    # Additional fields for user registration
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    profession = forms.ChoiceField(choices=PROFESSION_TYPE)
    phone_number = forms.CharField(max_length=12)
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 10}))

    class Meta:
        model = User
        # Fields to be included in the form
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email',
                 'birth_date', 'gender', 'profession', 'phone_number', 'address']

    def save(self, commit=True):
        # Save the user instance
        our_user = super().save(commit=False)
        if commit:
            our_user.save()
            # Retrieve additional data from the form
            gender = self.cleaned_data.get('gender')
            profession = self.cleaned_data.get('profession')
            birth_date = self.cleaned_data.get('birth_date')
            phone_number = self.cleaned_data.get('phone_number')
            address = self.cleaned_data.get('address')

            # Create User instance
            UserProfile.objects.create(
                user=our_user,
                gender=gender,
                birth_date=birth_date,
                profession=profession,
                phone_number=phone_number,
                address=address
            )
        return our_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields for styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

# Form for updating user information, inherits from forms.ModelForm

class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    profession = forms.ChoiceField(choices=PROFESSION_TYPE)
    phone_number = forms.CharField(max_length=12)
    balance = forms.DecimalField(max_digits=10, decimal_places=2, initial=0)
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields for styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
            
         # If the user instance exists, retrieve related UserBankAccount and UserAddress data
        if self.instance:
            try:
                user_profile = self.instance.profile
            except UserProfile.DoesNotExist:
                user_profile = None

            # Populate initial values for related fields if they exist
            if user_profile:
                self.fields['gender'].initial = user_profile.gender
                self.fields['profession'].initial = user_profile.profession
                self.fields['phone_number'].initial = user_profile.phone_number
                self.fields['balance'].initial = user_profile.balance
                self.fields['address'].initial = user_profile.address
                self.fields['birth_date'].initial = user_profile.birth_date


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            # Retrieve or create UserProfile instance
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            # Update fields based on form data
            user_profile.birth_date = self.cleaned_data['birth_date']
            user_profile.gender = self.cleaned_data['gender']
            user_profile.profession = self.cleaned_data['profession']
            user_profile.phone_number = self.cleaned_data['phone_number']
            user_profile.balance = self.cleaned_data['balance']
            user_profile.address = self.cleaned_data['address']

            user_profile.save()

        return user