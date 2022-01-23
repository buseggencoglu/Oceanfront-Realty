import copy
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from account.forms import EditProfileForm
from .filters import houseFilter

from .models import House, Reservation, PrivateMsg, EstatePersonal, Branch, Customer, Admin, Profile, Notifications
from .forms import houseForm, ReservationSearchForm, MessageForm, ReservationForm, CredithousedForm, ApprovehouseDealer, \
    BranchForm


def home(request):
    context = {
        "title": "OceanFrontReality",
        "locations": Branch.objects.all().values('branch_name')
    }
    return render(request, 'home.html', context)


def available_houses(request):
    request_data = copy.deepcopy(request.POST)
    dates = request_data['dates'].split(' - ')
    request_data['pickUpDate'] = dates[0]
    request_data['returnDate'] = dates[1]

    data = ReservationSearchForm(request_data).data

    start_date_date = datetime.strptime(data['pickUpDate'], '%m/%d/%Y').strftime("%Y-%m-%d")
    end_date_date = datetime.strptime(data['returnDate'], '%m/%d/%Y').strftime("%Y-%m-%d")

    if datetime.strptime(data['pickUpDate'], '%m/%d/%Y') <= datetime.now():
        return HttpResponse('Start date cannot selected from past!')

    busy_houses = Reservation.busy_houses(start_date_date, end_date_date)

    branch_name = Branch.get_by_branch_name(data['location'])
    houses = House.search_for_house(busy_houses, branch_name[0])

    if len(houses) == 0:
        return HttpResponse('No available houses')

    context = {
        "title": "OceanFrontReality",
        'houses': houses,
        'pickUpDate': start_date_date,
        'returnDate': end_date_date,
        'location': data['location'],
    }
    return render(request, 'house/available_houses.html', context)


@login_required()
def create_reservation(request, house_id, location, pickUpDate, returnDate):
    house = House.objects.get(id=house_id)
    start_date_date = datetime.strptime(pickUpDate, '%Y-%m-%d')
    end_date_date = datetime.strptime(returnDate, '%Y-%m-%d')
    form = ReservationForm(initial={
        'house': house,
        'customer': request.user,
        'location': location,
        'pickUpDate': pickUpDate,
        'returnDate': returnDate,
        'total_price': house.price * (end_date_date - start_date_date).days
    })
    housed_form = CredithousedForm()

    context = {
        "title": "OceanFrontReality",
        "reservation_form": form,
        "house_detail": house,
        "housed_form": housed_form
    }

    return render(request, 'reservation/reservation_order.html', context)


@login_required()
def complete_reservation(request):
    posted_data = request.GET
    branch_name = request.GET.get('location')
    customer_name = request.GET.get('customer_name')
    form = ReservationForm(posted_data)
    credit_form = CredithousedForm(posted_data)
    user = request.user
    customers = Customer.objects.filter(user=user)
    house_dealers = EstatePersonal.objects.filter(user=user)
    branch = Branch.objects.filter(branch_name=branch_name)[0]
    status = False
    if form.is_valid() and len(customers) == 0 and not request.is_ajax():
        reservation = form.save(commit=False)
        reservation.paymentStatus = False
        reservation.estate_person = house_dealers[0]
        reservation.customer_name = customer_name
        branch.save()
        reservation.save()
        status = True
    elif form.is_valid() and credit_form.is_valid() and not request.is_ajax():
        reservation = form.save(commit=False)
        reservation.paymentStatus = True
        reservation.customer = customers[0]
        branch.save()
        reservation.save()
        status = True

    context = {
        "title": "OceanFrontReality",
        "status": status
    }

    return render(request, 'reservation/reservation_approve.html', context)


def house_list(request):
    context = {}
    user = request.user
    house_dealers = EstatePersonal.objects.filter(user=user)
    if len(house_dealers) > 0:
        context["dataset"] = House.objects.filter(branch=house_dealers[0].branch)

    return render(request, 'house/house_list.html', context)


def total_house_list(request):
    context = {}
    user = request.user
    labels = []
    data = []
    admin = Admin.objects.filter(user=user)
    if len(admin) > 0:
        context["houses"] = House.objects.all()
        context["house_dealers"] = EstatePersonal.objects.filter(user__is_active=False)
        context["branch_form"] = ApprovehouseDealer()
        context["house_dealers_dataset"] = EstatePersonal.objects.filter(user__is_active=True)

    queryset = Branch.objects.order_by('-id')
    for branch in queryset:
        labels.append(branch.branch_name)

    context['labels'] = labels
    context['data'] = data

    return render(request, 'admin/admin_dashboard.html', context)


def house_dealer_approve(request, pk):
    posted_data = ApprovehouseDealer(request.GET)
    dealer = EstatePersonal.objects.get(id=pk)
    dealer.user.is_active = True
    dealer.branch = Branch.objects.get(id=posted_data.data['dealer_branch'])
    dealer.save()
    dealer.user.save()

    return HttpResponseRedirect('/admin/dashboard')


def house_dealer_reject(request, pk):
    dealer = EstatePersonal.objects.get(id=pk)
    dealer.user.delete()
    dealer.delete()

    return HttpResponseRedirect('/admin/dashboard')


def house_detail(request, id=None):
    detail = get_object_or_404(House, id=id)
    context = {
        "detail": detail
    }
    return render(request, 'house/house_detail.html', context)


@login_required
def create_house(request, branch_page=None):
    user = request.user
    house_dealers = EstatePersonal.objects.filter(user=user)
    branch_id = None
    if len(house_dealers) > 0:
        branch_id = house_dealers[0].branch
    if branch_page:
        branch_id = Branch.objects.get(pk=branch_page)
    posted_data = request.POST or None
    form = houseForm(posted_data, request.FILES or None, branch_status=len(house_dealers) > 0 or branch_page != None, initial={
        'branch': branch_id
    })

    if form.is_valid():
        instance = form.save(commit=False)
        instance.pk = None
        instance.save()
        if len(house_dealers) > 0:
            return redirect('/house/list')
        else:
            if branch_page:
                return redirect(f'/branch/branch_house_list/{branch_page}')
            return redirect('/admin/dashboard')
    context = {
        "form": form,
        "title": "Create house"
    }
    return render(request, 'house/create_house.html', context)


def search(request):
    house_list = House.objects.all()
    house_filter = houseFilter(request.GET, queryset=house_list)
    return render(request, 'house/search.html', {'filter': house_filter, 'house_list': house_list})


def search_results(request):
    house_list = House.objects.all()
    house_filter = houseFilter(request.GET, queryset=house_list)
    return render(request, 'house/search_results.html', {'filter': house_filter, 'house_list': house_list})


@login_required()
def house_update(request, pk, branch_page=None):
    detail = get_object_or_404(House, pk=pk)

    user = request.user
    house_dealers = EstatePersonal.objects.filter(user=user)
    form = houseForm(request.POST or None, request.FILES or None, branch_status=len(house_dealers) > 0 or branch_page != None,
                   instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if len(house_dealers) > 0:
            return redirect('/house/list')
        else:
            if branch_page:
                return redirect(f'/branch/branch_house_list/{branch_page}')
            return redirect('/admin/dashboard')

    context = {
        "form": form,
        "title": "Update house"
    }
    return render(request, 'house/house_update.html', context)


@login_required()
def house_delete(request, pk):
    query = get_object_or_404(House, pk=pk)
    query.delete()

    house = House.objects.all()
    context = {
        'house': house,
    }
    return render(request, 'house/house_deleted.html', context)


def reservation_list_old(request):
    reservation = Reservation.objects.all()

    query = request.GET.get('q')
    if query:
        reservation = reservation.filter(
            Q(pickUpLocation__icontains=query) |
            Q(pickUpDate__icontains=query) |
            Q(returnDate__icontains=query)
        )

    # pagination
    paginator = Paginator(reservation, 4)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        reservation = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reservation = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reservation = paginator.page(paginator.num_pages)
    context = {
        'reservation': reservation,
    }
    return render(request, 'reservation/reservation_list.html', context)


@login_required()
def reservation_list(request):
    context = {}
    context["dataset"] = Reservation.objects.filter(pickUpDate__gte=timezone.now())
    return render(request, 'reservation/reservation_list.html', context)


@login_required()
def reservation_detail(request, id=None):
    detail = get_object_or_404(Reservation, id=id)
    context = {
        "detail": detail,
    }
    return render(request, 'reservation/reservation_detail.html', context)


@login_required()
def reservation_created(request):
    form = ReservationSearchForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title": "Create Reservation"
    }
    return render(request, 'reservation/reservation_create.html', context)


@login_required()
def reservation_update(request, id=None):
    detail = get_object_or_404(Reservation, id=id)
    form = ReservationSearchForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title": "Update Reservation"
    }
    return render(request, 'reservation/reservation_create.html', context)


@login_required()
def reservation_delete(request, pk=None):
    query = get_object_or_404(Reservation, id=pk)
    if query.pickUpDate < timezone.now():
        return HttpResponse("Pick up has passed!Cannot delete.")
    houseDealers = EstatePersonal.objects.filter(user=request.user)
    url = '/reservations/customer'
    message = f'{query} is canceled by {request.user.username}. Your payment will returned!'
    if len(houseDealers) > 0:
        url = '/reservations/housedealer'
        f'{query} is canceled by you. Your payment will returned!'
    if query.customer:
        notification = Notifications(
            message=message,
            user=query.customer.user
        )
        notification.save()
    query.delete()
    return HttpResponseRedirect(url)


@login_required()
def view_my_reservation_housedealer(request):
    username = request.user
    user = User.objects.get(username=username)
    estate = EstatePersonal.objects.get(user=user)
    pickup = estate.branch.branch_name
    reservations = Reservation.objects.filter(location=pickup, pickUpDate__gte=timezone.now())
    return render(request, 'reservation/my_reservations.html', {'reservation_list': reservations,
                                                                'delete_url': ''})


@login_required()
def view_my_reservation_customer(request):
    username = request.user
    user = User.objects.get(username=username)
    reservations = Reservation.objects.filter(customer=Customer.get_customer_by_user(user),
                                              pickUpDate__gte=timezone.now())
    return render(request, 'reservation/my_reservations.html', {'reservation_list': reservations})


def contact(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/house/newhouse/")
    context = {
        "form": form,
        "title": "Contact With Us",
    }
    return render(request, 'admin/contact.html', context)


# -----------------Admin Section-----------------

def admin_msg(request):
    msg = PrivateMsg.objects.order_by('-id')
    context = {
        "house": msg,
    }
    return render(request, 'admin/admin_msg.html', context)


def msg_delete(request, id=None):
    query = get_object_or_404(PrivateMsg, id=id)
    query.delete()
    return HttpResponseRedirect("/message/")


def dashboard_house_list(request):
    houses = House.view_house_list()
    house_detail = House.view_house_detail(1)

    context = {
        "house_details": house_detail,
        "houses": houses
    }

    return render(request, 'house/house_detail.html', context)


def users(request):
    context = {}
    context["dataset"] = User.objects.all()

    return render(request, 'admin/users.html', context)


@login_required
def add_branch(request):
    form = BranchForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/branch/list')
    context = {
        "form": form
    }
    return render(request, 'admin/add_branch.html', context)


def branch_list(request):
    context = {}
    context["dataset"] = Branch.objects.all()
    return render(request, 'admin/branch_list.html', context)


@login_required()
def branch_update(request, pk):
    detail = get_object_or_404(Branch, pk=pk)

    form = BranchForm(request.POST or None, request.FILES or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/branch/list')
    context = {
        "form": form,
        "title": "Update Branch"
    }
    return render(request, 'admin/branch_update.html', context)


@login_required()
def branch_delete(request, pk):
    query = get_object_or_404(Branch, pk=pk)
    query.delete()

    branch = Branch.objects.all()
    context = {
        'branch': branch,
    }
    return render(request, 'admin/branch_deleted.html', context)


@login_required()
def delete_notification(request, pk):
    instance = get_object_or_404(Notifications, pk=pk)
    instance.delete()
    return HttpResponse(status=204)


@login_required()
def view_my_reservation_customer_history(request):
    username = request.user
    user = User.objects.get(username=username)
    reservations = Reservation.objects.filter(customer=Customer.get_customer_by_user(user),
                                              pickUpDate__lt=timezone.now())
    return render(request, 'reservation/reservation_history.html', {'reservation_history': reservations})


@login_required()
def view_my_reservation_housedealer_history(request):
    username = request.user
    user = User.objects.get(username=username)
    houseDealer = EstatePersonal.objects.get(user=user)
    pickup = houseDealer.branch.branch_name
    reservations = Reservation.objects.filter(location=pickup, pickUpDate__lt=datetime.now())
    return render(request, 'reservation/reservation_history.html', {'reservation_history': reservations,
                                                                    'delete_url': ''})


def view_my_reservation_admin_history(request):
    context = {}
    context["dataset"] = Reservation.objects.filter(pickUpDate__lt=datetime.now())
    return render(request, 'admin/admin_history.html', context)


def branch_house_list(request, pk):
    houses = House.objects.all()
    branch = get_object_or_404(Branch, id=pk)
    context = {"branch": branch}
    context["houses"] = houses

    return render(request, 'admin/branch_house_list.html', context)


@login_required()
def houseDealer_delete(request, pk):
    dealer = get_object_or_404(EstatePersonal, id=pk)
    dealer.user.delete()
    dealer.delete()
    profile = get_object_or_404(Profile, id=pk)
    profile.delete()
    return HttpResponseRedirect('/admin/dashboard')


def view_profile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    return render(request, 'layout/profile.html', {'profile': profile})


def edit_profile(request, pk):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context = {'form': form}

        return redirect('profile', pk=pk)


    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'layout/edit_profile.html', args)
