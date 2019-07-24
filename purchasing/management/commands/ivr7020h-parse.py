from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from purchasing.models import IVR7020H
from django.utils import timezone

class Command(BaseCommand):
    help = 'Parsing IVR7020H PRN to DB'

    def handle(self, *args, **options):
        FILE='/home/nest/public_html/media/prn/IVR7020H'
        IVR7020H.objects.all().delete()
        f = open(FILE, "r")
        i = 0
        for l in f.readlines():
            if i > 5:
                content = {
                    'master' : l[6:15].strip(),
                    'po' : l[15:30].strip(),
                    'created' : datetime.strptime(l[30:38].strip(),"%d%b%y") if l[30:38].strip() else None,
                    'byr' : l[38:42].strip(),
                    's1' : l[42:44].strip(),
                    'sandi' : l[44:49].strip(),
                    'pg' : l[49:53].strip(),
                    'f1' : l[53:55].strip(),
                    'p1' : l[55:57].strip(),
                    'c1' : l[57:59].strip(),
                    'pt' : l[59:62].strip(),
                    'pi' : l[62:65].strip(),
                    'pjk' : l[65:69].strip(),
                    'itm' : int(l[69:73].strip()),
                    'pr' : l[73:81].strip(),
                    'wom' : l[81:90].strip(),
                    'sandi' : l[90:96].strip(),
                    'partnumber' : l[96:117].strip(),
                    'description' : l[117:138].strip().replace('\t','\s').replace('\n','\s'),
                    'duedate' : datetime.strptime(l[138:146].strip(),"%d%b%y") if l[138:146].strip() else None,
                    'qty' : float(l[146:155].strip()),
                    'um' : l[155:158].strip(),
                    'mtu' : l[158:163].strip(),
                    'unitprice' : float(l[163:178].strip()),
                    'extpricerph' : float(l[178:193].strip()),
                    'vendor' : l[193:200].strip(),
                    'vendorname' : l[200:216].strip().replace('\t','\s').replace('\n','\s'),
                    'f2' : l[216:218].strip(),
                    'so' : l[218:221].strip(),
                    'sr' : l[221:224].strip(),
                    # 'text' : l[224:575].strip().replace('\t','\s').replace('\n','\s'),
                    'hs' : l[575:586].strip(),
                    'received' : datetime.strptime(l[586:595].strip(),"%d%b%y") if l[586:595].strip() else None,
                    'inspected' : datetime.strptime(l[595:605].strip(),"%d%b%y") if l[595:605].strip() else None,
                    'stored' : datetime.strptime(l[605:614].strip(),"%d%b%y") if l[605:614].strip() else None,
                    'posts3' : datetime.strptime(l[614:622].strip(),"%d%b%y") if l[614:622].strip() else None,
                    'c2' : l[622:625].strip(),
                    'p2' : l[625:627].strip(),
                    'dokument' : l[627:637].strip(),
                    'engdisp' : l[637:646].strip(),
                    'lifetime' : l[646:656].strip(),
                    'country' : l[656:666].strip(),
                }
                try:
                    obj = IVR7020H(**content)
                    obj.save()
                    # print("insert %s" % i)
                except:
                    pass
                    # print("insert error %s %s" % (content.get('master'),content.get('itm')) )
            i += 1
