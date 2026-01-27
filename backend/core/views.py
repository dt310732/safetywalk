from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from django.db import transaction
from django.contrib import messages
from .forms import SafetyWalkForm, ObservationFormSet
from .models import SafetyWalk
from .models import Employee  # jesli potrzebujesz lookupu
@login_required
def safetywalk_create(request):
    if request.method == "POST":
        form = SafetyWalkForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                sw = form.save(commit=False)
                sw.performed_by = request.user
                sw.save()

                # TERAZ dopiero budujemy formset pod zapisany SafetyWalk
                formset = ObservationFormSet(request.POST, instance=sw)

                if formset.is_valid():
                    # wymaganie: co najmniej jedna obserwacja
                    valid_forms = [
                        f for f in formset.forms
                        if f.cleaned_data and not f.cleaned_data.get("DELETE", False)
                    ]
                    if len(valid_forms) == 0:
                        formset._non_form_errors = formset.error_class(
                            ["Dodaj przynajmniej jedna obserwacje."]
                        )
                        return render(
                            request,
                            "core/safetywalk_form.html",
                            {"form": form, "formset": formset},
                        )

                    # ustawiamy employee automatycznie
                    observations = formset.save(commit=False)
                    employee = Employee.objects.filter(user=request.user).first()
                    if not employee:
                        formset._non_form_errors = formset.error_class(
                            ["Brak przypisanego Employee do tego konta. Podepnij usera w adminie."]
                        )
                        return render(
                            request,
                            "core/safetywalk_form.html",
                            {"form": form, "formset": formset},
                        )
                    for obs in observations:
                        obs.employee = employee
                        obs.save()

                    # usun zaznaczone obserwacje (DELETE)
                    for obj in formset.deleted_objects:
                        obj.delete()

                    messages.success(request, "Raport zostal wyslany.")
                    return redirect("safetywalk_list")

        # jak form niewazny albo formset niewazny, trzeba wyrenderowac oba
        formset = ObservationFormSet(request.POST)

    else:
        form = SafetyWalkForm()
        formset = ObservationFormSet()

    return render(
        request,
        "core/safetywalk_form.html",
        {"form": form, "formset": formset},
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
        performed_by=request.user,  # user widzi tylko swoje
    )

    return render(
        request,
        "core/safetywalk_detail.html",
        {"safetywalk": safetywalk},
    )