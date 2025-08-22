from email.policy import default
from django.db import models
from uuid import uuid4

# Create your models here.

class Election(models.Model):
    year = models.CharField(max_length=9)
    detail = models.TextField()
    begin = models.DateTimeField()
    end = models.DateTimeField()
    enable = models.BooleanField(default=True)
    thumbnail = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ['-pk']
        verbose_name="Election"
    def __str__(self) : return self.year

class Candidat(models.Model):
    mat=models.CharField(max_length=255, verbose_name="Matricule",default=uuid4)
    name = models.CharField(max_length=255, verbose_name="Nom",blank=False)
    fac=models.CharField(max_length=255, choices=[
        ("Sciences Informatiques","informatique"),
        ("Sciences Biomédicales","medecine"),
        ("Sciences Juridiques","droit"),
        ("Sciences Sociales","social"),
        ("Sciences Economiques","economie"),
        ("Sciences Agronomiques","agronomie"),
        ("Ecole de Santé Publique","sante"),
        ("Sciences Psychologiques","psycho"),
        ("Sciences de l'Information et de la Communication","sic"),
    
    ], verbose_name="Faculté" )
    prom=models.CharField(choices=[
        ("G1","g1"),
        ("G2","g2"),
        ("G3","g3"),
        ("L1","l1"),
        ("L2","l2"),
        ("Bac+1","bac1"),
        ("Bac+2","bac2"),
        ("Bac+3","bac3"),

        
    ], max_length=255)
    description=models.TextField(blank=True, null=True, default='Aucune description')
    thumbnail = models.ImageField(default='')

    num_candidat=models.IntegerField()
    poste=models.CharField(max_length=255,choices=[
        ("coordo","Coordonnateur des Etudiants"),
        ("vice-cordo","Vice-Coordonnateur des Etudiants"),
        ("sec","Sécretaire de la Coordination"),
        ("tresorier","Trésorier de la Coordination"),
        ("cc","Chargé de Communication de la Coordination")
    ])
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True)


class Electeur(models.Model):
    candidat=models.ManyToManyField(Candidat, null=True, blank=True, related_name='votant')
    matricule=models.CharField(max_length=255)
    nom=models.CharField(max_length=255)
    fac=models.CharField(max_length=255, choices=[
        ("Sciences Informatiques","informatique"),
        ("Sciences Biomédicales","medecine"),
        ("Sciences Juridiques","droit"),
        ("Sciences Sociales","social"),
        ("Sciences Economiques","economie"),
        ("Sciences Agronomiques","agronomie"),
        ("Ecole de Santé Publique","sante"),
        ("Sciences Psychologiques","psycho"),
        ("Sciences de l'Information et de la Communication","sic"),
    
    ], verbose_name="Faculté" )
    prom=models.CharField(choices=[
        ("G1","g1"),
        ("G2","g2"),
        ("G3","g3"),
        ("L1","l1"),
        ("L2","l2"),
        ("Bac+1","bac1"),
        ("Bac+2","bac2"),
        ("Bac+3","bac3"),
    ], max_length=255,verbose_name="Promotion")
    voted=models.BooleanField(default=False)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True)




    

