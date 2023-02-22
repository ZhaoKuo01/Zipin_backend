from django.contrib import admin
from .models import Note, Userinfo,Maincomn,Subcomn,MyCollection,MyLike

# Register your models here.
admin.site.register(Note)
admin.site.register(Userinfo)
admin.site.register(Maincomn)
admin.site.register(Subcomn)
admin.site.register(MyCollection)
admin.site.register(MyLike)