from django.contrib import admin
from .models import House, Reservation, PrivateMsg, Admin, Branch, EstatePersonal, Customer, Profile


# Register your models here.


class HouseAdmin(admin.ModelAdmin):
    list_display = ("name",)


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("house", "pickUpDate", "returnDate", "estate_person")


class PrivateMsgAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "lastname", "mail")


admin.site.register(House, HouseAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(PrivateMsg, PrivateMsgAdmin)
#admin.site.register(CustomUser)
#admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Branch)
admin.site.register(EstatePersonal)
admin.site.register(Customer)
#admin.site.register(CarDealerCustomerSystem)
admin.site.register(Profile)

