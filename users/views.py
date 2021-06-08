from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm
from django.contrib.auth import logout

# Sign Up View
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


def logoutPage(request):
	logout(request)
	return redirect('login')