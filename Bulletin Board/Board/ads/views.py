from django.shortcuts import render, redirect, get_object_or_404
from .forms import AnnouncementForm, ResponseForm, NewsForm
from .models import Announcement, Response, News
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

@login_required
def create_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user
            announcement.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'ads/announcement_form.html', {'form': form})

def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'ads/announcement_form.html', {'form': form})

def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'ads/announcement_list.html', {'announcements': announcements})
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        announcement.delete()
        messages.success(request, 'Объявление успешно удалено.')
        return redirect('announcement_list')
    return render(request, 'ads/announcement_confirm_delete.html', {'announcement': announcement})

@login_required
def respond_to_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.announcement = announcement
            response.user = request.user
            response.save()


            send_mail(
                subject='Новый отклик на ваше объявление',
                message=f'Пользователь {request.user.username} откликнулся на ваше объявление "{announcement.title}".',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[announcement.user.email],
            )


            send_mail(
                subject='Ваш отклик отправлен',
                message=f'Ваш отклик на объявление "{announcement.title}" был успешно отправлен.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
            )

            return redirect('announcement_list')
    else:
        form = ResponseForm()
    return render(request, 'ads/response_form.html', {'form': form, 'announcement': announcement})

@login_required
def user_responses(request):
    announcements = Announcement.objects.filter(user=request.user)
    responses = Response.objects.filter(announcement__in=announcements)

    return render(request, 'ads/user_responses.html', {
        'responses': responses,
    })
@login_required
def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk, user=request.user)
    if request.method == "POST":
        response.delete()
        messages.success(request, 'Отклик успешно удален.')
        return redirect('user_responses')
    return render(request, 'ads/response_confirm_delete.html', {'response': response})

@login_required
def user_responses(request):
    announcements = Announcement.objects.filter(user=request.user)
    responses = Response.objects.filter(announcement__in=announcements)


    announcement_id = request.GET.get('announcement_id')
    if announcement_id:
        responses = responses.filter(announcement_id=announcement_id)

    return render(request, 'ads/user_responses.html', {
        'responses': responses,
        'announcements': announcements,

    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()

            users = User.objects.all()
            for user in users:
                send_mail(
                    subject=news.title,
                    message=news.content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )
            messages.success(request, 'Новость успешно создана и отправлена всем пользователям.')
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'ads/create_news.html', {'form': form})

def news_list(request):
    news = News.objects.all()
    return render(request, 'ads/news_list.html', {'news': news})


def home(request):
    return render(request, 'ads/home.html')

