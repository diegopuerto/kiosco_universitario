# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
from apps.DaneUsers.models import IdType, AgeRange, EducationalType,ActivityType,\
    DisabilityType, Departament, City, ProfessionalType
from django.contrib.auth.models import Group
from libs.groups_utils.permissions_assigner import PermissionsAssigner
from apps.services_requests.models import StatisticalCultureService
from django.utils import translation
import csv
import os

class Command(BaseCommand):
    help = _(u'Load initial options for DANE users')
    permission_assigner = PermissionsAssigner()
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    

    def _console_output(self, message, options, verbosity = 1):
        if options["verbosity"] >= verbosity:
            print message

    def handle(self, *args, **options):
        if "is_unittest" not in options.keys() or not options["is_unittest"]:
            translation.activate('es')
            
        if "is_unittest" not in options.keys() or not options["is_unittest"]:
            CitiesDepartamentsFile = os.path.join(self.__location__, "MunicipiosYDepartamentos.csv")
        else:
            CitiesDepartamentsFile = os.path.join(self.__location__, "MunicipiosYDepartamentosTest.csv")
            
        with open(CitiesDepartamentsFile, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            header = reader.next()
            
            self._console_output("Start loading Departaments", options)
            departaments = {row[2]: row[3] for row in reader}
            for id,name in departaments.iteritems():
                self._get_or_create_in_model(id, {"name":name,"alias":name}, Departament)  
                
        
        self._console_output("Start loading Cities", options)           
        with open(CitiesDepartamentsFile, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            header = reader.next()                       
            for row in reader:
                self._get_or_create_in_model(row[0], {"name":row[1],"alias":row[1],"departament_id":row[2]}, City)      

        ID_TYPE_OPTIONS = (
            (1,'cedula',_(u'Cédula de Ciudadanía')),
            (2,'nuip',_(u'NUIP')),
            (4,'NIP/ tarjeta_identidad',_(u'NIP/ Tarjeta de Identidad')),
            (6,'passport',_(u'Passport')),
            (7,'ce',_(u'Cédula de Extranjería')),
        )

        AGE_RANGE_OPTIONS = (
            (0,'under18',_(u'Under 18 years')),
            (1,'18to25',_(u'Between 18 to 25 years')),
            (2,'26to35',_(u'Between 26 to 35  years')),
            (3,'36to45',_(u'Between 36 to 45 years')),
            (4,'46to55',_(u'Between 46 to 55 years')),
            (5,'55+',_(u'More than 55 years old'))
        )
        
        EDUCATIONAL_OPTIONS = (
            (1,'primary',_(u'Primary')),
            (3,'secundary',_(u'Secundary')),
            (4,'technician',_(u'Technician')),
            (5,'technologist',_(u'Technologist')),
            (7,'college',_(u'College')),
            (8,'specialization',_(u'Specialization')),
            (9,'master',_(u'Master')),
            (10,'doctorate',_(u'Doctorate')),
            (11,'postdoctoral',_(u'Posdoctoral'))
        )

        ACTIVITY_OPTIONS = (
            (0,'study',_(u'Study')),
            (1,'work',_(u'Work')),
            (2,'studywork',_(u'Study and work')),
            (3,'unemployee',_(u'Unemployee')),
            (4,'housewife',_(u'Housewife')),
            (5,'retired',_(u'Retired'))
        )

        # Standarize names to fit english 
        PROFESSIONAL_OPTIONS = (
            (1,'laywer',_(u'Laywer')),
            (2,'administrador',_(u'Administrador')),
            (3,'storekeeper',_(u'Storekeeper')),
            (4,'analist',_(u'Analist')),
            (65,'architect',_(u'Architect')),
            (5,'adviser',_(u'Adviser')),
            (6,'assistant',_(u'Asistant')),
            (7,'research_assistent',_(u'Research Assistant')),
            (8,'auditor',_(u'Auditor')),
            (9,'helper',_(u'Helper')),
            (10,'cashier',_(u'Cashier')),
            (67,'merchant',_(u'Merchant')),
            (68,'international_trading',_(u'International trading')),
            (11,'social_communicator',_(u'Social communicator')),
            (12,'consultant',_(u'Consultant')),
            (13,'accounting',_(u'Accounting')),
            (14,'controller',_(u'Controller')),
            (15,'coordinator',_(u'Coordinator')),
            (16,'draftsman',_(u'Drafsman')),
            (17,'director',_(u'Director')),
            (18,'designer',_(u'Designer')),
            (19,'profesor',_(u'Professor and/or Teacher')),
            (60,'economist',_(u'Economist')),
            (20,'editor',_(u'Editor')),
            (21,'executive',_(u'Executive')),
            (59,'nurse',_(u'Nurse')),
            (22,'trainer',_(u'Trainer / capacitador')),
            (58,'statistics',_(u'Estadístico')),
            (61,'evaluator',_(u'Evaluador')),
            (23,'manager',_(u'Manager')),
            (24,'general_manager',_(u'General manager')),
            (25,'promoter',_(u'Promoter')),
            (26,'engineer',_(u'Engineer')),
            (27,'inspector',_(u'Inspector')),
            (28,'interventor',_(u'Interventor')),
            (29,'chief',_(u'Chief')),
            (30,'doctor',_(u'Doctor')),
            (64,'vet',_(u'Vet')),
            (31,'messenger',_(u'Messenger')),
            (62,'marketing',_(u'Marketing')),
            (32,'mercaderista',_(u'Mercaderista')),
            (33,'waiter',_(u'Waiter')),
            (69,'international_business',_(u'International business')),
            (34,'operator',_(u'Operator')),
            (35,'intern',_(u'Intern')),
            (36,'food_preparer',_(u'Preparador de alimentos')),
            (37,'president',_(u'President')),
            (38,'professional',_(u'Professional')),
            (39,'programmer',_(u'Programmer')),
            (40,'promoter',_(u'Promoter')),
            (41,'recepcionist',_(u'Recepcionist')),
            (42,'editor',_(u'Editor')),
            (43,'reporter',_(u'Reporter')),
            (44,'sales_respresentative',_(u'Sales representative')),
            (45,'resident',_(u'Residente')),
            (46,'fiscal_auditor',_(u'Fiscal auditor')),
            (47,'secretary',_(u'Secretary')),
            (66,'sociologist',_(u'Sociologist')),
            (48,'subdirector',_(u'Subdirector')),
            (49,'submanager',_(u'Submanager')),
            (50,'supernumerary',_(u'Supernumerary')),
            (51,'supervisor',_(u'Supervisor')),
            (52,'technician',_(u'Technician')),
            (63,'social_worker',_(u'Social worker')),
            (53,'trader',_(u'Trader')),
            (54,'seller',_(u'Seller')),
            (55,'vicepresident',_(u'Vicepresident')),
            (56,'health_visitor',_(u'Health visitor')),
            (57,'webmaster',_(u'Webmaster'))
        )
        
        DISABILITY_OPTIONS = (
            (0,'none disability',_(u'None Disability')),
            (1,'movility/physical',_(u'Movility/Physical')),
            (2,'auditive',_(u'Auditive')),
            (3,'mental psychosocial',_(u'Mental Psychosocial')),
            (4,'mental cognitive',_(u'Mental Cognitive')),
            (5,'multiple',_(u'Multiple')),
        )
        
        STATISTICAL_CULTURE_SERVICES = (
            (0, 'pin1pin2', _(u'Pin 1, Pin 2, Pin Dane')),
            (1, 'DaneAcademics', _(u'Dane in Academics')),
        )
        
        GROUPS = (
            ('citizen', []),
            ('servant',[]),
            ('statistical_society_user',[]),
            ('statistical_society_reader',[]),
            ('statistical_society_admin',[
                                           {"model":"statisticalsocietymember","name":PermissionsAssigner.ADD },
                                           {"model":"statisticalsocietymember","name":PermissionsAssigner.CHANGE },
                                           {"model":"statisticalsocietymember","name":PermissionsAssigner.DELETE },
                                           {"model":"statisticalsocietyuserpreference","name":PermissionsAssigner.ADD },
                                           {"model":"statisticalsocietyuserpreference","name":PermissionsAssigner.CHANGE },
                                           {"model":"statisticalsocietyuserpreference","name":PermissionsAssigner.DELETE },
                                           {"model":"userprofile","name":PermissionsAssigner.ADD },
                                           {"model":"userprofile","name":PermissionsAssigner.CHANGE },
                                           {"model":"userprofile","name":PermissionsAssigner.DELETE },
                                           ]),
       )
        
        SUPERUSERS = ("ejarizar@dane.gov.co",
                      "davillamilm@dane.gov.co",
                      "apforerow@dane.gov.co",
                      "camolinaa@dane.gov.co",
                      "dejimenezg@dane.gov.co",
                      "oasaavedrac@dane.gov.co")
        self._console_output("Adding Groups", options)
        for group_data in GROUPS:
            group, was_created = Group.objects.get_or_create(name=group_data[0])
            if was_created:
                for permission in group_data[1]:           
                    self.permission_assigner.set_permissions(group, permission["model"], permission["name"])


        self._console_output("Start loading Activity type options", options)
        for act in ACTIVITY_OPTIONS:
            self._get_or_create_in_model(act[0], {"name":act[1],"alias":act[2]}, ActivityType)
        self._console_output("Activity type loaded", options)

        self._console_output("Start loading ID Type options", options)
        for id_type in ID_TYPE_OPTIONS:
            self._get_or_create_in_model(id_type[0], {"name":id_type[1],"alias":id_type[2]}, IdType)
        self._console_output("ID type loaded", options)

        self._console_output("Start loading Age Range type options", options)
        for age in AGE_RANGE_OPTIONS:
            self._get_or_create_in_model(age[0], {"name":age[1],"alias":age[2]}, AgeRange)         
        self._console_output("Age range type loaded", options)

        self._console_output("Start loading Education type options", options)
        for ed in EDUCATIONAL_OPTIONS:
            self._get_or_create_in_model(ed[0], {"name":ed[1],"alias":ed[2]}, EducationalType)              
        self._console_output("Education type loaded", options)
        
        self._console_output("Start loading Education type options", options)
        for prof in PROFESSIONAL_OPTIONS:
            self._get_or_create_in_model(prof[0], {"name":prof[1],"alias":prof[2]}, ProfessionalType)              
        self._console_output("Profesional type loaded", options)

        self._console_output("Start loading Disability type options", options)
        for ed in DISABILITY_OPTIONS:
            self._get_or_create_in_model(ed[0], {"name":ed[1],"alias":ed[2]}, DisabilityType)              
        self._console_output("Disability type loaded", options)
                
        self._console_output("Start loading statistical culture services", options)
        for ser in STATISTICAL_CULTURE_SERVICES:
            self._get_or_create_in_model(ser[0], {"name":ser[1],"alias":ser[2]}, StatisticalCultureService)  
        self._console_output("statistical culture services loaded", options)        
        
#         Creates a default superuser   
        if not "is_unittest" in options.keys() or not options["is_unittest"]:     
            for superuser in SUPERUSERS:    
                self._console_output("Creating default superuser", options)
                from apps.DaneUsers.models import BasicDaneUser as User
                user = User.objects.get_or_create(email=superuser)[0]
                user.is_superuser=True
                user.is_staff = True
                user.save()
            
        
    def _get_or_create_in_model(self, object_id, data, model):  
        if model.objects.filter(id=object_id).exists():
            model.objects.filter(id=object_id).update(**data)
        else:
            model.objects.get_or_create(id=object_id, **data)

