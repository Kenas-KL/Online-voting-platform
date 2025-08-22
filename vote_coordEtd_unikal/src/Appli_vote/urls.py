from django.urls import path 
from .views import CandidateDetailVieW, CandidatesView, resultat,voter, ElectionView, home, ElectionDetail,CandidatesLast, publish

app_name = 'Appli_vote'

urlpatterns = [
    path('', home, name='accueil'),
    path('election', ElectionView.as_view(), name="election"),
    path('candidats/<int:year>/', CandidatesView.as_view(), name='candidats'),
    path('cands/', CandidatesLast.as_view(), name="cands_last"),
    path('detail-candidate/<int:pk>/',CandidateDetailVieW.as_view(),name='detail'),
    path ('cands/voter/',voter,name="voter"),
    path('election-detail/<int:pk>/', ElectionDetail.as_view(), name='election_detail'),
    path('resultat/<int:pk>/',resultat,name="resultat"),   
    path('publish/<int:pk>/', publish, name='publish'),
]

