from django.shortcuts import render
from pockemongo.models import Pokemon


def pockmon_list(request):
    qs = Pokemon.objects.all()
    return render(request, 'pockemongo/pockmon_list.html', {
        'pokemon_list': qs,
    })
