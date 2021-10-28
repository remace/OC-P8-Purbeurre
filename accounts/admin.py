from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

@admin.register(User)
class UserInAdmin(UserAdmin):
    """ User admin model """

    # the forms tu add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    search_fields = ['email', 'first_name','last_name',]
    list_display = ['email', 'first_name', 'last_name', 'is_admin',]
    list_filter = ['is_admin', 'is_active']

    readonly_fields = ['created_at', 'updated_at',]

    fieldsets = (
        (None, {
            'fields':( 'email', 'password', ('first_name', 'last_name'),)}),
            ('Contact', {'fields':('phone',)}),
            ('Permissions', {'fields': ('is_admin', 'is_active')}),
            ('Time', {'fields': ('created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}),
    )

    ordering = ('email',)
    filter_horizontal = ()