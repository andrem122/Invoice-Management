from django.views.generic.base import View
from django.http import HttpResponse
from django.template import loader
from jobs.models import Job, Request_Payment
from expenses.models import Expenses
from expenses.forms import Edit_Expense
from django.db.models import Q
from django.shortcuts import redirect
from customer_register.customer import Customer
from payment_history.forms import Upload_Document_Form
from expenses.forms import Delete_Expense
from jobs_admin.forms import Approve_Job, Approve_As_Payment, Reject_Estimate, Edit_Job
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.views.decorators.csrf import csrf_exempt
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

    def search_results(self, query, request, context, ajax=False):
        queryset_jobs, queryset_payments = [], []
        customer = Customer(request.user)
        context['count'] = 0


        if query != None and query != '':
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

            jobs = Job.objects.filter(queryset_jobs, house__customer=customer.customer).add_balance()
            payments = Request_Payment.objects.filter(queryset_payments, job__house__customer=customer.customer)
            expenses = Expenses.objects.filter(queryset_expenses, house__customer=customer.customer)

            context['query'] = query

            # Replace the post_from_url with the format 'search/?search=' + query
            replacement_string = 'search/?search=' + query
            if 'ajax' in request.build_absolute_uri():
                context['post_from_url'] = request.build_absolute_uri().replace('ajax', '')
            elif 'payments' in request.build_absolute_uri():
                context['post_from_url'] = request.build_absolute_uri().replace('payments/', replacement_string)
            else:
                context['post_from_url'] = request.build_absolute_uri().replace('jobs-admin/', replacement_string)

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

            if ajax:
                context['edit_job_form'] = Edit_Job(user=request.user)
                context['edit_expense_form'] = Edit_Expense(user=request.user)
                context['approve_form'] = Approve_Job()
                context['approve_as_payment_form'] = Approve_As_Payment()
                context['reject_estimate_form'] = Reject_Estimate()
                context['upload_document_form'] = Upload_Document_Form()
                context['delete_exp_form'] = Delete_Expense()
                context['request'] = request

                return render_to_string('search_submit/search_submit_results.html', context)

            return context

        else:
            upload_document_form = Upload_Document_Form()
            edit_job_form = Edit_Job(user=request.user)
            edit_expense_form = Edit_Expense(user=request.user)

            if not ajax:
                return context
            else:
                return render_to_string('search_submit/search_submit_results.html', context)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(user_passes_test(customer_and_staff_check, login_url='/accounts/login/'))
    def get(self, request):
        current_user = request.user
        template = loader.get_template(self.template_name)
        upload_document_form = Upload_Document_Form()
        send_data_form = Send_Data()
        edit_job_form = Edit_Job(user=current_user)
        edit_expense_form = Edit_Expense(user=current_user)
        query = request.GET.get('search', None)

        context = {
            'current_user': current_user,
            'upload_document_form': upload_document_form,
            'send_data_form': send_data_form,
            'edit_job_form': edit_job_form,
            'edit_expense_form': edit_expense_form,
        }

        context = self.search_results(query=query, request=request, context=context)
        return HttpResponse(template.render(context, request))

class Search_Submit_Ajax_View(Search_Submit_View):
    template_name = 'search_submit/search_submit_results.html'

    def get(self, request):
        current_user = request.user
        query = request.GET.get('search', None)

        if request.is_ajax():
            html = self.search_results(query=query, request=request, context={'current_user': current_user,}, ajax=True)
            return HttpResponse(html)
        else:
            return redirect('/search')
