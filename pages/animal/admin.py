from django.contrib import admin
from pages.animal.models import KindAnimal, KindAnimalAttr, AnimalAttr, KindAnimalAttrVal, Animal, AnimalPhoto


class KindAnimalAttrInline(admin.TabularInline):
    model = KindAnimalAttr
    fields = ('attr',)


class KindAnimalAdmin(admin.ModelAdmin):
    inlines = [KindAnimalAttrInline,]
    fields = ('kind',)
    list_display = ['kind',]
    search_fields = ['kind']


class KindAnimalAttrValAdmin(admin.ModelAdmin):
	fileds = ('attr', 'value',)
	list_display = ['attr', 'value',]


admin.site.register(KindAnimal, KindAnimalAdmin)
admin.site.register(AnimalAttr)
admin.site.register(KindAnimalAttrVal, KindAnimalAttrValAdmin)
admin.site.register(Animal)
admin.site.register(AnimalPhoto)