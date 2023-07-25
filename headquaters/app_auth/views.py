from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

class Connect(View):
    template_name = "app_auth/connect.html"
    title = "Connexion"
    def get(self, request):
        return render(request, self.template_name, {
            'title':self.title
        })
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None :
            login(request, user)
            if user.status == 'admin':
                return redirect('create_center')
        else:
            messages.error(request, "Informations incorrectes")
            return redirect('connect')
        
        print(email)
        print(password)
        return redirect('connect')
       

class Disconnect(View):
    def get(self, request):
        logout(request)
        return redirect('connect')