from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
import requests

from student.models import Student
from student.serializeres import StudentSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        password = request.query_params.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(username=username)

            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            microservice_url = f"http://localhost:3000/api/sigaa/student/?user={username}&pass={password}"
            response = requests.get(microservice_url)

            if response.status_code != 200:
                return Response(
                    {"error": "Failed to fetch student data from microservice."},
                    status=response.status_code
                )

            data = response.json().get("studentInfo")

            if not data:
                return Response(
                    {"error": "Student data not found in microservice response."},
                    status=status.HTTP_404_NOT_FOUND
                )

            new_student = Student.objects.create(
                username=username,
                password=password,
                enrollment=data["name"].split(" - ")[0],
                course=data["course"],
                photo=data["photo"]
            )

            serializer = self.get_serializer(new_student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
