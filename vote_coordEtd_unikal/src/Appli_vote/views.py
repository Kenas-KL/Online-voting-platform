from multiprocessing import context
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Candidat,Electeur,Election
from django.db.models import Count
from django.utils import timezone
from pprint import pprint
# Create your views here.
class ElectionView(ListView):
    model = Election
    context_object_name="elections"
    template_name = 'Appli_vote/election.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timenow'] = timezone.now()
        return context



class CandidatesView(ListView):
    model = Candidat
    context_object_name="candidats" 

    def get_queryset(self):
        year=self.kwargs.get('year')
        queryset=Candidat.objects.filter(election=year)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year=self.kwargs.get('year')
        context['coords']=Candidat.objects.filter(election=year, poste='coordo')
        context['vcords']=Candidat.objects.filter(election=year, poste='vice-cordo')
        context['tresoriers']=Candidat.objects.filter(election=year, poste='tresorier')
        context['secretaires']=Candidat.objects.filter(election=year, poste='sec')
        context['cc']=Candidat.objects.filter(election=year, poste='cc')
    
        return context

        
class CandidateDetailVieW(DetailView):
    model= Candidat 
    context_object_name = "candidat"

def voter(request):
    if request.method == "POST":
        try: 
            elec = Electeur.objects.get(matricule=request.POST.get('mat'))
        except:
            return render(request, 'Appli_vote/voter.html', context={"error_mat":True})
        try:
            election = Election.objects.first()
            print(election)
            if elec.voted:
                return render(request, 'Appli_vote/voter.html', context={"voted":True})
            else:
                coordo = Candidat.objects.get(num_candidat=request.POST.get('c'), poste="coordo", election=election)
                vcoordo = Candidat.objects.get(num_candidat=request.POST.get('vc'), poste="vice-cordo", election=election)
                sec = Candidat.objects.get(num_candidat=request.POST.get('s'), poste="sec", election=election) 
                treso = Candidat.objects.get(num_candidat=request.POST.get('t'), poste="tresorier", election=election) 
                cc = Candidat.objects.get(num_candidat=request.POST.get('cc'), poste="cc", election=election) 
            
                elec.candidat.set([coordo.pk,vcoordo.pk,sec.pk,treso.pk,cc.pk]) 
                elec.voted = True
                elec.save()
                return render(
                    request,
                    'Appli_vote/voter.html',
                    context=
                    {
                        'c':coordo,
                        'vc': vcoordo,
                        's': sec,
                        't':treso,
                        'cc':cc,
                        'error':False,
                    } )  

        except:
            return render(request, 'Appli_vote/voter.html', context={"error_num":True}) 
    return render(request, "Appli_vote/candidat_list.html")

def resultat (request, pk):
    if pk == 0 :
        election = Election.objects.first()
    else:
        election = Election.objects.get(pk=pk)
    datas= {
        'year' : election.year, 
        'electeurs' : Electeur.objects.filter(election=election).count(),
        'candidats' : Candidat.objects.filter(election=election).annotate(nb_votes=Count('votant')).order_by('-nb_votes'),
        'part_num': Electeur.objects.filter(election=election, voted=True).annotate(n_elects=(Count('candidat',distinct=True))).count()
    }

    return render(request, 'Appli_vote/resultat.html', context=datas)

def home(request):
    return render(request, 'Appli_vote/home.html') 

class ElectionDetail(DetailView):
    model = Election
    context_object_name = 'election'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timenow'] = timezone.now()
        return context


class CandidatesLast(ListView):
    model = Candidat
    context_object_name = "candidats"
    template_name = "Appli_vote/candidat_list.html"

    
    def get_context_data(self, **kwargs):
        last_election = Election.objects.first()
        context = super().get_context_data(**kwargs)
        context['coords']=Candidat.objects.filter(election=last_election, poste='coordo')
        context['vcords']=Candidat.objects.filter(election=last_election, poste='vice-cordo')
        context['tresoriers']=Candidat.objects.filter(election=last_election, poste='tresorier')
        context['secretaires']=Candidat.objects.filter(election=last_election, poste='sec')
        context['cc']=Candidat.objects.filter(election=last_election, poste='cc')
        context['no_vote'] = True

        if last_election:
            time_begin = last_election.begin
            time_end = last_election.end
            now = timezone.now()

            if now < time_begin:
                context['status'] = 'before'
            elif time_begin <= now <= time_end:
                context['status'] = 'in_'
            else: 
                context['status'] = 'after'
        else:
            context['status'] = 'not'

        return context


def publish(request, pk):
    election = Election.objects.get(pk=pk)
  
    datas = {
        'part_num': Electeur.objects.filter(election=election, voted=True).annotate(n_elects=(Count('candidat',distinct=True))).count(),
        'time' : election.end,
        'part_num': Electeur.objects.filter(election=election, voted=True).annotate(n_elects=(Count('candidat',distinct=True))).count(),
        'coord' : Candidat.objects.filter(election=election, poste="coordo").annotate(nb_votes=Count('votant')).first(),
        'vcoord' : Candidat.objects.filter(election=election, poste="vice-cordo").annotate(nb_votes=Count('votant')).first(),
        'sec' : Candidat.objects.filter(election=election, poste="sec").annotate(nb_votes=Count('votant')).first(),
        'tres' : Candidat.objects.filter(election=election, poste="tresorier").annotate(nb_votes=Count('votant')).first(),
        'cc' : Candidat.objects.filter(election=election, poste="cc").annotate(nb_votes=Count('votant')).first(),
    }

    for candidat in Candidat.objects.filter(election=election).annotate(nb_votes=Count('votant')):
        if candidat.nb_votes > datas['coord'].nb_votes and candidat.poste == 'coordo' :
            datas['coord'] = candidat
        if candidat.nb_votes > datas['vcoord'].nb_votes and candidat.poste == 'vice-cordo' :
            datas['vcoord'] = candidat
        if candidat.nb_votes > datas['sec'].nb_votes and candidat.poste == 'sec' :
            datas['sec'] = candidat
        if candidat.nb_votes > datas['tres'].nb_votes and candidat.poste == 'tresorier' :
            datas['tres'] = candidat
        if candidat.nb_votes > datas['cc'].nb_votes and candidat.poste == 'cc' :
            datas['cc'] = candidat

    return render(request, 'Appli_vote/publish.html', context=datas)


