from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from customer_register.models import Customer_User
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class Customer_Payments(TemplateView):
    template_name = 'customer_payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['post_from_url'] = self.request.build_absolute_uri()
        return context

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def charge(request):
    if request.method == 'POST':
        template_name = 'charge.html'

        # Create a customer in Stripe
        customer = stripe.Customer.create(
            email=request.user.email

        )

        # Create a product
        product = stripe.Product.create(
            name='Nova One Software Monthly Subscription',
            type='service',
        )

        #create a plan from the product

        # Try to charge customer and catch errors
        try:
            charge = stripe.Charge.create(
                amount=500,
                currency='usd',
                description='Nova One Software Monthly Subscription',
                source=request.POST['stripeToken']
            )
        except stripe.error.CardError as e:
            # Problem with the card
            print(e)
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            print(e)
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe API
            print(e)
        except stripe.error.AuthenticationError as e:
            # Authentication Error: Authentication with Stripe API failed (maybe you changed API keys recently)
            print(e)
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            print(e)
        except stripe.error.StripeError as e:
            # Stripe Error
            print(e)
        else:
            # Success
            # Update 'is_paying' attribute to True for the current user
            customer, created = Customer_User.objects.get_or_create(user=request.user)
            user = User.objects.get(pk=request.user.pk)
            user.customer_user.is_paying = True
            user.save()

        return render(request, template_name)
    else:
        return redirect('/customer-payments')
