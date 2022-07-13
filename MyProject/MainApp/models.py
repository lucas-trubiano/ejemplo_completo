from django.db import models

from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

class User(AbstractUser):

    email = models.EmailField('Email', unique=True)
    username = models.CharField('Nombre de Usuario', max_length=100, unique=True)

    first_name = models.CharField('Nombre', max_length=30, blank=True, null=True)
    last_name = models.CharField('Apellido', max_length=30, blank=True, null=True)

    is_active = models.BooleanField('Activo', default=True)
    # is_staff = models.BooleanField('Es Staff', default=False)
    # is_superuser = models.BooleanField('Es Superuser', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

# Create your models here.

class ExtraUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    imagen = models.ImageField(upload_to='profile_pics', blank=True, null=True, default='profile_pics/undraw_profile.svg')
    
    bio = models.TextField(max_length=500, blank=True)

    ROLES = (
        ('admin', 'Administrador'),
        ('user', 'Usuario'),
        ('guest', 'Invitado'),
        ('teacher', 'Profesor'),
        ('student', 'Alumno'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='student')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Categoria(models.Model):

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500, blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Curso(models.Model):

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    nombre = models.CharField('Nombre del Curso', max_length=50)
    descripcion = models.CharField('Descripción', max_length=200, blank=True, null=True)
    imagen = models.ImageField('Imagen', upload_to='cursos/', blank=True, null=True)
    precio = models.IntegerField('Precio', blank=True, null=True)
    # duracion = models.IntegerField('Duración [horas]', blank=True, null=True)

    profesor = models.ManyToManyField(User, related_name='profesor_curso', blank=True)

    active = models.BooleanField('Activo', default=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Modulo(models.Model):

    curso = models.ManyToManyField(Curso)

    number = models.IntegerField('Número')
    nombre = models.CharField('Nombre', max_length=50)
    descripcion = models.CharField('Descripción',max_length=200, blank=True, null=True)
    imagen = models.ImageField(upload_to='modulos/', blank=True, null=True)
    
    contenido = RichTextField('Contenido', blank=True, null=True) # ckeditor

    active = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Inscripcion(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Mensaje(models.Model):

    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remitente')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destinatario')

    mensaje = models.TextField(max_length=500, blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mensaje