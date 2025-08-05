from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Student, Course
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.core.files.images import get_image_dimensions
from django.db.models import Q
import datetime

@api_view(['GET'])
def student_list(request):
    students = Student.objects.all()
    data = []

    for student in students:
        data.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "age": student.age,
            "joined_at": student.joined_at,
            "updated_at": student.updated_at,
            "image": student.image.url if student.image else None,
            "courses": [c.name for c in student.courses.all()]
        })

    return JsonResponse(data, safe=False)

@api_view(['GET'])
def student_detail(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)

    data = {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "age": student.age,
        "joined_at": student.joined_at,
        "updated_at": student.updated_at,
        "image": student.image.url if student.image else None,
        "courses": [c.name for c in student.courses.all()]
    }
    return JsonResponse(data)


@api_view(['POST'])
def student_create(request):
    data = request.data

    required_fields = ['name', 'email', 'age', 'joined_at', 'courses']
    for field in required_fields:
        if field not in data:
            return JsonResponse({"error": f"{field} is required"}, status=400)

    if int(data['age']) < 16:
        return JsonResponse({"error": "Age must be at least 16"}, status=400)

    try:
        validate_email(data['email'])
    except:
        return JsonResponse({"error": "Invalid email format"}, status=400)
    
    if Student.objects.filter(email=data['email']).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)

    joined_at = datetime.datetime.strptime(data['joined_at'], "%Y-%m-%d").date()
    if joined_at > datetime.date.today():
        return JsonResponse({"error": "joined_at cannot be in the future"}, status=400)

    courses = Course.objects.filter(id__in=data['courses'])
    if len(courses) != len(data['courses']):
        return JsonResponse({"error": "Some courses not found"}, status=400)

    student = Student.objects.create(
        name=data['name'],
        email=data['email'],
        age=data['age'],
        joined_at=joined_at,
        image=request.FILES.get('image')
    )
    student.courses.set(courses)
    student.save()

    return JsonResponse({"message": "Student created", "id": student.id})

@api_view(['PUT'])
def student_update(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)

    data = request.data

    if 'age' in data and int(data['age']) < 16:
        return JsonResponse({"error": "Age must be at least 16"}, status=400)

    if 'email' in data and data['email'] != student.email:
        if Student.objects.filter(email=data['email']).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)


    student.name = data.get('name', student.name)
    student.email = data.get('email', student.email)
    student.age = data.get('age', student.age)

    if 'joined_at' in data:
        joined_at = datetime.datetime.strptime(data['joined_at'], "%Y-%m-%d").date()
        if joined_at > datetime.date.today():
            return JsonResponse({"error": "joined_at cannot be in the future"}, status=400)
        student.joined_at = joined_at

    if request.FILES.get('image'):
        student.image = request.FILES['image']

    if 'courses' in data:
        courses = Course.objects.filter(id__in=data['courses'])
        student.courses.set(courses)

    student.save()
    return JsonResponse({"message": "Student updated"})


@api_view(['DELETE'])
def student_delete(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)

    student.delete()
    return JsonResponse({"message": "Student deleted"})

@api_view(['GET'])
def students_in_course(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)

    students = course.student_set.all()
    data = [{
        "id": s.id,
        "name": s.name,
        "email": s.email
    } for s in students]

    return JsonResponse(data, safe=False)
