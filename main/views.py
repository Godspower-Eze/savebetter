from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from .forms import UserCreationForm, UserLogin
from .serializers import SignatureGeneratorSerializer
from .utils import signature_generator, compare_hashes

User = get_user_model()

@login_required
def home_page(request):
    context = {
        "user":request.user
    }
    return render(request, 'index.html', context)

@login_required
def funding(request):
    context = {
        "user" : request.user
    }
    return render(request, 'funding.html')

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home_page')

    form = UserLogin()

    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home_page')
    context = {
        "form": form,
        "title": "Login - SaveBetter"
    }
    return render(request, 'login.html', context)


def register_view(request):
    
    if request.user.is_authenticated:
        return redirect('home_page')

    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, 'Account created successfully. You can now login!')
            return redirect('login_view')
    context = {
        "form": form,
        "title": "Register - SaveBetter"
    }
    return render(request, 'register.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("login_view")


class SignatureGenerator(generics.CreateAPIView):
    
    serializer_class = SignatureGeneratorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        user_id = serializer.data['user_id']
        reference = serializer.data['reference']
        amount_in_kobo = serializer.data['amount_in_kobo']

        signature = signature_generator(user_id, reference, amount_in_kobo)

        data = {
            "signature": signature
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@csrf_exempt
@require_POST
def webhook_reciever(request):
    if compare_hashes(request) == True:
        body = request.POST
        json_body = json.dumps(body)
        status = json_body['data']['status']
        if status == "Completed":
            users = User.objects.filter(username=json_body['data']['userId'])
            if user.exists():
                user = users[0]
                profile = user.profile
                profile.balance = profile.balance + int(json_body['data']['amount'])
                profile.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)
