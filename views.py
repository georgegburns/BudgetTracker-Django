from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .form import *
from .filters import spendfilter
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import csv
import datetime 


# Create your views here.
def index(request):
    context = {
        "title" : "Welcome To BirdNest",     
    }
    return render(request, 'index.html', context)

@login_required
def download(request):
    context = {
        "title" : "Download"
    }
    return render(request, 'download.html', context)

@login_required
def profile(request):
    context = {
    "title" : "Profile"
    }
    return render(request, 'profile.html', context)

@login_required
def Forecast(request):
    context = {
        "title" : "Forecast",     
    }
    return render(request, 'forecast.html', context)

@login_required
def Input(request):
    if request.method == "POST":
        if "add" in request.POST:
            form = BudgetForm(request.POST or None)
            if form.is_valid():
                form.save(commit=False).owner = request.user
                form.save()
                messages.success(request, ('New Spend Added!'))
            else:
                if form.errors.get('cost_centre') != None:
                    messages.error(request, ('The following error occured: ' + form.errors.get('cost_centre').as_text().replace('*','')))
                if form.errors.get('nominal') != None:    
                    messages.error(request, ('The following error occured: ' + form.errors.get('nominal').as_text().replace('*','')))
                if form.errors.get('supplier') != None:    
                    messages.error(request, ('The following error occured: ' + form.errors.get('supplier').as_text().replace('*','')))
                if form.errors.get('date') != None:    
                    messages.error(request, ('The following error occured: ' + form.errors.get('date').as_text().replace('*','')))
                if form.errors.get('spend') != None:    
                    messages.error(request, ('The following error occured: ' + form.errors.get('spend').as_text().replace('*','')))
                if form.errors.get('spend_type') != None:    
                    messages.error(request, ('The following error occured: ' + form.errors.get('spend_type').as_text().replace('*','')))
                else:
                    messages.error(request, ('Missing Required Field'))
            return redirect('Input')
        elif "upload" in request.POST:
            form = BudgetUploadForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save(commit=False).owner = request.user
                form.save()
                obj = BudgetUpload.objects.get(activated=False)
                obj.activated = True
                obj.save()
                count = 0
                cc_count = 0
                nom_count = 0
                sup_count = 0 
                st_count = 0
                total_count = 0
                with open(obj.file_name.path, 'r') as f:
                    reader = csv.reader(f)
                    for i,row in enumerate(reader):
                        if i==0:
                            pass
                        else:
                            cost_centre = row[0]
                            cc_test = CC_Choices.objects.filter(cost_centre = cost_centre).first()
                            nominal = row[1]
                            nom_test = Nom_Choices.objects.filter(nominal = nominal).first()
                            supplier = row[2]
                            sup_test = Sup_Choices.objects.filter(supplier = supplier).first()
                            spend_type = row[5]
                            st_test = ST_Choices.objects.filter(spend_type = spend_type).first()
                            spend = row[4]
                            if isinstance(spend, int) or isinstance(spend, float):
                                messages.error('Invalid Spend Format')
                                break 
                            description = row[6]
                            date = row[3]
                            if datetime.datetime.strptime(date, "%d/%m/%Y").strftime('%Y-%m-%d') == False:
                                messages.error('Invalid Date Format')
                                break
                            if cc_test == None:
                                cc_count += 1
                            if nom_test == None:
                                nom_count += 1
                            if sup_test == None:
                                sup_count += 1
                            if st_test == None:
                                st_count += 1
                            if st_test == None or sup_test == None or nom_test == None or cc_test == None:
                                total_count += 1
                            if cc_test and sup_test and nom_test and st_test:
                                BudgetInput.objects.create(
                                    cost_centre = CC_Choices.objects.get(cost_centre = cost_centre),
                                    nominal = Nom_Choices.objects.get(nominal = nominal),
                                    supplier = Sup_Choices.objects.get(supplier = supplier),
                                    spend = spend,
                                    spend_type = ST_Choices.objects.get(spend_type = spend_type),
                                    description = description,
                                    date = datetime.datetime.strptime(date, "%d/%m/%Y").strftime('%Y-%m-%d'),
                                    owner = request.user,
                                )
                                count += 1
                            else: 
                                pass
                messages.success(request, (f'{count} spends successfully uploaded'))
                messages.error(request, (f'{total_count} inputs failed to upload.'))
                messages.error(request, (f'{cc_count} had invalid cost centres.'))
                messages.error(request, (f'{nom_count} had invalid nominals.'))
                messages.error(request, (f'{sup_count} had invalid suppliers.'))
                messages.error(request, (f'{st_count} had invalid spend types.'))
            return redirect('Input')
        elif "edit" in request.POST:
            pass
    if request.method == "GET":
        if 'delete_all' in request.GET:
            BudgetInput.objects.filter(owner=request.user).delete()
            return redirect('Input')
        elif 'download' in request.GET:
            inputs = BudgetInput.objects.filter(owner=request.user)
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename=spends_export.csv'
            writer = csv.writer(response)
            writer.writerow(['Cost Centre', 'Nominal', 'Supplier', 'Spend', 'Spend Type', 'Description', 'Date'])
            inputs_fields = inputs.values_list('cost_centre', 'nominal', 'supplier', 'spend', 'spend_type', 'description', 'date')
            for input in inputs_fields:
                writer.writerow(input)
            return response
        elif 'template' in request.GET:
            inputs = ['XX0000', '0000 - XXXXXX', 'XXXXXX', '00.00', 'XX', 'XXXXXX', 'DD/MM/YY']
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename=spends_template.csv'
            writer = csv.writer(response)
            writer.writerow(['Cost Centre', 'Nominal', 'Supplier', 'Spend', 'Spend Type', 'Description', 'Date'])
            writer.writerow(inputs)
            return response
        else:
            context = {}
            all_inputs = BudgetInput.objects.filter(owner=request.user).order_by('-date')
            context['all_inputs'] = all_inputs
            spending_filter = spendfilter(request.GET, queryset=all_inputs)
            context['filter'] = spending_filter
            Upload = BudgetUploadForm(request.POST or None, request.FILES or None)
            context['Upload'] = Upload
            paginator = Paginator(spending_filter.qs, 25)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            context['page_obj'] = page_obj
            context['cc_choices'] = CC_Choices.objects.all()
            context['nom_choices'] = Nom_Choices.objects.all()
            context['sup_choices'] = Sup_Choices.objects.all()
            context['spendtype_choices'] = ST_Choices.objects.all()
            return render(request, 'input.html', context)

@login_required
def delete_input(request, input_id):
    input = BudgetInput.objects.get(pk=input_id)
    if input.owner == request.user:
        input.delete()
    else:
        messages.error(request,"Access Denied")
    return redirect('Input')

@login_required
def edit_input(request, input_id):
    if request.method == "POST":
        input = BudgetInput.objects.get(pk=input_id)
        form = BudgetForm(request.POST or None, instance= input)
        if form.is_valid():
            form.save()
            messages.success(request, ('Spend Edited!'))
        else:
            if form.errors.get('cost_centre') != None:
                messages.error(request, ('The following error occured: Cost Centre: ' + form.errors.get('cost_centre').as_text().replace('*','')))
            if form.errors.get('nominal') != None:    
                messages.error(request, ('The following error occured: Nominal: ' + form.errors.get('nominal').as_text().replace('*','')))
            if form.errors.get('supplier') != None:    
                messages.error(request, ('The following error occured: Supplier: ' + form.errors.get('supplier').as_text().replace('*','')))
            if form.errors.get('date') != None:    
                messages.error(request, ('The following error occured: Date: ' + form.errors.get('date').as_text().replace('*','')))
            if form.errors.get('spend') != None:    
                messages.error(request, ('The following error occured: Spend: ' + form.errors.get('spend').as_text().replace('*','')))
            if form.errors.get('spend_type') != None:    
                messages.error(request, ('The following error occured: Spend Type: ' + form.errors.get('spend_type').as_text().replace('*','')))
            else:
                messages.error(request, ('Missing Required Field'))
        all_inputs = BudgetInput.objects.filter(owner=request.user)
        paginator = Paginator(all_inputs, 25)
        input_obj = BudgetInput.objects.get(pk=input_id)
        return render(request, 'input.html', {'input_obj': input_obj, 'all_inputs': all_inputs})
    else:
        
        all_inputs = BudgetInput.objects.filter(owner=request.user)
        paginator = Paginator(all_inputs, 25)
        input_obj = BudgetInput.objects.get(pk=input_id)
        return render(request, 'edit.html', {'input_obj': input_obj, 'all_inputs': all_inputs})


@login_required
def Budget(request):
    if request.method == "POST":
        if "add" in request.POST:
            form1 = CCForm(request.POST or None)
            form2 = NomForm(request.POST or None)
            form3 = SupForm(request.POST or None)
            form4 = STForm(request.POST or None)
            if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
                form1.save()
                form2.save()
                form3.save()
                form4.save()
                messages.success(request, ('New Values Have Been Added!'))
            else:
                messages.error(request, ('Invalid Entry'))
        if 'uploadvalue' in request.POST:
            form = ValueUploadForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save(commit=False).owner = request.user
                form.save()
                obj = ValueUpload.objects.get(activated=False)
                obj.activated = True
                obj.save()
                with open(obj.file_name.path, 'r') as f:
                    reader = csv.reader(f)
                    for i,row in enumerate(reader):
                        print(row)
                        if i==0:
                            pass
                        else:
                            cost_centre = row[0]
                            nominal = row[2]
                            supplier = row[1]
                            spend_type = row[3]
                            if cost_centre != "":
                                if cost_centre in CC_Choices.objects.values():
                                    messages.info(request, ('Cost Centre Already Exists'))
                                else:
                                    CC_Choices.objects.create(
                                        cost_centre = cost_centre,
                                    )     
                            if nominal != "":
                                if nominal in Nom_Choices.objects.values():
                                    messages.info(request, ('Nominal Already Exists'))
                                else: 
                                   Nom_Choices.objects.create(
                                        nominal = nominal,
                                    )  
                            if supplier != "":
                                if supplier in Sup_Choices.objects.values():
                                    messages.info(request, ('Supplier Already Exists'))#
                                else:
                                    Sup_Choices.objects.create(
                                        supplier = supplier,
                                    )  
                            if spend_type != "":
                                if spend_type in ST_Choices.objects.values():
                                    messages.info(request, ('Spend Type Already Exists'))
                                else:
                                    ST_Choices.objects.create(
                                        spend_type = spend_type,
                                    )              
                messages.success(request, ('Values Uploaded'))
            else:
                messages.error(request, ('Invalid File'))
        return redirect('Budget')
    else:
        context = {
            "title" : "Admin",     
        }
        context['CCForm'] = CCForm(request.POST or None)
        context['NomForm'] = NomForm(request.POST or None)
        context['SupForm'] = SupForm(request.POST or None)
        context['STForm'] = STForm(request.POST or None)
        context['ValueUpload'] = ValueUploadForm(request.POST or None, request.FILES or None)
        return render(request, 'budget.html', context)