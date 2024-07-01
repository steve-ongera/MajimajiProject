from django.contrib import admin
from .models import *

admin.site.register(Month)
admin.site.register(Profile)
admin.site.register(Payment_Year)
admin.site.register(House)
admin.site.register(Tenant)
admin.site.register(tenants_database)
admin.site.register(MonthlySignOff)
admin.site.register(Payment)
admin.site.register(MaintenanceRequest)


admin.site.site_header='MAJI ONLINE SYSTEM'
admin.site.site_title='majimaji | application'
admin.site.index_title='Welcome to MajiOnline App developed by steve Ongera'
