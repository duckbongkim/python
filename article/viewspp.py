from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotAllowed
from .models import Test, Question, Answer
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm,AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    ## create_date가 최근 순서로 model에서 값을 가져와라
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10) # 페이지를 나눠주는 함수
    pagi_obj = paginator.get_page(request.GET.get('page','1'))
    context = {"question_list": pagi_obj}
    return render(request, 'article/question_list.html', context)

def insert(requst):
    for i in range(300):
        q = Question(subject = f'테스트 데이터 : {i}',
                     content = '테스트',
                     create_date = timezone.now())
        q.save()
    return HttpResponse("데이터 입력완료")

def show(request):
    display_all = Test.objects.all()
    result = ""
    for t in display_all:
        result += "<h1>" + t.name + "</h1>" + "<br>"
    return HttpResponse(result)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {"question" : question}
    return render(request, 'article/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('article:detail', question_id = question.id)
    else:
        return HttpResponseNotAllowed('Only Post method using possible')
    context = {'question': question, 'form':form}
    return render(request, 'article/question_detail.html', context)
    
    # question.answer_set.create(content=request.POST.get('content'),
    #                            create_date= timezone.now())
    # return redirect('article:detail', question_id= question.id)


@login_required(login_url='common:login')
def Question_create(request):
    if request.method == 'POST': #요청이 Post 방식인지 확인
        # 요청이 Post 방식인건 "저장하기" 버튼을 눌렀을때만
        form = QuestionForm(request.POST) #Question에 입력값 넣기
        if form.is_valid():# 해당 form의 형식이 맞는지 검사
            #입력받은 subject와 content를 모델에 저장
            #모델에 저장은 하는데 해당 모델의 commit은 하지 않음
            # 아직 create_date라는 속성값이 정의 되지 않았기 때문에
            #commit을 하면 에러가 발생함
            question = form.save(commit=False)
            question.author = request.user 
            # 현재 시작으로 create_date 저장
            question.create_date = timezone.now()
            #model 에서 필요한 모든 값이 저장 되었음으로
            #commit 완료
            question.save()
            ##데이터의 저장이 끝나면 이제 기본 페이지로 이동
            return redirect('article:index')
    else:
        form = QuestionForm()
    return render(request,"article/question_form.html",{'form':form})


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('article:detail', question_id=question.id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST ,instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('article:detail',question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    return render(request,"article/question_form.html",{'form':form})


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한 없습니다')
        return redirect('article:detail', question_id=question.id)
    question.delete()
    return redirect('article:index')







@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('article:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST ,instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('article:detail',question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
        
    return render(request,"article/answer_form.html",{'form':form})


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한 없습니다')
        return redirect('article:detail', question_id=answer.question.id)
    answer.delete()
    return redirect('article:detail', question_id=answer.question.id)

# @login_required(login_url='common:login')
# def question_modify(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     if request.user != question.author:
#         messages.error(request, "수정 권한이 없습니다.")
#         return redirect('article:detail', question_id=question.id)
#     if request.method == 'POST': 
#         form = QuestionForm(request.POST, instance=question) 
#         if form.is_valid(): 
#             question = form.save(commit=False) 
#             question.modify_date = timezone.now()
#             question.save()
#             return redirect('article:detail', question_id = question.id)
#     else:
#         form = QuestionForm(instance=question)
#     return render(request, 'article/question_form.html', {'form': form})





# Create your views here.
