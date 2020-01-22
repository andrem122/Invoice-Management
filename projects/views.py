from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from send_data.forms import Send_Data
from .forms import Archive_House, Edit_Project
from jobs.models import House
from django.contrib.auth.decorators import user_passes_test
from project_management.decorators import customer_and_staff_check
from django.core.paginator import Paginator
from itertools import chain
from django.views import View

class Projects(View):
    template_name = 'projects/projects.html'

    def get(self, request, *args, **kwargs):
        """
        Show all projects the customer currently has including
        completed projects and open ones
        """
        current_user = request.user

        narchived_houses = (
            House.objects.filter(
            archived=False,
            customer=current_user,
            )
            .add_total_spent()
            .add_num_approved_jobs()
            .add_num_expenses()
            .add_num_active_jobs()
        )

        archived_houses = (
            House.objects.filter(
            archived=True,
            customer=current_user,
            )
            .add_total_spent()
            .add_num_approved_jobs()
            .add_num_expenses()
            .add_num_active_jobs()
        )

        send_data_form = Send_Data()
        archive_house_form = Archive_House()
        edit_project_form = Edit_Project()

        projects_list = list(chain(narchived_houses, archived_houses))
        paginator = Paginator(projects_list, 25)

        page = request.GET.get('page')
        projects = paginator.get_page(page)
        narchived_houses_count = narchived_houses.count()
        archived_houses_count = archived_houses.count()

        context = {
            'projects': projects,
            'narchived_houses_count': narchived_houses_count,
            'archived_houses_count': archived_houses_count,
            'current_user': current_user,
            'archive_house_form': archive_house_form,
            'edit_project_form': edit_project_form,
            'send_data_form': send_data_form,
        }

        return render(request, Projects.template_name, context)

    def post(self, request, *args, **kwargs):

        # Edit Project Form
        if 'edit_project' in request.POST:
            if edit_project_form.is_valid():
                project_id = int(request.POST.get('project_id')) #get project id from POST request
                project = get_object_or_404(House, id=project_id) #get project object from database
                # Get new data values from form
                new_address = edit_project_form.cleaned_data.get('address', None)
                new_purchase_price = edit_project_form.cleaned_data.get('purchase_price', None)
                new_profit = edit_project_form.cleaned_data.get('profit', None)
                new_after_repair_value = edit_project_form.cleaned_data.get('after_repair_value', None)

                # Save new data into object
                if new_address != None:
                    project.address = new_address

                    #update object
                    project.save(update_fields=['address'])

                if new_purchase_price != None:
                    project.purchase_price = new_purchase_price

                    #update object
                    project.save(update_fields=['purchase_price'])

                if new_profit != None:
                    project.profit = new_profit

                    #update object
                    project.save(update_fields=['profit'])

                if new_after_repair_value != None:
                    project.after_repair_value = new_after_repair_value

                    #update object
                    project.save(update_fields=['after_repair_value'])

            if request.is_ajax():
                return load_ajax_search_results(request)
            else:
                return request.POST.get('post_from_url', None)

@user_passes_test(customer_and_staff_check, login_url='/accounts/login/')
def projects(request):
    current_user = request.user


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        archive_house_form = Archive_House(request.POST)
        edit_project_form = Edit_Project(request.POST)

        if archive_house_form.is_valid():
            #get house ID from POST request
            house_id = int(request.POST.get('house_id'))

            #store form data into variables
            house = House.objects.get(pk=house_id)

            if house.archived == False: #if house.archived is False
                house.archived = True
                house.save(update_fields=['archived'])
            else: #if house.archived is True already
                house.archived = False
                house.save(update_fields=['archived'])


            return redirect('/projects')
        else:
            print(archive_house_form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        archive_house_form = Archive_House()

    return HttpResponse(template.render(context, request))
