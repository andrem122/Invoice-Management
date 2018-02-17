import datetime

class Dates_And_Times():

    #filter results by current week
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)

    def __init__(self, houses, queryset, model):
        #initialize object with houses, queryset, and model
        self.houses = houses
        self.queryset = queryset
        self.model = model

    #fetch current weeks results
    def current_week_results(self, update_field={}, **kwargs):
        """fetch current week results, if there are none
        then set the appropriate house attributes to false"""
        for h in self.houses.iterator():
            for q in self.queryset.iterator():
                if q.house == h:
                    query_set_check = getattr(self.model, 'objects').filter(house=h, **kwargs)
                    if query_set_check:
                        setattr(h, list(update_field.keys())[0], list(update_field.values())[0][0])
                    else:
                        setattr(h, list(update_field.keys())[0], list(update_field.values())[0][1])

                    h.save(update_fields=[list(update_field.keys())[0]])
