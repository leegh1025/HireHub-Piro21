from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt

from .models import Application, Answer, Possible_date_list, Comment, individualQuestion, individualAnswer, Interviewer
from accounts.models import Interviewer
from template.models import ApplicationTemplate, ApplicationQuestion, InterviewTemplate, InterviewQuestion
from .forms import ApplicationForm, CommentForm, QuestionForm, AnswerForm

def interview(request):
    applicants = Application.objects.all()
    ctx = {"applicants": applicants}
    return render(request, "applicant/interview.html", ctx)

def document(request):
    applicants = Application.objects.all()
    ctx = {"applicants": applicants}
    return render(request, "applicant/document.html", ctx)

def search_applicant(request):
    search_txt = request.GET.get('search_txt')
    applicants = Application.objects.filter(name__icontains=search_txt)
    results = [{'id': applicant.id, 'name': applicant.name} for applicant in applicants]
    return JsonResponse(results, safe=False)

def profile(request, pk):
    applicant = get_object_or_404(Application, pk=pk)
    answers = Answer.objects.filter(application=applicant)
    ctx = {
        'applicant': applicant,
        'answers': answers,
    }
    return render(request, 'applicant/profile.html', ctx)

def schedule(request):
    applicants = Application.objects.filter(~Q(status ='submitted'))
    schedules = Possible_date_list.objects.all()

    ctx = {"applicants": applicants, "schedules":schedules}
    return render(request, 'applicant/schedule.html', ctx)

def auto_schedule(request):
    schedules = Possible_date_list.objects.all()

    # 스케줄 정보 리스트
    schedules_info = [[schedule.id, 0, schedule.max_possible_interview] for schedule in schedules]

    # 이미 배치된 인원 가능 인터뷰수에서 빼기
    scheduled_applicants = Application.objects.filter(interview_date__isnull=False)
    for scheduled_applicant in scheduled_applicants:
        for schedule_info in schedules_info:
            if schedule_info[0] == scheduled_applicant.interview_date.id:
                schedule_info[2] -= 1

    # 배치 가능 인터뷰 수 0 이하면 해당 스케줄 삭제
    for schedule_info in schedules_info:
        if schedule_info[2] <=0:
            schedules_info.remove(schedule_info)

    # 지원자 정보 리스트
    applicants = Application.objects.filter(interview_date__isnull=True)
    applicants_info = [[applicant.id, list(applicant.possible_date.all())] for applicant in applicants]

    # 스케줄 짜기 알고리즘
    while schedules_info:
        # 스케줄링 필요 인원 없으면 break
        if len(applicants) == 0:
            break

        # 삭제할 인원 인덱스 리스트
        del_applicant_index = []

        # 가능 시간대 0개 or 1개 인원 배치, 인기도 갱신
        for num in range(len(applicants_info)):
            # 0개
            if len(applicants_info[num][1]) == 0:
                del_applicant_index.append(num)
            # 1개
            elif len(applicants_info[num][1]) == 1:
                applicant = Application.objects.get(id=applicants_info[num][0])
                for schedule_info in schedules_info:
                    if schedule_info[0] == applicants_info[num][1][0].id:
                        if schedule_info[2] > 0:
                            applicant.interview_date = applicants_info[num][1][0]
                            applicant.save()
                            schedule_info[2] -= 1
                            break
                        else:
                            break

                del_applicant_index.append(num)
            # 인기도 갱신
            else:
                for possible_date in applicants_info[num][1]:
                    for schedule_info in schedules_info:
                        if schedule_info[0] == possible_date.id:
                            schedule_info[1] += 1
    
        # 배치 안되거나 배치한 애들 목록에서 삭제
        for index in sorted(del_applicant_index, reverse=True):
            del applicants_info[index]
        
        del_applicant_index = []    
        # 인기도 - 남는자리수 작은 시간대 추출
        popularity = 1000000
        low_pop_schedule = []
        for schedule_info in schedules_info:
            my_popularity = schedule_info[1] - schedule_info[2]
            if popularity > my_popularity:
                popularity = my_popularity
                low_pop_schedule = schedule_info

        # 인기도 - 남는자리수 낮은 시간대 배치
        for num in range(len(applicants_info)):
            for possible_date in applicants_info[num][1]:
                if possible_date.id == low_pop_schedule[0]:
                    if low_pop_schedule[2] > 0:
                        applicant = Application.objects.get(id=applicants_info[num][0])
                        applicant.interview_date = possible_date
                        applicant.save()
                        del_applicant_index.append(num)
                        low_pop_schedule[2] -=1
                    applicants_info[num][1].remove(possible_date)

        # 배치된 인원 및 시간대 삭제
        for index in sorted(del_applicant_index, reverse=True):
            del applicants_info[index]
        del_applicant_index = []

        schedules_info.remove(low_pop_schedule)
                    
    return redirect('applicants:schedule')

def apply(request, pk):
    template = ApplicationTemplate.objects.get(id=pk)

    if request.method == 'POST':
        application = Application(
            template = template,
            name = request.POST['name'],
            phone_number = request.POST['phone_number'],
            school = request.POST['school'],
            major = request.POST['major'],
        )
        application.save()

        for question in template.questions.all():
            answer_text = request.POST.get(f'answer_{question.id}')
            Answer.objects.create(
                application = application,
                question = question,
                answer_text = answer_text
            )
        return redirect('accounts:initialApplicant')
        
    context = {
        'template': template,
    }
    return render(request, 'for_applicant/write_apply.html', context)

def comment(request, pk):
    applicant = get_object_or_404(Application, pk=pk)
    answers = Answer.objects.filter(application=applicant)
    comments = Comment.objects.filter(application=applicant).order_by('created_at')
    form = CommentForm()
    
    if request.method == 'POST':
        interviewer = get_object_or_404(Interviewer, email=request.user.email)  # 인터뷰어 객체 가져오기
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.application = applicant
            comment.interviewer = interviewer
            comment.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX 요청 확인
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'text': comment.text,
                        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'interviewer': interviewer.email  # 인터뷰어 이메일 반환
                    }
                })
            else:
                return redirect('applicants:comment', pk=pk)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX 요청 확인
                return JsonResponse({'success': False, 'error': 'Invalid form submission', 'form_errors': form.errors.as_json()})
    
    ctx = {
        'applicant': applicant,
        'answers': answers,
        'comments': comments,
        'form': form,
    }
    return render(request, 'applicant/comments.html', ctx)


def question(request, pk):
    applicant = get_object_or_404(Application, pk=pk)
    answers = Answer.objects.filter(application=applicant)
    questions = individualQuestion.objects.filter(application=applicant).order_by('created_at')
    question_form = QuestionForm()
    answer_form = AnswerForm()

    # 공통 질문 템플릿 및 질문 가져오기
    common_template = InterviewTemplate.objects.first()  # 첫 번째 템플릿을 사용합니다. 필요에 따라 변경 가능
    common_questions = InterviewQuestion.objects.filter(template=common_template)


    if request.method == 'POST':
        if 'question_submit' in request.POST:
            interviewer = get_object_or_404(Interviewer, email=request.user.email)
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.application = applicant
                question.interviewer = interviewer
                question.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'question': {
                            'text': question.text,
                            'created_at': question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            'interviewer': interviewer.email
                        }
                    })
                else:
                    return redirect('applicants:question', pk=pk)
        elif 'answer_submit' in request.POST:
            interviewer = get_object_or_404(Interviewer, email=request.user.email)
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                answer = answer_form.save(commit=False)
                answer.application = applicant
                answer.interviewer = interviewer
                answer.question_id = request.POST.get('question_id')
                answer.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'answer': {
                            'text': answer.text,
                            'created_at': answer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            'interviewer': interviewer.email
                        }
                    })
                else:
                    return redirect('applicants:question', pk=pk)

    ctx = {
        'applicant': applicant,
        'answers': answers,
        'questions': questions,
        'question_form': question_form,
        'answer_form': answer_form,
        'common_questions': common_questions
    }
    return render(request, 'applicant/questions.html', ctx)
