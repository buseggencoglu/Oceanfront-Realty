from django.contrib.auth.models import AnonymousUser

from oceanf.models import Customer, EstatePersonal, Notifications


def user_type(request):
    user = request.user
    if not user.is_anonymous:
        customers = Customer.objects.filter(user=user)
        car_dealers = EstatePersonal.objects.filter(user=user)
        notifications = Notifications.objects.filter(user=user)
        user_type = 'admin'
        if len(customers) > 0:
            user_type = 'customer'
        elif len(car_dealers) > 0:
            user_type= 'estate_person'
        return {
            'user': user,
            'user_type': user_type,
            'notifications': notifications
        }
    return {}
