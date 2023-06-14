from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,"main/login.html")

def signup(request):
    return 