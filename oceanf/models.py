from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

TYPE = [
    (0, 'apartment'),
    (1, 'villa'),
    (2, 'studio')
]
ROOMS = [
    (0, '1+0'),
    (1, '1+1'),
    (2, '2+1'),
    (3, '3+1'),
    (4, '4+1'),
    (5, '5+2'),
]
STATUS = [
    (1, 'Available'),
    (0, 'UnAvailable'),
]


class Branch(models.Model):
    branch_name = models.CharField(max_length=100, default="")
    branch_location = models.TextField()

    @classmethod
    def get_by_branch_name(cls, branch_name):
        return cls.objects.filter(branch_name__contains=branch_name)

    def __str__(self):
        return self.branch_name


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class EstatePersonal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, null=True, on_delete=models.CASCADE)
    rate = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthDate = models.DateField(default=datetime.now())

    @classmethod
    def get_customer_by_user(cls, user):
        return cls.objects.filter(user=user)[0]


class House(models.Model):
    image = models.ImageField(upload_to='house_images', null=True, blank=True, default='images/default')
    name = models.CharField(max_length=100, default="")
    branch = models.ForeignKey(Branch, null=True, on_delete=models.SET_NULL)
    type = models.IntegerField(choices=TYPE)
    rooms = models.IntegerField(choices=ROOMS)
    status = models.IntegerField(choices=STATUS, default=1)
    price = models.IntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'house'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return "/house/%s/" % (self.pk)

    @classmethod
    def view_house_list(cls):
        return cls.objects.values('id', 'model', 'status')

    @classmethod
    def view_house_detail(cls, house_id):
        return cls.objects.get(id=house_id)

    @classmethod
    def search_for_house(cls, busy_house, branch_name):
        return cls.objects\
            .filter(branch__branch_name=branch_name, status=1)\
            .exclude(id__in=busy_house)


class PrivateMsg(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()


class Reservation(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE)
    customer_name = models.CharField(default='', blank=True, null=True, max_length=36)
    estate_person = models.ForeignKey(EstatePersonal, blank=True, null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    pickUpDate = models.DateTimeField()
    returnDate = models.DateTimeField()
    paymentStatus = models.BooleanField(default=False)
    total_price = models.FloatField(default=0.0)

    def get_absolute_url(self):
        return "/house/detail/%s/" % (self.pk)

    @classmethod
    def view_users_history(cls, customerID):
        return cls.objects.filter(customerID=customerID).values('house__name', 'pickUpDate', 'returnDate', 'customer_name')

    @classmethod
    def busy_houses(cls, start_date_date, end_date_date):
        return cls.objects.filter(Q(pickUpDate__date__range=[start_date_date, end_date_date]) |
                                  Q(pickUpDate__date__lte=start_date_date,
                                    returnDate__date__gte=end_date_date))\
                          .values('house__id')

    def __str__(self):
        return f'Reservation of {self.house} on {self.pickUpDate.date()}-{self.returnDate.date()}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Notifications(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
