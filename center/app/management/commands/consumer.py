from django.core.management.base import BaseCommand
from app.models import *
import pika
import time
 
class Command(BaseCommand):
    help = 'Starts consuming messages from rabbitmq'
    def connect(self):
        while True:
            try:
                credentials = pika.PlainCredentials('guest', 'guest')
                connection  = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host='rabbitmq',
                        port=5672,
                        virtual_host='/',
                        credentials=credentials,
                        heartbeat=600,
                        blocked_connection_timeout=300
                    )
                )
                return connection
            except pika.exceptions.AMQPConnectionError:
                time.sleep(5)
                
    def handle(self, *args, **options): 
        connection = self.connect()
        channel = connection.channel()
        channel.basic_consume(queue='center', on_message_callback=self.get_data_center, auto_ack=True)
        channel.basic_consume(queue='agent', on_message_callback=self.get_data_agent, auto_ack=True)
        channel.basic_consume(queue='invoice', on_message_callback=self.get_data_invoice, auto_ack=True)
        self.stdout.write(
                self.style.SUCCESS("Started Consuming....")
            )
        channel.start_consuming()
        connection.close()
        
    def get_data_center(ch, method, properties, body, b):
        data = b.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':')
            dict_data[key.strip()] = value.strip() 
        name_center = dict_data['name_center']
        address_center = dict_data['address_center']
        center = Center(
            name_center=name_center,
            address_center=address_center
        )
        center.save()
        print("message received successfully")
        
    def get_data_agent(ch, method, properties, body, b):
        data = b.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':')
            dict_data[key.strip()] = value.strip()
        registration_number = dict_data['registration_number']
        username = dict_data['username']
        last_name = dict_data['last_name']
        first_name = dict_data['first_name']
        email = dict_data['email']
        password = dict_data['password']
        name_center = dict_data['name_center']
        get_center = Center.objects.get(name_center=name_center)
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, status='agent')
        agent = Agent(
            user=user,
            registration_number=registration_number,
            center=get_center
        )
        agent.save()
        print("message received successfully")
        
    def get_data_invoice(ch, method, properties, body, b):
        data = b.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':')
            dict_data[key.strip()] = value.strip()
        invoice_code = dict_data['invoice_code']
        code_subscriber = dict_data['subscriber']
        souscriber_id = Subscriber.objects.get(code_subscriber=code_subscriber)
        month = dict_data['month']
        index_invoice = dict_data['index_invoice']
        consommation = dict_data['consommation']
        amount = dict_data['amount']
        invoice = Invoice(
            invoice_code=invoice_code,
            souscriber = souscriber_id,
            month=month,
            index_invoice=index_invoice,
            consommation=consommation,
            amount=amount
        )
        invoice.save()
        print("message received successfully")

        
