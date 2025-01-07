from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import SignupForm 

# Create your views here.
def logout_view (request):                        #Kdybych pouzil logout kolidovalo by to s internim logout
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'agent/logout.html', {})

# Changes for forms
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/agent/login/')
    else:
        form = SignupForm()
    return render(request, 'agent/signup.html', {
        'form': form    
    })