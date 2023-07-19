from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    
    ordering = ['name']
    list_display = ['email', 'name', 'slug']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name','is_doctor','is_patient','is_organization_user')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',                          
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_doctor',
                'is_patient',
                'is_organization_user',                            

            ),
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.OrganizationUser)
admin.site.register(models.Doctor)
admin.site.register(models.Patient)
admin.site.register(models.Appointment)
admin.site.register(models.Medicine)
admin.site.register(models.Prescription)
admin.site.register(models.DoctorFollow)
admin.site.register(models.PatientFollow)
admin.site.register(models.Blog)