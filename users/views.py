from django.http import HttpResponse
from django.shortcuts import redirect, render
from app.models import Category, Question, Reply
from users.forms import profileForm
from users.models import Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def loginPage(request):
    if request.user.is_authenticated==False:
        categories = Category.objects.all()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Muvaffaqiyatli avtorizatsiya')
                return redirect('home')
            else:
                messages.error(request, 'Qaytadan urining !', extra_tags=' alert-danger')
                return redirect('login')  
        return render(request, 'users/login.html', {'categories': categories})
    else:
        return redirect('profile')

def logoutPage(request):
    logout(request)
    messages.success(request, 'Kabinetdan chiqildi')
    return redirect('home')

@login_required(login_url='login')
def profilePage(request):
    categories = Category.objects.all()
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = Profile.objects.create(
            user=request.user
        )
    rating = Reply.objects.filter(owner=request.user).count()
    return render(request, 'users/profile.html', {'categories': categories, 'profile':profile, 'rating':rating})

@login_required(login_url='login')
def editProfilePage(request):
    categories = Category.objects.all()
    
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = Profile.objects.create(
            user=request.user
        )
    form = profileForm(instance=profile)

    if request.method == "POST":
        form = profileForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumotlar yangilandi")
            return redirect('profile')
        else:
            messages.error(request,'Qaytadan urining', extra_tags=' alert-danger')
    return render(request, 'users/edit-profile.html', {'categories': categories, 'profile':profile, 'form': form})


@login_required(login_url='login')
def editPersonal(request):
    categories = Category.objects.all()
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = Profile.objects.create(
            user=request.user
        )

    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        username = request.POST.get('username')
        password = request.POST.get('password')
        repass = request.POST.get('re-pass')
        newpass = request.POST.get('new-pass')
        if password == repass and request.user.check_password(password):
            if username != request.user.username:
                filterusername = User.objects.filter(username=username)
                if filterusername:
                    messages.error(request, 'Login oldin olib bo\'lingan', extra_tags=' alert-error')
                    return redirect('edit-personal')
                else:
                    user.username = username
                    user.set_password(newpass)
                    user.save()
                    messages.success(request,'Ma\'lumotlar yangilandi')
            else:
                user.set_password(newpass)
                user.save()
                messages.success(request,'Ma\'lumotlar yangilandi')
        else:
            messages.error(request, 'Parollar bir xil emas yoki noto\'g\'ri ', extra_tags=' alert-error')
            return redirect('edit-personal')


    return render(request, 'users/edit-personal.html', {'categories': categories, 'profile':profile})



def registrationPage(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repass = request.POST.get('re-password')

        if password == repass:
            filterusername = User.objects.filter(username=username)
            if filterusername:
                messages.error(request, 'Login oldin olib bo\'lingan', extra_tags=' alert-error')
                return redirect('registration')
            else:
                nuser = User.objects.create_user(username=username,password=password)
                nuser.save()
                messages.success(request,'Muvaffaqiyatli avtorizatsiya')
                return redirect("login")

        else:
            messages.error(request, 'Parollar bir xil emas', extra_tags=' alert-error')
            return redirect('registration')
    return render(request, 'users/registration.html', {'categories': categories})


@login_required(login_url='login')
def questionsPage(request):
    categories = Category.objects.all()
    questions = Question.objects.filter(owner=request.user).order_by('-created')
    return render(request, 'users/questions.html', {'categories':categories, 'questions':questions})


@login_required(login_url='login')
def answersPage(request):
    categories = Category.objects.all()
    questions = Reply.objects.filter(owner=request.user).order_by('-created')
    
    return render(request, 'users/questions.html', {'categories':categories, 'questions':questions, 'answer':True})


def userPage(request, username):
    try:
        categories = Category.objects.all()
        pf_user = User.objects.get(username=username)
        profile = Profile.objects.get(user=pf_user)
        rating = Reply.objects.filter(owner=pf_user).count()
        return render(request, 'users/user.html', {'categories':categories, 'profile':profile, 'rating':rating})
    except:
        return HttpResponse("<h1>Not found")