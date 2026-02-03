from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Student, Course, Exam, Mark
from django.utils.timezone import now
from django.utils import timezone


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            if user.is_staff:
                return redirect('/admin-dashboard/')
            return redirect('/student-dashboard/')
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        course_id = request.POST['course']

        # create user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # link student with course
        course = Course.objects.get(id=course_id)
        Student.objects.create(
            user=user,
            course=course
        )

        return redirect('/')

    return render(request, 'register.html', {
        'courses': Course.objects.all()
    })

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def manage_students(request):
    return render(request, 'manage_students.html', {
        'students': Student.objects.all()
    })


def manage_courses(request):
    if request.method == "POST":
        Course.objects.create(name=request.POST['name'])
    return render(request, 'manage_courses.html', {
        'courses': Course.objects.all()
    })


def manage_exams(request):
    if request.method == "POST":
        Exam.objects.create(
            name=request.POST['name'],
            course_id=request.POST['course'],
            subjects=request.POST['subjects'],
            date=request.POST['date'],
            time=request.POST['time']
        )
    return render(request, 'manage_exams.html', {
        'courses': Course.objects.all(),
        'exams': Exam.objects.all()
    })



def add_marks(request):
    if request.method == "POST":
        student_id = request.POST['student']
        exam_id = request.POST['exam']
        count = int(request.POST['count'])

        for i in range(1, count + 1):
            subject = request.POST[f'subject_{i}']
            marks = request.POST[f'marks_{i}']

            Mark.objects.create(
                student_id=student_id,
                exam_id=exam_id,
                subject=subject,
                marks=marks
            )

        # IMPORTANT: redirect after saving
        return redirect('/marks/')

    return render(request, 'add_marks.html', {
        'students': Student.objects.all(),
        'exams': Exam.objects.all(),
        'marks': Mark.objects.all()
    })



def student_dashboard(request):
    student = Student.objects.get(user=request.user)

    upcoming_exams = Exam.objects.filter(course=student.course)

    return render(request, 'student_dashboard.html', {
        'student': student,
        'upcoming_exams': upcoming_exams
    })

def upcoming_exams(request):
    student = Student.objects.get(user=request.user)
    today = timezone.now().date()

    exams = Exam.objects.filter(
        course=student.course,
        date__gte=today
    ).order_by('date', 'time')

    return render(request, 'upcoming_exams.html', {
        'exams': exams
    })


def view_marks(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            student = Student.objects.get(user=user)
            marks = Mark.objects.filter(student=student)
            return render(request, 'marksheet.html', {'marks': marks})

    return render(request, 'view_marks.html')

def delete_student(request, id):
    Student.objects.get(id=id).delete()
    return redirect('/students/')

def delete_course(request, id):
    Course.objects.get(id=id).delete()
    return redirect('/courses/')

def delete_exam(request, id):
    Exam.objects.get(id=id).delete()
    return redirect('/exams/')

def delete_mark(request, id):
    Mark.objects.get(id=id).delete()
    return redirect('/marks/')
