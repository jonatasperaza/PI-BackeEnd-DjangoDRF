from rest_framework.serializers import ModelSerializer

from student.models import Grades

class GradesSerializer(ModelSerializer):
    class Meta:
        model = Grades
        fields = "__all__"