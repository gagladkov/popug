from django.urls import path

from accounting.views import TransactionList, GetBalance
from analytics.views import GetMinusEmployersCount, GetCompanyBalance, GetExpensiveTaks

urlpatterns = [
    path('transactions/', TransactionList.as_view()),
    path('balance/', GetBalance.as_view()),

    path('analytics/company_balance', GetCompanyBalance.as_view()),
    path('analytics/minus_employers_count', GetMinusEmployersCount.as_view()),
    path('analytics/expensive_task_by_period', GetExpensiveTaks.as_view()),
]
