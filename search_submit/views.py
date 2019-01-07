from django.views.generic.base import View
from django.http import HttpResponse
from django.template import loader
from jobs.models import Job, Request_Payment
from jobs_admin.forms import Edit_Job
from expenses.models import Expenses
from django.db.models import Q
from django.shortcuts import redirect
from customer_register.customer import Customer
from payment_history.forms import Upload_Document_Form
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from send_data.forms import Send_Data
import operator
import functools
import re

class Search_Submit_View(View):
    template_name = 'search_submit/search_submit.html'

    def normalize_query(self, query_string,
        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
        normspace=re.compile(r'\s{2,}').sub):

        '''
        Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
        Example:
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
            ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
        '''
        if isinstance(query_string, str) == False:
            raise ValueError('Value must be a string')

        return [normspace(' ',(t[0] or t[1]).strip()) for t in findterms(query_string)]

    @method_decorator(user_passes_test(customer_and_staff_check, login_url='/accounts/login/'))
    def get(self, request):
        current_user = request.user
        template = loader.get_template(self.template_name)
        upload_document_form = Upload_Document_Form()
        send_data_form = Send_Data()
        edit_job_form = Edit_Job(user=current_user)

        customer = Customer(current_user)
        context = {
            'current_user': current_user,
            'upload_document_form': upload_document_form,
            'send_data_form': send_data_form,
            'edit_job_form': edit_job_form,
        }

        return HttpResponse(template.render(context, request))

    @method_decorator(user_passes_test(customer_and_staff_check, login_url='/accounts/login/'))
    def post(self, request):
        current_user = request.user
        template = loader.get_template(self.template_name)
        upload_document_form = Upload_Document_Form()
        edit_job_form = Edit_Job(user=current_user)

        current_user = request.user
        customer = Customer(current_user)
        context = {
            'current_user': current_user,
            'upload_document_form': upload_document_form,
            'edit_job_form': edit_job_form,
        }

        if request.method == 'POST':
            query = request.POST.get('search', None)
            queryset_jobs, queryset_payments = [], []
            if query != None:
                query_terms = self.normalize_query(query)
                #search jobs table
                queryset_jobs = functools.reduce(operator.__or__, (
                    Q(company__username__icontains=term) |
                    Q(house__address__icontains=term) |
                    Q(house__address__startswith=term) |
                    Q(house__address__endswith=term) |
                    Q(start_amount__startswith=term)
                    for term in query_terms)
                )

                #search payments table
                queryset_payments = functools.reduce(operator.__or__, (
                    Q(job__company__username__icontains=term) |
                    Q(job__house__address__icontains=term) |
                    Q(job__house__address__startswith=term) |
                    Q(job__house__address__endswith=term) |
                    Q(amount__startswith=term)
                    for term in query_terms)
                )

                #search expenses table
                queryset_expenses = functools.reduce(operator.__or__, (
                    Q(house__address__icontains=term) |
                    Q(house__address__startswith=term) |
                    Q(house__address__endswith=term) |
                    Q(amount__startswith=term) |
                    Q(expense_type__icontains=term) |
                    Q(expense_type__startswith=term) |
                    Q(expense_type__endswith=term)
                    for term in query_terms)
                )

                jobs = Job.objects.filter(queryset_jobs, house__customer=customer.customer)
                payments = Request_Payment.objects.filter(queryset_payments, job__house__customer=customer.customer)
                expenses = Expenses.objects.filter(queryset_expenses, house__customer=customer.customer)
                count = 0

                context['query'] = query
                context['count'] = count

                #if query results
                if jobs.exists():
                    context['jobs'] = jobs
                    context['count'] += int(jobs.count())
                if payments.exists():
                    context['payments'] = payments
                    context['count'] += int(payments.count())
                if expenses.exists():
                    context['expenses'] = expenses
                    context['count'] += int(expenses.count())

            else:
                upload_document_form = Upload_Document_Form()
                edit_job_form = Edit_Job(user=current_user)

        return HttpResponse(template.render(context, request))

class Search_Ajax_Submit_View(Search_Submit_View):
    template_name = 'search_submit/search_submit_results.html'

    def get(self, request):
        return redirect('/search')
