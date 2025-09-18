#from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from .models import Student, MessCut, IceCream, StudentIceCream
from .forms import StudentForm, MessCutForm, IceCreamForm
from datetime import timedelta

# Only superuser check
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")


@login_required
@superuser_required
def dashboard(request):
    students = Student.objects.all()
    query = request.GET.get("q")
    if query:
        students = students.filter(name__icontains=query)
    return render(request, "dashboard.html", {"students": students})


@login_required
@superuser_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    mess_form = MessCutForm()
    ice_form = IceCreamForm()
    return render(request, "student_detail.html", {
        "student": student,
        "mess_form": mess_form,
        "ice_form": ice_form
    })


@login_required
@superuser_required
def add_messcut(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = MessCutForm(request.POST)
        if form.is_valid():
            messcut = form.save(commit=False)
            messcut.student = student
            if messcut.days_count() >= 3:
                messcut.save()
    return redirect("student_detail", student_id=student.id)


"""@login_required
@superuser_required
def add_icecream(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentIceCreamForm(request.POST)
        if form.is_valid():
            icecream = form.save(commit=False)
            icecream.student = student
            icecream.save()
    return redirect("student_detail", student_id=student.id)"""


#@login_required
#@superuser_required
"""def fees_list(request):
    students = Student.objects.all()
    data = []
    for student in students:
        messcuts = MessCut.objects.filter(student=student)
        icecreams = StudentIceCream.objects.filter(student=student)

        # Calculate food fee with mess cuts
        total_cut = 0
        for cut in messcuts:
            if cut.days_count() >= 3:
                total_cut += cut.days_count() * 100

        # Add ice cream charges
        icecream_total = sum(i.icecream.price for i in icecreams)

        final_fee = student.base_rent + student.food_fee - total_cut + icecream_total
        data.append({
            "student": student,
            "final_fee": final_fee
        })
    return render(request, "fees_list.html", {"data": data})"""


def fees_list(request):
    """students = Student.objects.all()
    data = []
    for student in students:
        monthly_fee = student.calculate_fee()
        data.append({
            'student': student,
            'fee': monthly_fee
        })
    return render(request, 'fees_list.html', {'data': data})"""
    students = Student.objects.all()
    return render(request, "fees_list.html", {"students": students})




def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


def delete_student_page(request):
    query = request.GET.get("q", "")
    if query:
        students = Student.objects.filter(name__icontains=query)
    else:
        students = Student.objects.none()  # empty until search
    return render(request, "delete_student.html", {"students": students})


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        student.delete()
        return redirect("delete_student_page")
    return redirect("dashboard")


def add_icecream_global(request):
    if request.method == "POST":
        form = IceCreamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_icecream')  # After saving, show list of ice creams
    else:
        form = IceCreamForm()
    return render(request, 'add_icecream.html', {'form': form})


def add_icecream(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = IceCreamForm(request.POST)
        if form.is_valid():
            icecream = form.save(commit=False)
            # Add the ice cream price to student’s extra fees
            if not hasattr(student, 'extra_fees'):
                student.extra_fees = 0
            student.extra_fees += icecream.price
            student.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = IceCreamForm()

    return render(request, 'hostel_app/add_icecream.html', {
        'form': form,
        'student': student
    })

# Page for listing available ice creams
def list_icecream(request):
    icecreams = IceCream.objects.all()
    return render(request, 'list_icecream.html', {'icecreams': icecreams})