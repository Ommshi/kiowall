from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile




class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon'}), required=False)
    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse 1'}), required=False)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse 2'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stadt'}), required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bundesland'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postleitzahl'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Land'}), required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country',)

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1, new_password2']
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        # Passwort
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Passwort'
        })
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '''
            <ul class="form-text text-muted small">
                <li>Ihr Passwort darf nicht zu ähnlich zu Ihren persönlichen Informationen sein.</li>
                <li>Ihr Passwort muss mindestens 8 Zeichen lang sein.</li>
                <li>Ihr Passwort darf kein häufig verwendetes Passwort sein.</li>
                <li>Ihr Passwort darf nicht nur aus Zahlen bestehen.</li>
            </ul>
        '''

        # Passwort bestätigen
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Passwort bestätigen'
        })
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Geben Sie dasselbe Passwort wie zuvor ein, um es zu bestätigen.</small></span>'

class UpdateUserForm(UserChangeForm):
    #Hide password stuff
    password = None
    #Show these from blow only
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'E-Mail-Adresse'
        })
    )
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Vorname'
        })
    )
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nachname'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        # Benutzername
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Benutzername'
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Erforderlich. 150 Zeichen oder weniger. Nur Buchstaben, Ziffern und @/./+/-/_ sind erlaubt.</small></span>'



class SignUpForm(UserCreationForm):
    usable_password = None
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'E-Mail-Adresse'
        })
    )
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Vorname'
        })
    )
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nachname'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Benutzername
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Benutzername'
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Erforderlich. 150 Zeichen oder weniger. Nur Buchstaben, Ziffern und @/./+/-/_ sind erlaubt.</small></span>'

        # Passwort
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Passwort'
        })
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '''
            <ul class="form-text text-muted small">
                <li>Ihr Passwort darf nicht zu ähnlich zu Ihren persönlichen Informationen sein.</li>
                <li>Ihr Passwort muss mindestens 8 Zeichen lang sein.</li>
                <li>Ihr Passwort darf kein häufig verwendetes Passwort sein.</li>
                <li>Ihr Passwort darf nicht nur aus Zahlen bestehen.</li>
            </ul>
        '''
        

        # Passwort bestätigen
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Passwort bestätigen'
        })
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Geben Sie dasselbe Passwort wie zuvor ein, um es zu bestätigen.</small></span>'


