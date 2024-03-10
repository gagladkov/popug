from rest_framework import status

from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.logic import get_company_profile
from accounting.models import Profile, Task


class GetCompanyBalance(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['role:admin']
    allowed_methods = ['get']

    def get(self, request, *args, **kwargs):
        balance = get_company_profile().balance
        return Response({'company_balance': balance}, status=status.HTTP_200_OK)


class GetMinusEmployersCount(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['role:admin']
    allowed_methods = ['get']

    def get(self, request, *args, **kwargs):
        minus_employers_count = Profile.objects.filter(is_company=False, balance__lt=0).count()
        return Response({'count': minus_employers_count}, status=status.HTTP_200_OK)


class GetExpensiveTaks(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['role:admin']
    allowed_methods = ['get']

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        max_close_price = Task.objects.filter(is_open=False,
                                              closed_at__range=[start_date, end_date]).order_by('-close_price').first()
        return Response({'max_close_price': max_close_price}, status=status.HTTP_200_OK)
