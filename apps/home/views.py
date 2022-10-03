from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Module



def module_access(request, module: str) -> bool:
    if request.user.groups.first().access_level >= Module.objects.get(name=module).access_level:
        return True
    return False


@login_required(login_url="/login/")
def dashboard(request):
    if not module_access(request, 'Dashboard'):
        return redirect('/login/')
    return render(request, 'modules/calendar.html', context=context)



@login_required(login_url="/login/")
def calendar(request):
    if not module_access(request, 'Calendar'):
        return redirect('/login/')
    context = {}
    return render(request, 'modules/calendar.html', context=context)


@login_required(login_url="/login/")
def charts(request):
    if not module_access(request, 'Charts'):
        return redirect('/login/')
    context = {}
    return render(request, 'modules/charts.html', context=context)



# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))
