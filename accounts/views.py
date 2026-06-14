from django.shortcuts import (
    render,
    redirect,
)
from django.contrib.auth import (
    login,
    logout,
    authenticate
)
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import (
    login_required
)
from .forms import (RegisterForm, LoginForm)
from django.views.decorators.http import require_POST
from django.contrib import messages


def staff_login(request):

    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.exists():
            return redirect("dashboard_router")
       # return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if not user.groups.exists() and not user.is_superuser:
                return redirect("staff_login")

            login(request,user)
            return redirect("dashboard_router")
        
        messages.error(request, "Invalid Username or Password")
        
    return render(request, "auth/staff_login.html")

@require_POST
def staff_logout(request):
    logout(request)
    return redirect("staff_login")


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect_user(user)
        
    else:

        form = RegisterForm()

    return  render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    authentication_form = LoginForm

    def form_valid(self, form):
        user = form.get_user()

        login(self.request, user)
        return redirect_user(user)
    


def redirect_user(user):

    if user.is_superuser:
        return redirect('owner_dashboard')

    if user.groups.filter(name='Manager').exists():
        return redirect ('manager_dashboard')
    
    elif user.groups.filter(name='Chef').exists():
        return redirect('chef_dashboard')
    
    elif user.groups.filter(name='Rider').exists():
        return redirect('rider_dashboard')
    
    elif user.groups.filter(name='Cashier').exists():
        return redirect('cashier_dashboard')
    
    elif user.groups.filter(name='Waiter').exists():
        return redirect('waiter_dashboard')

    
    return redirect ('home')