from django.shortcuts import render, HttpResponseRedirect, reverse
from bugtracker_app.models import MyDev, Bug
from bugtracker_app.forms import LoginForm, AddBugForm, InProgressBugForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from bugtracker.settings import AUTH_USER_MODEL

# Create your views here.


@login_required
def index_view(request):
    bugs = Bug.objects.all()
    return render(request, "index.html", {"headline": "Hello World!", "bugs": bugs})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data.get("username"),
                                password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


@login_required
def add_bug_form_view(request):
    if request.method == "POST":
        form = AddBugForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Bug.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                assigned_by_dev=request.user
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddBugForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def edit_bug_view(request, bug_id):
    edit_bug = Bug.objects.get(id=bug_id)
    if request.method == "POST":
        form = AddBugForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            edit_bug.title = data['title']
            edit_bug.description = data['description']
            edit_bug.save()
        return HttpResponseRedirect(reverse('bug', args=[edit_bug.id]))
    data = {
        'title': edit_bug.title,
        'description': edit_bug.description
    }
    form = AddBugForm(initial=data)
    return render(request, 'generic_form.html', {'form': form})


@login_required
def bug_detail_view(request, bug_id):
    the_bug = Bug.objects.filter(id=bug_id).first()
    return render(request, 'bug_detail.html', {'bug': the_bug})


@login_required
def dev_detail_view(request, dev_id):
    the_dev = MyDev.objects.filter(id=dev_id).first()
    bugs_by = Bug.objects.filter(assigned_by_dev=the_dev.id)
    bugs_assigned = Bug.objects.filter(assigned_to_dev=the_dev.id)
    bugs_completed = Bug.objects.filter(completed_by_dev=the_dev.id)
    return render(request, "dev_detail.html", {"dev": the_dev, "bugs_by": bugs_by, "bugs_assigned": bugs_assigned, "bugs_completed": bugs_completed})


@login_required
def in_progress_view(request, bug_id):
    in_progress = Bug.objects.get(id=bug_id)
    in_progress.completion_status_choice = "IP"
    in_progress.completed_by_dev = None
    if request.method == "POST":
        form = InProgressBugForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            in_progress.assigned_to_dev = data["assigned_to_dev"]
            in_progress.save()
        return HttpResponseRedirect(reverse("bug", args=[in_progress.id]))
    data = {
        "assigned_to_dev": in_progress.assigned_to_dev
    }
    form = InProgressBugForm(initial=data)
    return render(request, "generic_form.html", {"form": form})


@login_required
def completed_view(request, bug_id):
    completed = Bug.objects.get(id=bug_id)
    completed.completion_status_choice = "DO"
    completed.completed_by_dev = completed.assigned_to_dev
    completed.assigned_to_dev = None
    completed.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def invalid_view(request, bug_id):
    invalid = Bug.objects.get(id=bug_id)
    invalid.completion_status_choice = "IN"
    invalid.completed_by_dev = None
    invalid.assigned_to_dev = None
    invalid.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
