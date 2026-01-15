from django.shortcuts import render
from django.shortcuts import render, redirect
from userRegister.form import RegisterUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.
# registration ======================================================================>>>>
def Register(request):
    if request.method == "POST":
        regForm = RegisterUser(request.POST)
        if regForm.is_valid():
            new_user = regForm.save(commit=False)
            new_user.set_password(regForm.cleaned_data.get('password'))
            new_user.save()
            return redirect('userRegister:login')
    else:
        form = RegisterUser()
        return render(request, 'registerTemplate/register.html', {'form': form})
    
def logoutview(request):
    logout(request)
    return redirect('userRegister:login')
# reset password ==============================================================================
