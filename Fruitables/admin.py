from django.contrib import admin
from.models import User,Product,Category,Order,ShippingAddress,Contact,Wishlist

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display =('name','slug')
    prepopulated_fields = {"slug": ["name",]}
    search_fields = ['name']

admin.site.register(User)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Product)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Contact)
admin.site.register(Wishlist)




