from django import forms
from django.contrib.auth.forms import UserCreationForm

from ckeditor.widgets import CKEditorWidget

from .models import *

class ModuloAdminForm(forms.ModelForm):

    contenido = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Modulo
        fields = ['curso', 'number', 'nombre', 'descripcion', 'imagen', 'contenido']


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(label='Email', required=True)
    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(label='Nombre', required=False)
    last_name = forms.CharField(label='Apellido', required=False)

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user

class ExtraUserForm(forms.ModelForm):

    class Meta:
        model = ExtraUser
        fields = ['rol'] # 'imagen', 'bio', 

class UserUpdateForm(forms.ModelForm):

    # email = forms.EmailField(label='Email', required=True)
    # username = forms.CharField(max_length=100, required=True)
    # first_name = forms.CharField(label='Nombre', required=False)
    # last_name = forms.CharField(label='Apellido', required=False)
    imagen = forms.ImageField(label='Foto de Perfil', required=False)
    bio = forms.CharField(label='Biografía', required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name'] # , 'rol'

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        extra_user = ExtraUser.objects.get(user=user)
        extra_user.imagen = self.cleaned_data['imagen']
        extra_user.bio = self.cleaned_data['bio']
        # extra_user.rol = self.cleaned_data['rol']

        if commit:
            user.save()
            extra_user.save()

        return user

class CreateMensajeForm(forms.Form):
    
    destinatario = forms.EmailField(label='Email', required=True, widget=forms.Select(choices=[('', 'Seleccione un destinatario')] + [(user.email, user.email) for user in User.objects.all()]))
    # email = forms.EmailField(label='Email', required=True)
    mensaje = forms.CharField(label='Mensaje', required=True, widget=forms.Textarea)

    # def save(self, commit=True):
    #     mensaje = Mensaje(
    #         nombre=self.cleaned_data['nombre'],
    #         email=self.cleaned_data['email'],
    #         mensaje=self.cleaned_data['mensaje']
    #     )
    #     if commit:
    #         mensaje.save()
    #     return mensaje