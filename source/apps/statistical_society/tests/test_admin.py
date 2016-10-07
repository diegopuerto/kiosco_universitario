'''
Created on 16/10/2015

@author: EJArizaR
'''
import unittest
from apps.DaneUsers.tests.test_base import test_base
from mock.mock import patch, MagicMock, ANY
from apps.statistical_society.admin import StatisticalSocietyMembersAdmin 
from apps.statistical_society.models import StatisticalSocietyMember 
from django.contrib.admin.sites import AdminSite


class StatisticalSocietyMembersAdminTest(test_base):

    def setUp(self):
        pass


    def tearDown(self):
        pass

    @patch('apps.statistical_society.admin.EmailUserAdmin.get_queryset')
    def test_query_is_filter_by_group(self, parent_get_queryset_mock):
        query_mock = MagicMock()
        parent_get_queryset_mock.return_value = query_mock
        admin = StatisticalSocietyMembersAdmin(StatisticalSocietyMember, AdminSite())
        admin.get_queryset(ANY)
        query_mock.filter.assert_called_once_with(groups__name='statistical_society_user')
        
    @patch('apps.statistical_society.admin.EmailUserAdmin.get_queryset')
    def test_returns_filtered_query(self, parent_get_queryset_mock):
        query_mock = MagicMock()
        parent_get_queryset_mock.return_value = query_mock
        admin = StatisticalSocietyMembersAdmin(StatisticalSocietyMember, AdminSite())
        expected_query = query_mock.filter() 
        actual_query = admin.get_queryset(ANY)
        self.assertEqual(expected_query, actual_query)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()