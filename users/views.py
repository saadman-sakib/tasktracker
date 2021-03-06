from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin

# Sign Up View
class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'
    success_message = 'User Created!!!'
    


def logoutPage(request):
	logout(request)
	return redirect('login')