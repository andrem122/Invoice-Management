from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Tenant
from property.models import Company
from customer_register.models import Customer_User
from .forms import TenantFormCreate, TenantMassMessage
from django.views import View
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from twilio.rest import Client

def dispatch(class_name, class_instance, request, *args, **kwargs):
    # Check if there is a GET variable if not redirect to the home page
    try:
        company_id = int(request.GET.get('c', None))
    except ValueError:
        # Customer id was empty in GET variable
        raise Http404('Company not found!')
    except TypeError:
        # No GET variables attached to url
        raise Http404('Invalid url!')

    # Get the company
    company = None
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        # Company id was in GET variable but NOT found in database
        raise Http404('Company not found!')

    customer_id = company.customer_user.id
    if not request.user.is_superuser: # Will raise 'User object has no customer_user object if superuser'
        if request.user.is_authenticated and request.user.customer_user.id != customer_id:
            # Do not allow the customer_user (if they are logged in) to make appointments for other customers calendars
            raise PermissionDenied('Request denied!')

    return super(class_name, class_instance).dispatch(request, args, kwargs)

class TenantListView(LoginRequiredMixin, ListView):
    """Shows users a list of tenants"""
    paginate_by = 25

    def get_queryset(self):
        # Filter objects by user's companies
        company_id = int(self.request.GET.get('c', None))
        company = Company.objects.get(pk=company_id)
        return Tenant.objects.filter(
            company=company,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fields
        context['fields'] = ('Name', 'Phone Number', 'Email', 'Lease Begin', 'Lease End')
        context['customer_user'] = self.request.user.customer_user

        # Company object
        company_id = int(self.request.GET.get('c', None))
        company = Company.objects.get(pk=company_id)

        context['tenant_mass_message_form'] = TenantMassMessage()
        context['company'] = company

        return context

    def dispatch(self, request, *args, **kwargs):
        return dispatch(TenantListView, self, request, args, kwargs)

class ProcessSendMassMessageForm(View):
    # Handle the submission of the send mass message form
    success_message = 'Message sent successfully!'
    def post(self, request, *args, **kwargs):
        send_text_message = request.POST.get('send_text_message', None)
        message = request.POST.get('message', None)
        company_id = request.POST.get('company_id', None)

        # Get ALL tenants belonging to the company
        company = Company.objects.get(pk=int(company_id))
        tenants = Tenant.objects.filter(company=company)

        if send_text_message == 'True':
            # Send text message to ALL tenants
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            for tenant in tenants:
                client.messages.create(
                    body=message,
                    to=tenant.phone_number.as_e164,
                    from_=settings.TWILIO_NUMBER,
                )
        else:
            # Send email to tenants
            pass

        return HttpResponse('/tenants')


class TenantCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Allows user to add tenants"""

    model = Tenant
    form_class = TenantFormCreate
    template_name = 'tenants/add_tenant_form.html'
    success_message = 'Tenant successfully added.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request # Pass request object to form when it is initialized
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_user'] = self.request.user.customer_user
        return context

    def form_valid(self, form):
        # Set company for tenant based on the GET parameters in the url
        company_id = self.request.GET.get('c', None)
        company = Company.objects.get(id=int(company_id))

        tenant = form.save(commit=False) # Call form.save(commit=False) to create an object 'in memory' and not in the database
        tenant.company = company
        tenant.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        return dispatch(TenantCreateView, self, request, args, kwargs)

class TenantDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        # Handle POST requests to this view
        if 'object_id' in request.POST:
            tenant_id = int(self.request.POST.get('object_id'))
            tenant = Tenant.objects.get(pk=tenant_id)

            # Get updated company disabled_datetime objects and send as a string to the ajax success function
            tenants = Tenant.objects.filter(company=tenant.company)
            context = {
                'object_list': tenants,
                'fields': ('Name', 'Phone Number', 'Email', 'Lease Begin', 'Lease End'),
                'csrf_token': request.POST.get('csrfmiddlewaretoken')
            }

            # Delete the selected object
            tenant.delete()
            html_response = ''
            if not tenants.exists():
                html_response = '<p style="text-align: center;">There are currently no tenants.</p>'
            else:
                html_response = render_to_string('tenants/tenant_list_ajax_results.html', context)

            return HttpResponse(html_response)
        else:
            return JsonResponse({'error': 'Invalid post request'}, status=400)
