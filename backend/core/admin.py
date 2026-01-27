from django.contrib import admin
from .models import Department, Employee, SafetyWalk, Observation, Area, Reaction



admin.site.register(Department)
admin.site.register(Employee)


class ObservationInline(admin.TabularInline):
    model = Observation
    extra = 1  # ile pustych wierszy ma pokazać


@admin.register(SafetyWalk)
class SafetyWalkAdmin(admin.ModelAdmin):
    list_display = ("number", "date", "shift", "area", "performed_by")
    list_filter = ("date", "shift", "area")
    search_fields = ("number", "area", "performed_by__username")
    inlines = [ObservationInline]

    # 1) USER widzi tylko swoje
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff or request.user.is_superuser:
            return qs
        return qs.filter(performed_by=request.user)

    # 2) USER nie może zmienić performed_by
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff or request.user.is_superuser:
            return ()
        return ("performed_by",)

    # 3) Przy tworzeniu zawsze ustawiamy performed_by na zalogowanego (dla USER)
    def save_model(self, request, obj, form, change):
        if not change and not (request.user.is_staff or request.user.is_superuser):
            obj.performed_by = request.user
        super().save_model(request, obj, form, change)
    #Żeby pole w ogóle zniknęło dla USER (ładniej)    
    def get_fields(self, request, obj=None):
        fields = ["number", "date", "shift", "area", "performed_by"]
        if request.user.is_staff or request.user.is_superuser:
            return fields
        # USER: bez performed_by (i tak ustawiamy automatycznie)
        return ["number", "date", "shift", "area"]



@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ("id", "safety_walk", "employee", "ppe", "work", "environment")
    list_filter = ("ppe", "work", "environment")
    search_fields = ("comment", "reaction", "employee__employee_no", "employee__last_name")

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
