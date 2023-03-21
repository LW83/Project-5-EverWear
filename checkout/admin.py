from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """Enables editing of Order line items from Admin"""
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid',)

    fields = ('order_number', 'order_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag'
              'stripe_pid', 'order_status',)

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total', 'order_status',)

    search_fields = ['order_number', 'order_profile', 'date',
                     'full_name', 'email', 'phone_number',
                     'stripe_pid', 'country', 'order_status',]

    list_filter = ('date', 'order_status',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
