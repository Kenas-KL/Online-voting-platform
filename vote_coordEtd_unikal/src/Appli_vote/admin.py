from django.contrib import admin
from .models import Candidat,Electeur, Election

# Register your models here.

class CandidatAdmin(admin.ModelAdmin):
    model=Candidat 
    list_display=(
        "mat",
        "name",
        "fac",
        "prom",
        'thumbnail',
        "num_candidat",
        "poste",
    )
    list_editable=(
        "poste",
        "num_candidat",
    )


class ElecteurAdmin(admin.ModelAdmin):
    model=Electeur
    list_display = (
        "matricule",
        "nom",
        "fac",
        "prom",
        "voted",
    )

class ElectionAdmin(admin.ModelAdmin):
    model=Election
    list_display = (
        "year",
        "detail",
        "begin",
        "end",
        "enable",
    )
    list_editable=(
        "begin",
        "end",
        'enable',
    )

  

admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidat, CandidatAdmin)
admin.site.register(Electeur, ElecteurAdmin)


