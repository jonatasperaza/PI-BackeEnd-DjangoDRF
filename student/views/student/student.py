from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

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
            microservice_url = f"https://pi-microservices-177ebc723a1f.herokuapp.com/api/sigaa/student/?user={username}&pass={password}"

            print(microservice_url)
            response = requests.get(microservice_url)

            print(response.status_code)

            if response.status_code != 200:
                return Response(
                    {"error": "Failed to fetch student data from microservice."},
                    status=response.status_code
                )

            data = response.json().get("studentInfo")

            print(data)

            if not data:
                return Response(
                    {"error": "Student data not found in microservice response."},
                    status=status.HTTP_404_NOT_FOUND
                )

            new_student = Student.objects.create(
                username=username,
                password=password,
                enrollment=data["name"].split(" - ")[0],
                name=data["name"].split(" - ")[1],
                course=data["course"],
                photo=data["photo"]
            )

            serializer = self.get_serializer(new_student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
