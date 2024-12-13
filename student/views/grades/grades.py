import requests
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

class GradesViewSet(ViewSet):

    def list(self, request):

        username = request.query_params.get('username')
        password = request.query_params.get('password')
        index = request.query_params.get('index', 1)

        if not username or not password:
            return Response(
                {"error": "Os parâmetros 'user' e 'pass' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = f"http://localhost:3000/api/sigaa/notas/?user={username}&pass={password}&index={index}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Erro ao acessar o microserviço: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
