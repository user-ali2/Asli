from django.shortcuts import (
    render,
    redirect,
)
from django.contrib.auth import (
    login,
    logout,
)
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import (
    login_required
)
from .forms import (RegisterForm, LoginForm)



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

    if user.groups.filter(name='Owner').exists():
        return redirect ('owner_dashboard')
    
    elif user.groups.filter(name='Management').exists():
        return redirect('management_dashboard')
    
    elif user.groups.filter(name='Staff').exists():
        return redirect('staff_dashboard')
    
    return redirect ('home')