'''
Created on 12/11/2015

@author: EJArizaR
'''
import unittest
from libs.StatisticalSocietyUsersExporterUtils.Formatter import Formatter 

class Test(unittest.TestCase):


    def setUp(self):
        self.input_text = "email,userProfile__cellphone\n\
                      user1@anyserver.com,3001111111\n\
                      user2@anyserver.com,3002222222\n\
                      user3@anyserver.com,3003333333\n"


    def tearDown(self):
        pass


    def test_extracts_emails(self):
        formatter = Formatter()
        self.assertEqual(formatter.email_format(self.input_text), "user1@anyserver.com,user2@anyserver.com,user3@anyserver.com")
        
    def test_extracts_cellphones(self):
        formatter = Formatter()
        self.assertEqual(formatter.cellphone_format(self.input_text), "3001111111,3002222222,3003333333")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()