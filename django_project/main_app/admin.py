from django.contrib import admin
from .models import (Hotels,
                     HotelsParamsHotels,
                     HotelsParams,
                     RoomsTypes,
                     RoomsTypesHotels,
                     Prices,
                     Places)


admin.site.register(Hotels)
admin.site.register(HotelsParamsHotels)
admin.site.register(HotelsParams)
admin.site.register(RoomsTypes)
admin.site.register(RoomsTypesHotels)
admin.site.register(Prices)
admin.site.register(Places)
