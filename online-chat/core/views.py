from django.shortcuts import render




from account.models import User




def index(request):
    #test
    superusers = User.objects.filter(is_superuser=True)
    return render(request, 'core/index.html',{
        'superusers': superusers,
    })


def about(request):
    return render(request, 'core/about.html')