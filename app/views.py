from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from app.forms import QuestionRoom, ReplyRoom
from django.contrib import messages
from django.contrib.auth.models import User

from app.models import Category, Question, Reply
from django.db.models import Q

# Create your views here.
def homePage(request):
    categories = Category.objects.all()
    search = False
    if not 'category' in request.GET:
        questions = Question.objects.filter(category=categories[0]).order_by('-created')
    else:
        try:
            cat = Category.objects.get(name=request.GET.get('category', categories[0]))
            questions = Question.objects.filter(category=cat).order_by('-created')
        except:
            questions = False

    context = {'categories':categories}

    if 'q' in request.GET and request.GET.get('q') != "":
        query = request.GET.get('q')
        
        try:
            questions = Question.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created')
            print("worked")
        except:
            questions = False
            search = True
            print("Not")
    
    if questions and search==False:
        pagination = Paginator(questions, 5)
        try:
            page_num = int(request.GET.get('page', 1))
        except:
            page_num = 1
        num_pages = pagination.num_pages
        if page_num > num_pages:
            page_obj = pagination.page(num_pages)
        elif page_num < num_pages:
            page_obj = pagination.page(1)
        else:
            page_obj = pagination.page(page_num)
        context = {'categories':categories, 'questions':page_obj, 'num_pages':num_pages}
    else:
        context = {'categories':categories, 'questions':questions, 'num_pages':False}
    
    return render(request, 'app/home.html', context)

@login_required(login_url='login')
def createQuestion(request):
    categories = Category.objects.all()
    form = QuestionRoom()
    
    if request.method == 'POST':
        form = QuestionRoom(request.POST, request.FILES)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.owner = request.user
            quest.save()
            messages.success(request, 'Savol yuborildi ')
            return redirect('home')
        else:
            messages.error(request, 'Qandaydir xatolik, qaytadan urining.', extra_tags=' alert-danger')
            return redirect('question-room')
    return render(request, 'app/question.html', {'form': form, 'categories': categories})

def singleQuestion(request, pk):
    question = Question.objects.get(id=pk)
    answers = Reply.objects.filter(question=question)
    categories = Category.objects.all()
    reply_form = ReplyRoom()

    if request.user.is_authenticated:
        if request.method == 'POST':
            reply_form = ReplyRoom(request.POST, request.FILES)
            if reply_form.is_valid():
                ans = reply_form.save(commit=False)
                ans.owner = request.user
                ans.question = question
                ans.likes = 0
                ans.save()
                messages.success(request, 'Javob yuborildi')
                return redirect('home')
            else:
                messages.error(request, 'Qandaydir xatolik, qaytadan urining.', extra_tags=' alert-danger')
                return redirect('question-room')
    return render(request, 'app/single-question.html', {'question': question, 'categories': categories, 'answers': answers, 'reply_form': reply_form})