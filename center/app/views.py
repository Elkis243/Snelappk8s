from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout
from .models import *
from django.contrib import messages
from .producer import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import random
import string

class Create_subscribers(View):
    template_name = "app/create_subscribers.html"
    title = "Abonné"
    def get(self, request):
        return render(request, self.template_name, {
            'title':self.title
        })
    
    def post(self, request):
        random_number = ''.join(random.choices(string.digits, k=5))
        code_subscriber = f"{random_number}"
        name = request.POST.get('name').strip()
        last_name = request.POST.get('last_name').strip()
        first_name = request.POST.get('first_name').strip()
        address = request.POST.get('address').strip()
        type_subscriber = request.POST.get('type_subscriber').strip()
        agent = Agent.objects.get(user__id = request.user.id)
        center = agent.center
        if Subscriber.objects.filter(address=address).exists():
            messages.error(request, "L'enregistrement existe déjà !")
            return redirect('create_subscribers')
        else:
            subscriber = Subscriber(
                code_subscriber=code_subscriber,
                name=name,
                last_name=last_name,
                first_name=first_name,
                address=address,
                type_subscriber=type_subscriber,
                center=center
            )
            subscriber.save()
            messages.success(request, "L'enregistrement réussi")
            message =f"code_subscriber: {code_subscriber}, name: {name}, last_name: {last_name}, first_name: {first_name}, address: {address}, type_subscriber: {type_subscriber}, name_center: {center.name_center}"
            publish_message('subscribers', message)
            return redirect('create_subscribers')
        
class Read_subscribers(View):
    template_name = "app/read_subscribers.html"
    title = "Liste abonnés"
    def get(self, request):
        agent = Agent.objects.get(user__id = request.user.id)
        center = agent.center
        q = request.GET.get('q')
        if q:
            subscriber = Subscriber.objects.filter(center=center, name__contains=q)
        else:
            subscriber = Subscriber.objects.filter(center=center)
        return render(request, self.template_name, {
            'title':self.title,
            'subscribers':subscriber
        })
        

class Paiement(View):
    template_name = "app/paiement.html"
    title = "Paiement"
    def get(self, request):
        agent = Agent.objects.get(user__id = request.user.id)
        center = agent.center
        q = request.GET.get('q')
        if q:
            invoices = Invoice.objects.filter(invoice_code__contains=q, souscriber__center=center) | Invoice.objects.filter(souscriber__name__contains=q) 
        else:
            invoices = Invoice.objects.filter(souscriber__center=center)
        return render(request, self.template_name, {
            'title':self.title,
            'invoices':invoices
        })

class Update_invoice(View):
    def get(self, request, id_invoice):
        invoice = get_object_or_404(Invoice, id=id_invoice)
        invoice.status = 'Payée'
        invoice.save()
        message =f"invoice: {invoice}"
        publish_message('paiement', message)
        return redirect('paiement')
    
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
    
class Disconnect(View):
    def get(self, request):
        logout(request)
        return redirect('connect')