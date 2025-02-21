from django.contrib import admin
from .models import DonationRequest, Donation



@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'beneficiary', 'target_amount', 'collected_amount', 'status', 'deadline')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description', 'beneficiary__email')
    readonly_fields = ('collected_amount',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'donation_request', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('donor__email', 'donation_request__title')


