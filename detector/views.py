from django.shortcuts import render, redirect
from .forms import FormOne, FormTwo
from .utils import form1_score, form2_score
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone

@login_required
def form1_view(request):
    form = FormOne(request.POST or None)

    if form.is_valid():
        result = form1_score(form.cleaned_data)
        gender_result, created = GenderDetectionResult.objects.update_or_create(
            user=request.user,
            defaults={
                'form1_result': result,
                'updated_at': timezone.now()
            }
        )
        request.session["first_result"] = result
        return redirect("detector:result1")

    return render(request,"form.html",{"form":form, "form_no": 1})

@login_required
def result1_view(request):
    result = request.session.get("first_result")
    return render(request,"result1.html",{"result":result})

@login_required
def form2_view(request):
    form = FormTwo(request.POST or None)

    if form.is_valid():
        result = form2_score(form.cleaned_data)
        gender_result, created = GenderDetectionResult.objects.get_or_create(
            user=request.user
        )
        gender_result.form2_result = result

        gender_result.save()
        return render(request,"result2.html",{"result":result})

    return render(request,"form.html",{"form":form, "form_no": 2})
