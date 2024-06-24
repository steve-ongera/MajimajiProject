from django.shortcuts import render
from django.db.models import Avg
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from datetime import datetime
from django.urls import reverse
from django.db.models import Sum
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect , get_object_or_404
from django.db.models import Count, Sum
from decimal import Decimal  # Import Decimal

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')

def admin_dashboard(request):
    # Count number of tenants
    num_tenants = Tenant.objects.count()
    
    # Query to get payments aggregated by month
    payments_by_month = Payment.objects.values('month__name').annotate(total_payments=Count('id'), total_amount=Sum('amount'))
    
    # Prepare data for chart (labels and data)
    labels = []
    total_payments_data = []
    total_amount_data = []
    
    for item in payments_by_month:
        labels.append(item['month__name'])
        total_payments_data.append(item['total_payments'])
        # Convert Decimal to float for JavaScript compatibility
        total_amount_data.append(float(item['total_amount']))
    
    context = {
        'num_tenants': num_tenants,
        'labels': labels,
        'total_payments_data': total_payments_data,
        'total_amount_data': total_amount_data,
    }
    return render(request, 'admin_dashboard.html', context)






def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, ' You have been logged in successfully.')
            return redirect('home')  # Replace 'dashboard' with your desired URL name
        else:
            # Return an 'invalid login' error message.
            messages.error(request, ' Username or Password did not match. Try again.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    


    
    
def custom_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            identification_number = form.cleaned_data.get('identification_number')
            password = form.cleaned_data.get('password1')

            # Get the CompanyStaff instance
            staff = tenants_database.objects.get(username=username, identification_number=identification_number)

            # Create a new user
            if User.objects.filter(username=username):
                messages.warning(request,"The Username with that ID No already exist!")
            else:
                user = User.objects.create_user(username=username, password=password)
                Profile.objects.create(user=user, user_type='guest')
                user.email = staff.email
                user.first_name = staff.first_name
                user.last_name = staff.last_name
                # Save other fields as needed

                user.save()
                login(request, user)
                messages.success(request, 'You account has been created successfully.')
                return redirect('home')
           
        
           
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request, 'home.html') 


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('home'))



@login_required
@user_passes_test(lambda u: u.profile.user_type == 'guest')

def dashboard(request):
    tenant = Tenant.objects.filter(user_name=request.user.username).first()

    if not tenant:
        return render(request, 'error_404.html', {'user': request.user})
    
    #tenant = get_object_or_404(Tenant, user_name=request.user.username)
    payments = Payment.objects.filter(tenant=tenant)
    months = Month.objects.filter(payment__in=payments).distinct()
    month_payments_map = {}
    for month in months:
        month_payments_map[month] = payments.filter(month=month)
    
    context = {
        'tenant': tenant,
        'month_payments_map': month_payments_map,
    }
    return render(request, 'dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')

def tenant_payment_status(request):
    tenants = Tenant.objects.all()
    months = Month.objects.all().order_by('start_date')
    
    payment_data = {}
    for tenant in tenants:
        payment_data[tenant] = {}
        for month in months:
            # Adjust this logic based on how you're tracking payments
            payment = Payment.objects.filter(tenant=tenant, month=month).exists()
            payment_data[tenant][month] = payment

    context = {
        'tenants': tenants,
        'months': months,
        'payment_data': payment_data,
    }
    return render(request, 'tenant_payment_status.html', context)



@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment added successfully.')
            return redirect('payment_status')
    else:
        form = PaymentForm()
    return render(request, 'add_payment.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')

def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment updated successfully.')
            return redirect('tenant_payment_status')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'edit_payment.html', {'form': form, 'payment': payment})


@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Payment deleted successfully.')
        return redirect('tenant_payment_status')
    return render(request, 'delete_payment.html', {'payment': payment})



def tenant_payment_history(request):
    return render(request, 'tenant_payment_history.html')


@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def tenant_list(request):
    tenants = Tenant.objects.all()
    context = {
        'tenants': tenants
    }
    return render(request, 'tenant_list.html', context)

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def tenant_detail(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    payments = Payment.objects.filter(tenant=tenant)
    
    context = {
        'tenant': tenant,
        'payments': payments,
    }
    return render(request, 'tenant_detail.html', context)

@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def tenant_update(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    context = {
        'form': form,
        'tenant': tenant
    }
    return render(request, 'tenant_update.html', context)


@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def tenant_delete(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        tenant.delete()
        return redirect('tenant_list')
    context = {
        'tenant': tenant
    }
    return render(request, 'tenant_delete.html', context)

@login_required
def maintenance_request_create(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.tenant = tenant
            request_obj.save()
            messages.success(request, 'Maintenance request submitted successfully.')
            return redirect('tenant_detail', tenant_id=tenant.id)
    else:
        form = MaintenanceRequestForm()
    
    context = {
        'form': form,
        'tenant': tenant,
    }
    return render(request, 'maintenance_request_create.html', context)

@login_required
def maintenance_request_list(request):
    requests = MaintenanceRequest.objects.all()
    context = {
        'requests': requests
    }
    return render(request, 'maintenance_request_list.html', context)

def respond_to_request(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, id=request_id)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            maintenance_request.response = response  # Save response to model
            maintenance_request.status = 'responded'
            maintenance_request.save()
            messages.success(request, 'Response sent successfully.')
            return redirect('maintenance_request_list')
    else:
        form = ResponseForm()
    
    context = {
        'maintenance_request': maintenance_request,
        'form': form,
    }
    return render(request, 'respond_to_request.html', context)


@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def add_tenant(request):
    if request.method =='POST':
        form=TenantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenant Data successfully added to Tenants Database.')
            return redirect('tenant_list')
    else:
        form= TenantForm()
    return render(request, 'add_tenant.html', { 'form':form})



@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def add_tenant_databse(request):
    if request.method =='POST':
        form=tenants_databaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Information successfully added to Application Database.')
            return redirect('user_list')
    else:
        form= tenants_databaseForm()
    return render(request, 'add_tenant_databse.html', { 'form':form})



@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def user_list(request):
    tenants = tenants_database.objects.all()
    context = {
        'tenants': tenants
    }
    return render(request, 'user_list.html', context)



@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def add_house(request):
    if request.method =='POST':
        form=HouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'House  successfully created.')
            return redirect('house_list')
    else:
        form= HouseForm()
    return render(request, 'house.html', { 'form':form})


@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def house_list(request):
    tenants = House.objects.all()
    context = {
        'tenants': tenants
    }
    return render(request, 'house_list.html', context)



@login_required
@user_passes_test(lambda u: u.profile.user_type == 'admin')
def search_tenant(request):
    if request.method == 'POST':
        identification_number = request.POST.get('identification_number', '')
        try:
            tenant = Tenant.objects.get(identification_number=identification_number)
        except Tenant.DoesNotExist:
            tenant = None
        
        return render(request, 'search_tenant.html', {'tenant': tenant})
    else:
        return render(request, 'search_tenant.html')


