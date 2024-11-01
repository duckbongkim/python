from django.shortcuts import render
from django.http import HttpResponseNotAllowed
from ..models import Question, Answer
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..forms import AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



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
            return redirect('{}#answer_{}'.format(resolve_url('article:detail', question_id=question.id), answer.id))
    else:
        return HttpResponseNotAllowed('Only Post method using possible')
    context = {'question': question, 'form':form}
    return render(request, 'article/question_detail.html', context)

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
            # return redirect('article:detail',question_id=answer.question.id)
            return redirect('{}#answer_{}'.format(resolve_url('article:detail', question_id=answer.question.id), answer.id))
            
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


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request,'본인은 추천 못함')
    else:
        answer.voter.add(request.user)
    # return redirect('article:detail',question_id=answer.question.id)
    return redirect('{}#answer_{}'.format(resolve_url('article:detail', question_id=answer.question.id), answer.id))