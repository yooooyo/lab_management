from os import name
from oldiur.models import Unittable as ut
from oldiur.models import IurMailList as iml

# from django.contrib.auth.models import Group,User

from iur.models import AuthUser as User
from iur.models import Platform as pf
from iur.models import Uut as u
from iur.models import UutPhase as up
from iur.models import Member as mb
from iur.models import UutBorrowHistory as ubh
from iur.models import UutStatus as us
from iur.models import PlatformPhase as pp


all_iml = iml.objects.using('old').all().order_by('mail')
fail_iml=0

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

for m in all_iml:
    print("---------------------------------")
    print(f'{m.id} {m.name} {m.mail}')
    try:
        contact = contacts.get_contact_by_email(m.mail)
        user,user_created = User.objects.get_or_create(username=m.mail.strip(),email = m.mail.strip())
        print(f'{user} - {user_created}')
        if user_created:
            if contact:
                name = m.name if 'None' in contact.full_name else contact.full_name
            else :
                name =  m.name
            mb_obj,mb_obj = mb.objects.get_or_create(usernameincompany =name,user = user)
            print(f'{mb_obj} - {mb_obj}')
        print('PASS')
    except Exception as e:
        fail_iml = fail_iml + 1 

        print(e)
print(f"all/fail : {all_iml.count()}/{fail_iml}")


category = {'DT':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[1][0]),
             'BDT':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[1][0]),
             'BAIO':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[2][0]),
             'AIO':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[2][0]),
             'cDT':(pf.GROUP_CHOICE[1][0],pf.TARGET_CHOICE[1][0]),
             'BNB':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[0][0]),
             'CNB':(pf.GROUP_CHOICE[1][0],pf.TARGET_CHOICE[0][0])
            }
all_uut = ut.objects.using('old').all()

fail_uut_cnt = 0
fail_list = []
for uut in ut.objects.using('old').all():
    print("----------------")
    print(uut)
    try:
        if uut.platformname:
            group,target = category.get(uut.category,(None,None))
            platform,platform_created = pf.objects.get_or_create(codename=uut.platformname.strip(),cycle=uut.yearcycle.strip(),group = group,target=target)
            phase,phase_created = up.objects.get_or_create(phase_text = uut.phase.strip())
            platform_phase,platform_phase_created = pp.objects.get_or_create(platform=platform,phase = phase)

            status,status_created = us.objects.get_or_create(status_text = uut.unitstatus.strip())

            scrap = True if uut.unitstatus == 'Scrap' else False
            position = uut.position if uut.position else ''
            
            unit,unit_created = u.objects.get_or_create(platform_phase = platform_phase,scrap = scrap,position=position,sn = uut.sn,sku=uut.sku,keyin_time=uut.keyintime,cpu=uut.cpu,remark=uut.noteone,status=status)
            
            
            if uut.borrower:
                if not 'Storage' in uut.borrower:
                    borrower = mb.objects.get(usernameincompany__search=uut.borrower)
                    ubh.objects.create(member=borrower,rent_time=uut.borrowingdate1,uut = unit,)

            
            print('PASS')


    except Exception as e:
        fail_uut_cnt+=1
        print(e)
        fail_list.append(e)
        print('FAIL')

print(f"all/fail : {all_uut.count()}/{fail_uut_cnt}")
print(set(fail_list))