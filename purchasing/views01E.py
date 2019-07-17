import io
import xlwt
from django.shortcuts import render, redirect
from django.db.models import F,Q,Max,Prefetch
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from purchasing.models import *
from datetime import datetime

def in71_export_prn(b,e):
    # prn = io.StringIO()
    objs = TMIN71.objects.filter(Q(d_create__gte=b) & Q(d_create__lte=e))
    """
    PO......TGLDATINVOICE-NO..........PACKLIST............BOX-NO....RCV-BYCERT....OTHER........................AWB.................TGL...HAWB........TGL...TGL...BPBI/BPBL...........NATGL-BCNOMOR-AJU.................TGL...TGLAPRNIKAPRC
    PO990001190524123456789012345678901234567890123456789012345678907374031234567812345678901234567890123456789123456789012345678901905241234567890121905241905281234567890123456789012123456123456789012345678901234561234561234561234561
    PO00000119052412345678901234567890123456789012345678901234567890737403123456781234567890123456789012345678912345678901234567890190524                  190528                    12123456123456789012345678901234561234561234561234561
    PO040001190524123456789012345678901234567890123456789012345678907374031234567812345678901234567890123456789123456789012345678901905241234567890121905241905281234567890123456789012190524123456789012345678901234561905241905287374031
    OK......OK....OK..................OK..................OK........OK....OK......OK...........................12345678901234567890OK....OK..........OK....OK....OK..................OK......OK........................OK....1234561234561
    """
    prn = "PO......TGLDATINVOICE-NO..........PACKLIST............BOX-NO....RCV-BYCERT....OTHER........................AWB.................TGL...HAWB........TGL...TGL...BPBI/BPBL...........NATGL-BCNOMOR-AJU.................TGL...TGLAPRNIKAPRC\n"
    for o in objs:
        prn += "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}\n".format(
            o.c_po.upper(),
            o.d_received.strftime("%y%m%d"),
            o.c_invoice.ljust(20),
            o.c_packinglist.ljust(20),
            o.c_boxno.ljust(10),
            o.c_nik.ljust(6),
            o.e_certificate.ljust(8),
            o.e_other.ljust(29),
            o.c_awb.ljust(20),
            o.d_awb.strftime("%y%m%d") if o.d_awb else ''.ljust(6),
            o.c_hawb.ljust(12),
            o.d_hawb.strftime("%y%m%d") if o.d_awb else ''.ljust(6),
            o.d_create.strftime("%y%m%d") if o.d_awb else ''.ljust(6),
            o.c_bc23.ljust(20),
            o.c_negaraasal or ''.ljust(2),
            o.d_bc23.strftime("%y%m%d") if o.d_awb else ''.ljust(6),
            o.c_aju.ljust(26),
            o.d_aju.strftime("%y%m%d") if o.d_awb else ''.ljust(6),
            o.d_appr.strftime("%y%m%d") if o.d_awb else ''.ljust(6),
            o.c_nikappr.ljust(6) or ''.ljust(6),
            'Y' if o.b_isclosedr else ' '
        )
    return prn

def in72_export_prn(b,e):
    # prn = io.StringIO()
    def try_except(tr,ex):
        try:
            return tr
        except:
            return ex

    objs = TMIN72.objects.select_related('tmin73','f_in71').filter(Q(d_create__gte=b) & Q(d_create__lte=e))
    """
    PO......TGLDATITMSESHIP...DAT....PARTIN..............BY....TGLAPRNIKAPR
    12345678123456123111234567123456712345678901234567890123456123456123456
    PO990001123456123111234567123456712345678901234567890123456123456123456
    PO990001190524123111234567123456712345678901234567890123456123456123456
    PO990001190524001110000100000020012345678901234567890123456123456123456
    PO9900011905240011100001000000100                    737403190618737403
    PO9900011905240011100001000000100600220484           737403190618737403
    PO9800091906180021100001000000100                    737403190618737403
    ok......ok....ok.oook...,,DAT....PARTIN..............BY....TGLAPRNIKAPR
    """
    prn = "PO......TGLDATITMSESHIP...DAT....PARTIN..............BY....TGLAPRNIKAPR\n"
    for o in objs:
        prn += "{}{}{}{}{}{}{}{}{}{}{}\n".format(
            o.f_in71.c_po.upper(),
            o.f_in71.d_received.strftime("%y%m%d"),
            str(o.i_itemno).rjust(3,'0'),
            getattr(getattr(o,'tmin73',' '),'c_cert',' '),
            getattr(getattr(o,'tmin73',' '),'c_e',' '),
            str("%08.2f"%o.i_qship).replace(',','').replace('.',''),
            str("%08.2f"%o.i_qreceived).replace(',','').replace('.',''),
            o.c_partin.ljust(20),
            o.c_nik or ''.ljust(6),
            o.d_appr.strftime("%y%m%d"),
            o.c_nikappr or ''.ljust(6),
        )
    return prn
