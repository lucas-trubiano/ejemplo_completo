from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import *
from .models import *

# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# from django.contrib.admin.views.decorators import staff_member_required

page_title = "Academia IT"

base_context = {
    'page_title': page_title,
}

# --- Landing Page ---

def home(request):
    base_context.update({"active":"home"})
    return render(request, 'landing/home.html', base_context)

def about(request):
    base_context.update({"active":"about"})
    return render(request, 'landing/about.html', base_context)

def cursos(request):

    categories = Categoria.objects.all()

    cursos = Curso.objects.all()

    base_context.update({"cursos":cursos})
    base_context.update({"active":"cursos"})
    base_context.update({"filtered":"all"})
    base_context.update({"categories":categories})
    return render(request, 'landing/cursos.html', base_context)

def cursos_categoria(request, id_categoria):

    categories = Categoria.objects.all()

    cursos = Curso.objects.filter(categoria=id_categoria)

    base_context.update({"cursos":cursos})
    base_context.update({"active":"cursos"})
    base_context.update({"filtered":int(id_categoria)})
    base_context.update({"categories":categories})
    return render(request, 'landing/cursos.html', base_context)

# --- Dashboard ---

@login_required
def dashboard(request):

    user = request.user

    mensajes = Mensaje.objects.filter(destinatario=user)

    # if user.groups.filter(name="teacher").exists():
    #     cursos = Curso.objects.filter(profesor=user)
    #     titulo_cursos = "Mis Cursos"

    # elif user.groups.filter(name="student").exists():
    #     cursos = [insc.curso for insc in Inscripcion.objects.filter(user=user)]
    #     titulo_cursos = "Mis Cursos"

    # elif user.groups.filter(name="admin").exists():
    #     cursos = Curso.objects.all()
    #     titulo_cursos = "Cursos"

    # else:
    #     cursos = [] # Curso.objects.all()
    #     titulo_cursos = f"No hay cursos para este rol: {ExtraUser.objects.get(user=user).rol}"

    # base_context.update({"cursos":cursos})
    # base_context.update({"titulo_cursos":titulo_cursos})
    base_context.update({"active":"dashboard"})
    base_context.update({"mensajes":mensajes})
    return render(request, 'dashboard/dashboard.html', base_context)

@login_required
def dashboard_cursos(request):

    user = request.user

    if user.groups.filter(name="teacher").exists():
        cursos = Curso.objects.filter(profesor=user)
        titulo_cursos = "Mis Cursos"

    elif user.groups.filter(name="student").exists():
        cursos = [insc.curso for insc in Inscripcion.objects.filter(user=user)]
        titulo_cursos = "Mis Cursos"

    elif user.groups.filter(name="admin").exists():
        cursos = Curso.objects.all()
        titulo_cursos = "Cursos"

    else:
        cursos = [] # Curso.objects.all()
        titulo_cursos = f"No hay cursos para este rol: {ExtraUser.objects.get(user=user).rol}"

    base_context.update({"cursos":cursos})
    base_context.update({"titulo_cursos":titulo_cursos})
    base_context.update({"active":"dashboard_cursos"})
    return render(request, 'dashboard/cursos.html', base_context)

@login_required
def enviar_mensaje(request):
    if request.method == "POST":
        form = CreateMensajeForm(request.POST)
        if form.is_valid():
            info  = form.cleaned_data
            nuevo_mensaje = Mensaje(remitente=request.user,destinatario=User.objects.get(email=info["destinatario"]), mensaje = info["mensaje"])
            nuevo_mensaje.save()
            # form.save()
            messages.success(request, "Mensaje enviado!")
            return redirect("dashboard")
        else:
            messages.error(request, "Error al enviar el mensaje!")
            return redirect("dashboard")
    else:
        form = CreateMensajeForm()
        base_context.update({"form":form})
        return render(request,"dashboard/mensaje.html", base_context)

# --- Accounts ---

@login_required
def profile(request):

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if form.cleaned_data["imagen"] == None:
                form.cleaned_data["imagen"] = ExtraUser.objects.get(user=request.user).imagen
            form.save()
            messages.success(request, f"Su perfil ha sido actualizado.")
            return redirect("profile")

        messages.error(request, f"No se pudo actualizar su perfil.")
        return redirect("profile")
    

    user = request.user
    email = user.email
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    try:
        extra_user = ExtraUser.objects.get(user=user)

    except:
        # Crear el extra user
        extra_user = ExtraUser(user=user, rol="guest", imagen="", bio="")
        extra_user.save()
        
    rol = extra_user.rol
    imagen = extra_user.imagen
    bio = extra_user.bio

    form = UserUpdateForm(initial={
        'email': email,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'imagen': imagen,
        'bio': bio
    }) # , 'rol': extra_user.rol

    base_context.update({"form":form})
    return render(request, 'dashboard/profile.html', base_context)

def login_request(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            # print("FORM VALID")
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido {user.first_name}. Cómo estás?")
                return redirect("dashboard")
            
            else:
                messages.error(request, "El email ingresado no existe!")
                return redirect("login")
                # base_context.update({"form":form})
                # return render(request,"dashboard/login.html", base_context)

        else:
            # print("FORM INVALID")
            messages.error(request, "Email o contraseña incorrectos!")
            return redirect("login")
            # base_context.update({"form":form})
            # return render(request,"dashboard/login.html", base_context)
    
    form = AuthenticationForm()
    base_context.update({"form":form})

    return render(request,"dashboard/login.html", base_context)

def register_request(request):

    if request.method == "POST":
        
        # form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)
        rol = request.POST.get('rol')

        if form.is_valid() and rol in [u[0] for u in ExtraUser.ROLES]:
            
            # username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1') # es la primer contraseña, no la confirmacion
            # first_name = form.cleaned_data.get('first_name')
            # last_name = form.cleaned_data.get('last_name')

            user = form.save()
            
            try:
                group = Group.objects.get(name=rol)
                user.groups.add(group)
            except:
                pass # no se pudo agregar al grupo

            # iniciamos la sesion
            user_auth = authenticate(email=email, password=password)

            # print("Usuario authenticado")
            extra_user = ExtraUser(user=user_auth, rol=rol)
            extra_user.save()

            if user_auth is not None:
                login(request, user_auth)
                messages.success(request, f"Usuario creado con éxito!")
                return redirect("dashboard")
            else:
                return redirect("login")

        base_context.update({"form":form})
        # extra_form = ExtraUserForm(initial={'rol': rol})
        # base_context.update({"extra_form":extra_form})
        
        # for message in form.error_messages:
        #     messages.error(request, form.error_messages[message])
        password1 = form.data['password1']
        password2 = form.data['password2']
        # email = form.data['email']
        # username = form.data['username']

        for msg in form.errors.as_data():
            if msg == 'email':
                messages.error(request, f"El email es invalido o ya existe.")
            if msg == 'username':
                messages.error(request, f"El nombre de usuario es invalido o ya existe.")
            if msg == 'password2' and password1 == password2:
                messages.error(request, f"La contraseña elegida no cumple los requisitos.")
            elif msg == 'password2' and password1 != password2:
                messages.error(request, f"Las contraseñas no coinciden.")

        return render(request,"dashboard/register.html", base_context)

    # form = UserCreationForm()
    # form = UserRegisterForm()
    # extra_form = ExtraUserForm()

    # base_context.update({"form":form})
    # base_context.update({"extra_form":extra_form})
    return render(request,"dashboard/register.html", base_context)

def logout_request(request):
    logout(request)
    return redirect("home")
