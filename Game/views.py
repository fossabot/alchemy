from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from AlchemyCommon.models import Element, Category, UserProfile
from alchemysite import settings
from .forms import RegisterForm
import json
# Create your views here.


def index(request):
    if request.user.is_authenticated():
        return render(request, 'Game/game.html')
    else:
        return render(request, 'Game/index.html', {"text": "1"})


def activation(request, activationToken):
    userProfile = get_object_or_404(UserProfile, activationToken=activationToken)
    user = userProfile.user
    user.is_active = True
    user.save()
    return render(request, 'Game/activation_success_notify.html')

def registration(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            for el in Element.objects.filter(first_recipe_el=0).filter(second_recipe_el=0):
                user.profile.open_elements.add(el)
            if not settings.EMAIL_CONFIRM:
                user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['pass1'])
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'Game/email_confirm_notify.html')
    else:
        form = RegisterForm()
    return render(request, 'Game/regform.html', {'form': form})


def login_view(request):
	return HttpResponseForbidden() # this page forbidden for awhile
	result = ''
	if request.user.is_authenticated():
		result = 'alreadyLogIn'
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				login(request,user)
				result = 'success'
			else:
				result = 'userNotActive'
		else:
			result = 'wrongPassOrLogin'
	else: 
		return HttpResponseForbidden()
	return HttpResponse(result)


def get_categories(request):
    categories_dict = {"categories": []}
    categories = Category.objects.all()
    for category in categories:
        categories_dict["categories"].append({
            "id": category.id,
            "name": category.name
            })
    return HttpResponse(json.dumps(categories_dict))


def element_list(request, category_id):
    elements_dict = {"elements": []}
    elements = Category.objects.get(pk=category_id).element_set.all()
    for el in elements:
        elements_dict['elements'].append({
            'image': 'qwer.jpg',
            'name': el.name,
            'id': el.id
            })
    return HttpResponse(json.dumps(elements_dict))


def get_user_open_element_list(request, category_id):
	if not request.user.is_authenticated:
		return HttpResponseForbidden()

	category_id = int(category_id)
	openElementsDict = {"elements": []}
	userOpenElements = request.user.profile.open_elements.all()
	for element in userOpenElements:
		if (element.category.id == category_id):
			openElementsDict['elements'].append({
				'id': element.id,
				'name': element.name,
				'image': 'element.image'
				})
	return HttpResponse(json.dumps(openElementsDict))



def check_element(request):
    """
    return json

    {
        'success': bool
        'newElement':{
            'id':
            'name':
            'image':
        }
    }

    """
    if (not request.user.is_authenticated):
        return HttpResponseForbidden()

    if request.method == 'POST':
        result = {'success': False}
        element1 = int(request.POST['first_element'])
        element2 = int(request.POST['second_element'])
        if element1 > element2:
            element1, element2 = element2, element1
        try:
            element1obj = Element.objects.get(pk=element1)
            element2obj = Element.objects.get(pk=element2)
            resultElement = Element.objects.get(first_recipe_el=element1,
                                                second_recipe_el=element2)
        except Element.DoesNotExist:
            return HttpResponse(json.dumps(result))

        userOpenElements = request.user.profile.open_elements

        if element1obj in userOpenElements.all() and element2obj in userOpenElements.all():
            result['success'] = True
            result['newElement'] = {'id': resultElement.id,
                                    'name': resultElement.name,
                                    'image': 'qwe.jpg'}
            userOpenElements.add(resultElement)
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps(result))
    return HttpResponseForbidden()
