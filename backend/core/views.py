from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from django.db import transaction
from django.contrib import messages
from .forms import SafetyWalkForm, ObservationForm
from .models import SafetyWalk, Employee, Observation
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
@login_required
def safetywalk_create(request):
    if request.method == "POST":
        sw_form = SafetyWalkForm(request.POST)
        obs_form = ObservationForm(request.POST)

        if sw_form.is_valid() and obs_form.is_valid():
            employee = Employee.objects.filter(user=request.user).first()
            if not employee:
                messages.error(
                    request,
                    "Brak przypisanego Employee do tego konta. Podepnij usera w adminie.",
                )
                return render(
                    request,
                    "core/safetywalk_form.html",
                    {"form": sw_form, "obs_form": obs_form},
                )

            with transaction.atomic():
                sw = sw_form.save(commit=False)
                sw.performed_by = request.user
                sw.save()

                obs = obs_form.save(commit=False)
                obs.safety_walk = sw
                obs.employee = employee
                obs.save()

            messages.success(request, "Raport zostal wyslany.")
            return redirect("safetywalk_list")

    else:
        sw_form = SafetyWalkForm()
        obs_form = ObservationForm()

    return render(
        request,
        "core/safetywalk_form.html",
        {"form": sw_form, "obs_form": obs_form},
    )

def home(request):
    return redirect("safetywalk_list")

@login_required
def safetywalk_list(request):
    qs = SafetyWalk.objects.filter(
        performed_by=request.user
    ).order_by("-date", "-id")

    return render(
        request,
        "core/safetywalk_list.html",
        {"safetywalks": qs},
    )

@login_required
def safetywalk_detail(request, pk):
    safetywalk = get_object_or_404(
        SafetyWalk,
        pk=pk,
        performed_by=request.user,
    )
    return render(request, "core/safetywalk_detail.html", {"safetywalk": safetywalk})


def logout_view(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany.")
    return redirect("login")



class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, "Błędny login lub hasło.")
        return super().form_invalid(form)