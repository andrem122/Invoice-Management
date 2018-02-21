from jobs.models import Job, Current_Worker, House
class Customer():

    def __init__(self, customer):
        self.customer = customer
        self.houses = self.houses()
        self.current_houses = self.current_houses()
        self.completed_houses = self.completed_houses()

    #gets attributes of objects up to two levels down
    def attribute_level(self, obj, compare={}):
        level = list(compare.keys())
        attribute = list(compare.values())

        if level[0] is not 0:
            if level[0] is 1:
                return getattr(obj, attribute[0])
            elif level[0] is 2:
                return getattr(getattr(obj, attribute[0][0]), attribute[0][1])
        else:
            return obj

    #reduces repetition of looping code to get a query set
    def get_queryset(self, append_outer=False, houses=[], queryset=[], compare=[]):
        result_queryset = []
        for h in houses:
            for q in queryset.iterator():
                #get attributes to compare
                a = self.attribute_level(obj=h, compare=compare[0])
                b = self.attribute_level(obj=q, compare=compare[1])
                if a == b:
                    if append_outer == True:
                        result_queryset.append(h)
                    else:
                        result_queryset.append(q)

        return result_queryset

    #returns all houses that belong to the customer
    def houses(self):
        return House.objects.filter(customer=self.customer)

    #returns houses that are activley being worked on by workers
    def current_houses(self):
        """compare house with active jobs to customer house
        if the houses are the same, then it is a current customer house"""
        #get all customer houses and houses with active jobs
        houses = Current_Worker.objects.filter(current=True)
        return self.get_queryset(append_outer=True, houses=houses, queryset=self.houses, compare=[{1: 'house'}, {0: 0}])

    #returns all approved jobs for houses for each customer
    def approved_jobs(self):
        #get all customer workers jobs that are approved
        approved_jobs = Job.objects.filter(approved=True, balance_amount__gt=0)
        return self.get_queryset(houses=self.current_houses, queryset=approved_jobs, compare=[{2: ['house', 'customer']}, {2: ['house', 'customer']}])

    #returns all houses with completed jobs
    def completed_houses(self):
        return House.objects.filter(customer=self.customer, completed_jobs=True)

    #return all completed jobs
    def completed_jobs(self):
        completed_jobs = Job.objects.filter(approved=True, balance_amount__lte=0)
        return self.get_queryset(houses=self.completed_houses, queryset=completed_jobs, compare=[{0: 0}, {1: 'house'}])
