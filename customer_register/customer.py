from jobs.models import Job, Current_Worker, House
class Customer():

    def __init__(self, customer):
        self.customer = customer
        self.current_houses = self.current_houses()

    #returns houses that are activley being worked on by workers
    def current_houses(self):
        #get all customer houses and houses with active jobs
        customer_houses = House.objects.filter(customer=self.customer)
        current_houses = Current_Worker.objects.filter(current=True)

        """compare house with active jobs to customer house
        if the house are the same, then it is a current customer house"""
        current_customer_houses = []
        for h in customer_houses.iterator():
            for c_h in current_houses.iterator():
                if c_h.house == h:
                    current_customer_houses.append(c_h)

        return current_customer_houses

    #returns all approved houses for the customer
    def approved_jobs(self):
        #get all customer workers jobs that are approved
        jobs = Job.objects.filter(approved=True, balance_amount__gt=0)

        customer_worker_jobs = []
        for h in self.current_houses:
            for j in jobs:
                if j.house.customer == h.house.customer:
                    customer_worker_jobs.append(j)

        return customer_worker_jobs
