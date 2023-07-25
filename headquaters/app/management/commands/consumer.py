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
        channel.basic_consume(queue='subscribers', on_message_callback=self.get_data_subscriber, auto_ack=True)
        channel.basic_consume(queue='paiement', on_message_callback=self.get_data_paiement, auto_ack=True)
        self.stdout.write(
                self.style.SUCCESS("Started Consuming....")
            )
        channel.start_consuming()
        connection.close()

    def get_data_subscriber(self, ch, method, properties, body):
        data = body.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':') 
            dict_data[key.strip()] = value.strip()
        code_subscriber = dict_data['code_subscriber']
        name = dict_data['name']
        last_name = dict_data['last_name']
        first_name = dict_data['first_name']
        address = dict_data['address']
        type_subscriber = dict_data['type_subscriber']
        name_center = dict_data['name_center']
        get_center = Center.objects.get(name_center=name_center)
        subscriber = Subscriber(
            code_subscriber=code_subscriber,
            name = name,
            last_name = last_name,
            first_name = first_name,
            address = address,
            type_subscriber = type_subscriber,
            center = get_center
        )
        subscriber.save()
        print("message received successfully")
        
    def get_data_paiement(self, ch, method, properties, body):
        data = body.decode('utf-8')
        substrings = data.split(',')
        dict_data = {}
        for item in substrings:
            key, value = item.split(':') 
            dict_data[key.strip()] = value.strip() 
        invoice = dict_data['invoice']
        invoice_id = Invoice.objects.get(invoice_code=invoice)
        invoice_id.status= 'Payée'
        invoice_id.save()
        print("message received successfully")