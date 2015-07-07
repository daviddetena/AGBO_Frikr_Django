from django.contrib import admin
from photos.models import Photo

class PhotoAdmin(admin.ModelAdmin):
    """

    """
    list_display = ('name', 'owner_name', 'licence', 'visibility')   # campos que se muestran
    list_filter = ('licence', 'visibility')                     # campos de filtro
    search_fields = ('name', 'description')                     # habilita campo busqueda por esos campos

    def owner_name(self, obj):
        """
        Metodo con el que defino que quiero que se muestre nombre y apellido para el owner
        del list_display anterior
        :param obj:
        :return:
        """
        return obj.owner.first_name + u' ' + obj.owner.last_name

    # header para la columna owner_name, y defino tambien el campo por el que se puede ordenar
    owner_name.short_description = u'Photo owner'
    owner_name.admin_order_field = 'owner'

    # defininmos vista detalle de photo en el admin, utilizando fieldsets
    fieldsets = (
        (None, {
            'fields': ('name',),
            'classes': ('wide',)
        }),
        ('Description & author', {
            'fields': ('description', 'owner'),
            'classes': ('wide',)
        }),
        ('Extra', {
            'fields': ('url', 'licence', 'visibility'),
            'classes': ('wide', 'collapse')
        })
    )



# Registramos modelo Photo en el administrador
# El modelo lo maneja la clase PhotoAdmin de arriba
admin.site.register(Photo, PhotoAdmin)
