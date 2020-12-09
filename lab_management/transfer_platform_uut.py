from os import name
from oldiur.models import Unittable as ut
from oldiur.models import IurMailList as iml

from django.contrib.auth.models import Group,User

# from iur.models import AuthUser as User
from iur.models import Platform as pf
from iur.models import Uut as u
from iur.models import UutPhase as up
from iur.models import Member as mb
from iur.models import UutBorrowHistory as ubh
from iur.models import UutStatus as us
from iur.models import PlatformPhase as pp

class Migrate:

    def get_365_account():

        from O365 import Account,FileSystemTokenBackend,MSOffice365Protocol,MSGraphProtocol,Connection
        import json
        token_backend = FileSystemTokenBackend(token_path='.',token_filename='o365_token.txt')
        credentials = tuple()
        with open('credentials.json','r') as f:
                data = json.load(f)
                credentials = (data['appid'],data['secret'])
        protocal   = MSGraphProtocol(api_version='beta')
        account = Account(credentials,token_backend = token_backend,protocol=protocal)
        return account

    contacts = get_365_account().address_book()

    @property
    def old_mail_list(self):
        return iml.objects.using('old').all().order_by('mail')
    old_mail_list_fail = []

    def transferContacts(self):
        self.old_mail_list_fail.clear()
        for m in self.old_mail_list:
            # print("---------------------------------")
            # print(f'{m.id} {m.name} {m.mail}')
            try:
                if User.objects.filter(email=m.mail).count()>0: continue
                contact = self.contacts.get_contact_by_email(m.mail)
                user,user_created = User.objects.get_or_create(username=m.mail.strip(),email = m.mail.strip())
                if user_created:
                    if contact:
                        name = m.name if 'None' in contact.full_name else contact.full_name
                    else :
                        name =  m.name
                    mb_obj,mb_obj = mb.objects.get_or_create(usernameincompany =name,user = user)
                # print('PASS')
            except Exception as e:
                self.old_mail_list_fail.append({'m':m,'e':e})
        print(f"all/fail : {len(self.old_mail_list)}/{len(self.old_mail_list_fail)}")

    @property
    def old_uuts(self):
        return ut.objects.using('old').all()
    old_uuts_fail=[]
    category = {'DT':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[1][0]),
                    'BDT':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[1][0]),
                    'BAIO':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[2][0]),
                    'AIO':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[2][0]),
                    'cDT':(pf.GROUP_CHOICE[1][0],pf.TARGET_CHOICE[1][0]),
                    'BNB':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[0][0]),
                    'CNB':(pf.GROUP_CHOICE[1][0],pf.TARGET_CHOICE[0][0])
                    }
    
    def transferUut(self,uut):

        group,target = self.category.get(uut.category,(None,None))
        platform,platform_created =  pf.objects.get_or_create(codename=uut.platformname.strip(),cycle=uut.yearcycle.strip(),group = group,target=target) if uut.platformname else  pf.objects.get_or_create(codename=' ')
        phase,phase_created = up.objects.get_or_create(phase_text = uut.phase.strip())
        platform_phase,platform_phase_created = pp.objects.get_or_create(platform=platform,phase = phase)

        status = uut.unitstatus.strip().lower()
        status = 'Keep On' if status in ['Keep on','keep on'] else status
        status,status_created = us.objects.get_or_create(status_text = uut.unitstatus.strip())

        scrap = True if uut.unitstatus.strip() in ['Scrap','Broken','Fix','broken'] else False
        position = uut.position if uut.position else ''
        
        unit,unit_created = u.objects.update_or_create(platform_phase = platform_phase,scrap = scrap,position=position,sn = uut.sn,sku=uut.sku,keyin_time=uut.keyintime,cpu=uut.cpu,remark=uut.noteone,status=status)
        
        
        if uut.borrower:
            if uut.borrower.strip() not in ['Storage','storage','Detained by Emma','Donated TDC Pool','Donated for YEP','LAB','PDM','Return 8F','Srotage','Broken','broken','Fix']:
                borrower = mb.objects.get(usernameincompany__search=uut.borrower)
                unit.uutborrowhistory_set.create(member=borrower,rent_time=uut.borrowingdate1)

    def transferUuts(self):
        self.old_uuts_fail.clear()
        for uut in self.old_uuts:
            # print("----------------")
            # print(uut)
            try:
                self.transferUut(uut)
                # print('PASS')
            except Exception as e:
                self.old_uuts_fail.append({'uut':uut,'e':e})

        print(f"all/fail : {len(self.old_uuts)}/{len(self.old_uuts_fail)}")


    def fix(self):
        def assignMailAddr(uut,unit,mail):
            borrower = mb.objects.filter(user__email=mail)
            if not borrower.count():
                contact = self.contacts.get_contact_by_email(mail)
                user,user_created = User.objects.get_or_create(username=mail.strip(),email = mail.strip())
                if user_created:
                    if contact:
                        name = uut.borrower if 'None' in contact.full_name else contact.full_name
                    else :
                        name =  uut.borrower
                    borrower = mb.objects.create(usernameincompany =name,user = user)
            else:
                borrower = borrower.first()
            unit.uutborrowhistory_set.create(member=borrower,rent_time=uut.borrowingdate1)
        
        wait_for_fix = self.old_uuts_fail.copy()
        for uut in self.old_uuts_fail:
            try:
                uut_obj = uut['uut']
                unit = u.objects.get(sn=uut_obj.sn)
                if uut_obj.borrower.strip() in ['Bernice, Chiang','Bernice, Chiang58']:
                    assignMailAddr(uut_obj,unit,'bernice.chiang58@hp.com')
                elif uut_obj.borrower.strip() in ['Chien, Jeremy (Comms Radio HW)']:
                    assignMailAddr(uut_obj,unit,'jeremy.chien@hp.com')
                elif uut_obj.borrower.strip() in ['David, Chi']:
                    assignMailAddr(uut_obj,unit,'jeremy.chien@hp.com')
                elif uut_obj.borrower.strip() in ['Henry, Cheng']:
                    assignMailAddr(uut_obj,unit,'henry.cheng@hp.com')
                elif uut_obj.borrower.strip() in ['Mark, Su']:
                    assignMailAddr(uut_obj,unit,'yj.su@hp.com')
                elif uut_obj.borrower.strip() in ['Ryan, Wu']:
                    assignMailAddr(uut_obj,unit,'ryan.wu@hp.com')
                elif uut_obj.borrower.strip() in ['Serena, Lee']:
                    assignMailAddr(uut_obj,unit,'serena.lee@hp.com')
                elif uut_obj.borrower.strip() in ['Sheena, Kuo']:
                    assignMailAddr(uut_obj,unit,'sheena.kuo@hp.com')
                elif uut_obj.borrower.strip() in ['Timothy, Wang']:
                    assignMailAddr(uut_obj,unit,'timothy.wang1@hp.com')
                elif uut_obj.borrower.strip() in ['Yen, Lone (Lone,Yen (CMITNB))']:
                    assignMailAddr(uut_obj,unit,'lone.yen@hp.com')
                else:
                    continue
                wait_for_fix.remove(uut)
            
            except Exception as e:
                print(e)
            
        print(f"all/fail : {len(self.old_uuts_fail)}/{len(wait_for_fix)}")
        self.old_uuts_fail = wait_for_fix

    def transfer(self):
        self.transferContacts()
        self.transferUuts()
        self.fix()
            
                

