from django.views.generic.base import View
from django.http import HttpResponse
from django.template import loader
from jobs.models import Job
from django.db.models import Q
from customer_register.customer import Customer
import operator
import functools
import re

class Search_Submit_View(View):
    template_name = 'search_submit/search_submit.html'
    def post(self, request):
        def normalize_query(query_string,
            findterms=re.compile(r'"([^"]+)"|(\S+)|(\d+)').findall,
            normspace=re.compile(r'\s{2,}').sub):

            '''
            Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
            Example:
            >>> normalize_query('  some random  words "with   quotes  " and   spaces')
                ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
            '''

            result = (normspace(' ',(t[0] or t[1]).strip()) for t in findterms(query_string))
            #convert nums to decimals
            def is_num(string):
                try:
                    float(string)
                    return True
                except ValueError as e:
                    return False

            return (t + '.00' for t in result if is_num(t))

        template = loader.get_template(self.template_name)
        query = request.POST.get('search')
        query_terms = normalize_query(query)
        customer = Customer(request.user)

        #search jobs table
        queryset = functools.reduce(operator.__or__, (
            Q(company__username__icontains=term) |
            Q(house__address__icontains=term) |
            Q(house__address__startswith=term) |
            Q(house__address__endswith=term) |
            Q(start_amount=term)
            for term in query_terms)
        )
        items = Job.objects.filter(queryset, house__customer=customer.customer)
        context = {'title': 'This is the response', 'query': query, 'items': items}
        return HttpResponse(template.render(context, request))
