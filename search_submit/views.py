from django.views.generic.base import View
from django.http import HttpResponse
from django.template import loader
from jobs.models import Job, Request_Payment
from django.db.models import Q
from customer_register.customer import Customer
import operator
import functools
import re

class Search_Submit_View(View):
    template_name = 'search_submit/search_submit.html'
    def post(self, request):
        def normalize_query(query_string,
            findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
            normspace=re.compile(r'\s{2,}').sub):

            '''
            Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
            Example:
            >>> normalize_query('  some random  words "with   quotes  " and   spaces')
                ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
            '''

            return [normspace(' ',(t[0] or t[1]).strip()) for t in findterms(query_string)]


        template = loader.get_template(self.template_name)
        query = request.POST.get('search')
        query_terms = normalize_query(query)
        customer = Customer(request.user)
        queryset_jobs, queryset_payments = [], []
        context = {'query': query}

        if query != '':
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

            jobs = Job.objects.filter(queryset_jobs, house__customer=customer.customer)
            payments = Request_Payment.objects.filter(queryset_payments, job__house__customer=customer.customer)
            count = int(jobs.count()) + int(payments.count())
            context['jobs'] = jobs
            context['payments'] = payments
            context['count'] = count

        return HttpResponse(template.render(context, request))
