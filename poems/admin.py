from django.contrib import admin
from .models import Topic, Poem

# Register your models here.
class PoemAdmin(admin.ModelAdmin):
    readonly_fields = ('id','published_at','updated_at',)

admin.site.register(Poem, PoemAdmin)
admin.site.register(Topic)