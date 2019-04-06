from jobs_admin.forms import Edit_Job
from django.template.loader import render_to_string
from itertools import chain

class Ajax:
    """
    Creates an object to load ajax results
    customer: a User object representing the customer
    """

    def __init__(self, customer):
        self.customer = customer

    def load_ajax_results(self, object_type):

        #job ajax results
        if object_type is 'jobs':
            #get active houses and houses with estimates
            active_houses = self.customer.active_houses()
            estimate_houses = self.customer.current_week_proposed_jobs_houses()
            completed_houses = self.customer.current_week_completed_houses()
            rejected_houses = self.customer.current_week_rejected_job_houses()

            #get estimates, approved, completed, and rejected jobs
            estimates = self.customer.current_week_proposed_jobs()
            approved_jobs = self.customer.approved_jobs()
            completed_jobs = self.customer.current_week_completed_jobs()
            rejected_jobs = self.customer.current_week_rejected_jobs()

            #get forms
            edit_job_form = Edit_Job(user=self.customer.customer)

            #combine querysets and keep unique values for houses
            houses = set(chain(active_houses, estimate_houses, completed_houses, rejected_houses))
            jobs = list(chain(estimates, approved_jobs, completed_jobs, rejected_jobs))

            context = {
                'houses': houses,
                'items': jobs,
                'current_user': self.customer.customer,
                'edit_job_form': edit_job_form,
            }

            return render_to_string('jobs_admin/jobs_admin_results.html', context)

        #payments ajax results
        elif object_type is 'payments':
            payment_history_houses = self.customer.current_week_payment_history_houses()
            payment_request_houses = self.customer.current_week_payment_requests_houses()
            rejected_payment_houses = self.customer.current_week_rejected_payment_houses()
            expenses_houses = self.customer.expenses_houses_pay()

            #get all payments and expenses for current week
            payments = self.customer.current_week_payments_all()

            #combine querysets and keep unique items
            houses = set(chain(payment_history_houses, payment_request_houses, rejected_payment_houses))

            context = {
                'houses': houses,
                'items': payments,
                'current_user': self.customer.customer,
            }

            return render_to_string('payment_requests/payments_results.html', context)
