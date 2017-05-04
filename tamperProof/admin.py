from django.contrib import admin
from .models import System, Node, FileMd5

# Register your models here.
admin.site.register(System)
admin.site.register(Node)
admin.site.register(FileMd5)
