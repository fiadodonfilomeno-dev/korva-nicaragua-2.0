import pytest
from django.urls import reverse
from .models import AnalyticsReport


class TestAnalyticsReportModel:
    def test_report_creation(self, profile):
        report = AnalyticsReport.objects.create(user=profile)
        assert report.total_posts == 0
        assert report.total_products == 0
        assert report.total_collaborations == 0

    def test_report_str(self, profile):
        report = AnalyticsReport.objects.create(user=profile)
        assert profile.business_name in str(report)


class TestReportsViews:
    def test_reports_view_requires_login(self, client):
        response = client.get(reverse('reports'))
        assert response.status_code == 302

    def test_reports_view_authenticated(self, client_logged_in):
        response = client_logged_in.get(reverse('reports'))
        assert response.status_code == 200

    def test_export_csv(self, client_logged_in):
        response = client_logged_in.get(reverse('export_csv'))
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'

    def test_export_pdf(self, client_logged_in):
        response = client_logged_in.get(reverse('export_pdf'))
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/pdf'
