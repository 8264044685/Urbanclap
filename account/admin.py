from django.contrib import admin
from account.models import UserProfile,Services,Comment,ServiceRequest
# from account.forms import UserProfileForm


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username','email','user_type')
    # form = UserProfileForm
    # class Meta:
    #     model = UserProfile
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Services)
admin.site.register(ServiceRequest)
admin.site.register(Comment)
