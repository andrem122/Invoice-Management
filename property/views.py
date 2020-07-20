from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CompanyFormCreate, CompanyDisabledDatetimes
from django.urls import reverse_lazy
from .models import Company, Company_Disabled_Datetimes
from django.http import Http404, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.middleware.csrf import get_token

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


class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Powers a form to create a new company"""

    form_class = CompanyFormCreate
    template_name = 'property/add_company.html'
    success_message = 'Property successfully added!'
    success_url = reverse_lazy('appointments:list_appointments')

    def form_valid(self, form):
        # Associate the company added with the customer
        customer_user = self.request.user.customer_user
        company = form.save()
        company.customer_user = customer_user
        return super().form_valid(form)

class CompaniesListView(LoginRequiredMixin, ListView):
    """Shows users a list of companies"""
    paginate_by = 25

    def get_queryset(self):
        # Filter objects displayed by user
        return Company.objects.filter(
            customer_user=self.request.user.customer_user
        ).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_user = self.request.user.customer_user
        context['fields'] = ('Name', 'Address', 'City', 'State', 'Phone', 'Email') # fields to show in table header
        context['customer_user'] = customer_user
        return context

class CompanyDisabledDatetimesListView(LoginRequiredMixin, ListView):
    """Shows users a list of disabled datetimes"""
    paginate_by = 25

    def get_queryset(self):
        # Filter objects displayed by user
        company_id = int(self.request.GET.get('c', None))
        return Company_Disabled_Datetimes.objects.filter(
            company=company_id
        ).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company_id = int(self.request.GET.get('c', None))

        context['company_id'] = company_id
        context['fields'] = ('Disabled From', 'Disabled To', 'Created') # fields to show in table header
        return context

class CompanyDisabledDatetimesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Allows users to add additional disabled datetimes"""
    form_class = CompanyDisabledDatetimes
    template_name = 'property/add_company_disabled_datetimes.html'
    success_message = 'Disabled date and time successfully added!'

    def dispatch(self, request, *args, **kwargs):
        return dispatch(CompanyDisabledDatetimesCreateView, self, request, args, kwargs)

    def form_valid(self, form):
        company_id = int(self.request.GET.get('c', None))
        company = Company.objects.get(pk=company_id)

        company_disabled_datetimes = form.save()
        company_disabled_datetimes.company = company
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect user on successful form completion with correct url paramaters"""
        return reverse_lazy('property:add_company_disabled_datetimes') + '?c=' + self.request.GET.get('c')

class CompanyDisabledDatetimesDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Hello!</h2>')

    def post(self, request, *args, **kwargs):
        # Handle POST requests to this view
        print(request.POST)
        if 'company_disabled_datetime_id' in request.POST:
            company_disabled_datetime_id = int(self.request.POST.get('company_disabled_datetime_id'))
            company_disabled_datetime_object = Company_Disabled_Datetimes.objects.get(pk=company_disabled_datetime_id)

            # Get updated company disabled_datetime objects and send as a string to the ajax success function
            company_disabled_datetimes = Company_Disabled_Datetimes.objects.filter(company=company_disabled_datetime_object.company)
            context = {
                'object_list': company_disabled_datetimes,
                'fields': ('Disabled From', 'Disabled To', 'Created'),
                'csrf_token': request.POST.get('csrfmiddlewaretoken')
            }

            # Delete the selected object
            company_disabled_datetime_object.delete()
            html_response = ''
            if not company_disabled_datetimes.exists():
                html_response = '<p style="text-align: center;">There are currently no disabled dates and times.</p>'
            else:
                html_response = render_to_string('property/company_disabled_datetimes_list_ajax_results.html', context)

            return HttpResponse(html_response)
        else:
            return JsonResponse({'error': 'Invalid post request'}, status=400)
