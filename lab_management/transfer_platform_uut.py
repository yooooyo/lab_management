from oldiur.models import Unittable as ut
from oldiur.models import IurMailList as iml
from iur.models import Platform as pf
from iur.models import Uut as u
from iur.models import UutPhase as up
from iur.models import Member as mb
from iur.models import UutBorrowHistory as ubh
from iur.models import UutStatus as us




category = {'DT':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[1][0]),
             'BDT':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[1][0]),
             'BAIO':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[2][0]),
             'AIO':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[2][0]),
             'cDT':(pf.GROUP_CHOICE[1][0],pf.TARGET_CHOICE[1][0]),
             'BNB':(pf.GROUP_CHOICE[0][0],pf.TARGET_CHOICE[0][0]),
             'CNB':(pf.GROUP_CHOICE[1][0],pf.TARGET_CHOICE[0][0])
            }

for uut in ut.objects.using('old').all():
    try:

        if uut.platformname:
            platform = pf.objects.filter(codename=uut.platformname)
            if platform.count() == 0:
                codename=uut.platformname
                cycle = uut.yearcycle
                group = None
                target = None
                if uut.category:
                    group,target = category.get(uut.category,(None,None))
                platform = pf.objects.create(codename=codename,cycle=cycle,group=group,target=target)
                platform.save()
            else:
                platform = platform.first()
            scrap = False
            position=''
            if uut.unitstatus=='Scrap': scrap=True
            status=None
            if uut.unitstatus:
                status = us.objects.filter(status_text=uut.unitstatus)
                if status.count() == 0:
                    status = us.objects.create(status_text=uut.unitstatus)
                    status.save()
                else:
                    status = status.first()
            if uut.position:position = uut.position
            phase = None
            if uut.phase:
                _up = up.objects.filter(phase_text=uut.phase)
                if _up.count()==0:
                    phase = up.objects.create(phase_text=uut.phase)
                    phase.save()
                else:
                    phase = _up.first()

            unit = u.objects.create(phase=phase,platform=platform,sn=uut.sn,sku=uut.sku,status=status,scrap=scrap,position=position,keyin_time=uut.keyintime,cpu=uut.cpu,remark=uut.noteone)
            unit.save()
            
            borrower=None
            if uut.borrower:
                borrower = mb.objects.filter(usernameincompany__search=uut.borrower)
                if borrower.count() >= 1:
                    borrower = borrower.first()
                    ubh.objects.create(member=borrower,rent_time=uut.borrowingdate1,uut = unit,)

    except:
        print(uut)