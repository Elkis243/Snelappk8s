from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import *
from django.contrib import messages
from .document import *
from .password_generator import generate_password
from django.core.mail import EmailMessage
from django.conf import settings
from .producer import publish_message
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
import string
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum

class Create_center(View):
    template_name = "app/create_center.html"
    title = "Centre"
    def get(self, request):
        return render(request, self.template_name, {'title':self.title})
    
    def post(self, request):
        name_center = request.POST.get('name_center').strip()
        address_center = request.POST.get('address_center').strip()
        if Center.objects.filter(name_center=name_center).exists():
            messages.error(request, "L'enregistrement existe déjà !")
            return redirect('create_center')
        else:
            center = Center(
                name_center=name_center,
                address_center=address_center
            )
            center.save()
            messages.success(request, "L'enregistrement réussi !")
            message = f"name_center: {name_center}, address_center: {address_center}"
            publish_message('center', message)
            return redirect('create_center')

class Read_center(View):
    template_name = "app/read_center.html"
    title = "Liste centres"
    def get(self, request):
        q = request.GET.get('q')
        if q:
            centers = Center_document.search().query("multi_match", query=q, fields=["name_center", "address_center"], fuzziness="AUTO")
        else:
            centers = Center.objects.all()
        return render(request, self.template_name, {
            'title':self.title,
            'centers':centers,
            'count':Center.objects.all().count()
        })
        
class Create_agent(View):
    template_name = "app/create_agent.html"
    title = "Agent"
    def get(self, request):
        centers = Center.objects.all()
        return render(request, self.template_name, {
                'title':self.title,
                'centers':centers
            })
    
    def post(self, request):
        random_number= ''.join(random.choices(string.digits, k=5))
        registration_number = f"AG-SNEL-{random_number}"
        center_id = int(request.POST.get('name_center'))
        get_center = Center.objects.get(id=center_id)
        name = request.POST.get('name').strip()
        last_name = request.POST.get('last_name').strip()
        first_name = request.POST.get('first_name').strip()
        email = request.POST.get('email').strip()
        password=generate_password()
        if User.objects.filter(email=email).exists():
            messages.error(request, "L'enregisrement existe déjà !")
            return redirect('create_agent')
        else:
            user = User.objects.create_user(username=name, first_name=first_name, last_name=last_name, email=email, password=password, status='agent')
            agent = Agent(
                user=user,
                registration_number=registration_number,
                center=get_center
            )
            agent.save()
            messages.success(request, "L'enregistrement réussi")
            name_center = get_center.name_center
            message =f"registration_number: {registration_number}, username: {name}, last_name: {last_name}, first_name: {first_name}, email: {email}, password: {password}, name_center: {name_center}"
            publish_message('agent', message)
            subject = "Bienvenue dans la plateforme Snel app : vos identifiants de connexion."
            message = f"Bonjour {name},\n\nNous sommes ravis de vous informer que vous avez été ajouté avec succès dans la plateforme Snel app. Votre numero de matricule est : {registration_number} \nVous pouvez maintenant vous connecter à notre plateforme en utilisant les identifiants ci-dessous:\n\nEmail : {email}\nMot de passe : {password} \n\nBienvenue parmi nous !"
            email_message = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
            email_message.send()
            return redirect('create_agent')
        
class Read_agent(View):
    template_name = "app/read_agent.html"
    title = "Liste agents"
    def get(self, request):
        q = request.GET.get('q')
        if q:
            agents = Agent.objects.filter(user__username__contains=q) | Agent.objects.filter(registration_number__contains=q) 
        else:
            agents = Agent.objects.all()
        return render(request, self.template_name, {
            'title':self.title,
            'agents':agents,
            'count':Agent.objects.all().count()
        })

class Read_subscribers(View):
    template_name = "app/read_subscribers.html"
    title = "Liste abonnés"
    def get(self, request):
        q = request.GET.get('q')
        if q:
            subscribers =  Subscriber.objects.filter(name__contains=q)
        else:
            subscribers =  Subscriber.objects.all()
        return render(request, self.template_name, {
            'title':self.title,
            'subscribers': subscribers,
            'count': Subscriber.objects.all().count()
        })
    
class Create_invoice(View):
    template_name = "app/create_invoice.html"
    title = "Facture"
    def get(self, request):
        souscrebers = Subscriber.objects.all()
        return render(request, self.template_name, {'title':self.title,'souscrebers':souscrebers})
    
    
    def post(self, request):
        random_number = ''.join(random.choices(string.digits, k=5))
        invoice_code = f"{random_number}"
        subscriber = int(request.POST.get('subscriber'))
        subscriber_id = Subscriber.objects.get(id=subscriber)
        month = request.POST.get('month').strip()
        index_invoice = int(request.POST.get('index_invoice'))
        consommation = int(request.POST.get('consommation'))
        amount = index_invoice * consommation
        invoice = Invoice(
            invoice_code=invoice_code, 
            subscriber=subscriber_id, 
            month=month, 
            index_invoice=index_invoice, 
            consommation=consommation, 
            amount=amount)
        invoice.save()
        messages.success(request, "L'enregistrement réussi")
        message =f"invoice_code: {invoice_code}, subscriber: {subscriber_id.code_subscriber}, month: {month}, index_invoice: {index_invoice}, consommation: {consommation}, amount: {amount}"
        publish_message('invoice', message)
        return redirect('create_invoice') 
    
class Paiement(View):
    template_name = "app/paiement.html"
    title = "Paiement"
    def get(self, request): 
        q = request.GET.get('q')
        if q:
            invoices = Invoice.objects.filter(subscriber__name__contains=q)
        else:
            invoices = Invoice.objects.all()
        return render(request, self.template_name, {
            'title':self.title,
            'invoices':invoices,
            'amount_paid': Invoice.objects.filter(status='Payée').aggregate(Sum('amount'))['amount__sum'],
            'unpiad_amount': Invoice.objects.filter(status='Impayée').count()
        })
    def post(self, request):
        return redirect('create_invoice') 
    
class Update_invoice(View):
    def get(self, request, id_invoice):
        invoice = get_object_or_404(Invoice, id=id_invoice)
        invoice.status = 'Payée'
        invoice.save()
        return redirect('read_invoice')
    
class Generate_invoice(View):
    def get(self, request, id_invoice):
        invoice = get_object_or_404(Invoice, id=id_invoice)
        template_path = "app/create_pdf.html"
        context = {
            'invoice':invoice
        }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="facture_client.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF( html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response