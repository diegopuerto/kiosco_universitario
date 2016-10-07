'''
Created on 16/10/2015

@author: EJArizaR
'''
import unittest
from libs.groups_utils.permissions_assigner import PermissionsAssigner
from mock.mock import ANY, patch, MagicMock


@patch("libs.groups_utils.permissions_assigner.Permission")
@patch("libs.groups_utils.permissions_assigner.ContentType")
class PermissionsAssignerTest(unittest.TestCase):
    def setUp(self):
        self.permissions_asigner = PermissionsAssigner()
        self.group_mock = MagicMock()

    def tearDown(self):
        pass

    def test_gets_contenttype_by_modelname(self, ContentTypeMock, PermissionMock):
        self.permissions_asigner.set_permissions(group = self.group_mock, modelname = "model_name", permission = PermissionsAssigner.ADD)
        ContentTypeMock.objects.get.assert_called_once_with(model = "model_name")
     
    def test_gets_permission_by_contenttype_and_permission(self, ContentTypeMock, PermissionMock):
        contenttype_instance_mock = MagicMock()
        ContentTypeMock.objects.get.return_value = contenttype_instance_mock
        self.permissions_asigner.set_permissions(group = self.group_mock, modelname = "model_name", permission = PermissionsAssigner.DELETE)
        PermissionMock.objects.get.assert_called_once_with(content_type=contenttype_instance_mock, 
                                             codename=PermissionsAssigner.DELETE + "model_name")
        
    def test_assign_right_permissions_to_the_group(self, ContentTypeMock, PermissionMock):
        permission_instance_mock = MagicMock()
        PermissionMock.objects.get.return_value = permission_instance_mock
        self.permissions_asigner.set_permissions(group = self.group_mock, modelname = "model_name", permission = PermissionsAssigner.DELETE)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()