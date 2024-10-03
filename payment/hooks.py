from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from  django.dispatch import receiver
from django.conf import settings
import time
from .models import Order


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    #Add 5 second pause for paypal to send IPN data
    time.sleep(5)
    #Grab the info  that paypal sends
    paypal_obj = sender
    #grab th invoice 
    my_Invoice = str(paypal_obj.invoice)

    # Match the paypal invoice to the order invoice
    #look up th order
    my_order = Order.objects.get(invoice=my_Invoice)

    #record the order was paid
    my_order.paid = True
    #save the order
    my_order.save()





    #print(paypal_obj)
    #print(f'amount paid {paypal_obj.mc_gross}')