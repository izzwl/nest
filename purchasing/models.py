import datetime
from django.db import models
from django.dispatch import receiver
from django.utils.deconstruct import deconstructible
from django.core.validators import MaxValueValidator
from django.utils import timezone

CH_NEGARA_ASAL = (
    ('US','US'),
    ('UK','UK'),
    ('SG','SG'),
    ('ID','ID'),
    ('AU','AU'),
    ('CA','CA'),
    ('UA','UA'),
    ('GM','GM'),
    ('MY','MY'),
    ('JP','JP'),
    ('PH','PH'),
    ('DK','DK'),
    ('IR','IR'),
    ('ES','ES'),
    ('SE','SE'),
    ('HK','HK'),
)

class IVR7020H(models.Model):
    master = models.CharField(max_length=8)
    po = models.CharField(max_length=25)
    created = models.DateField(null=True,blank=True)
    byr = models.CharField(max_length=3)
    s1 = models.CharField(max_length=1)
    sandi = models.CharField(max_length=4)
    pg = models.CharField(max_length=2)
    f1 = models.CharField(max_length=1)
    p1 = models.CharField(max_length=1)
    c1 = models.CharField(max_length=1)
    pt = models.CharField(max_length=1)
    pi = models.CharField(max_length=3)
    pjk = models.CharField(max_length=3)
    itm = models.PositiveIntegerField()
    pr = models.CharField(max_length=8)
    wom = models.CharField(max_length=6)
    sandi = models.CharField(max_length=4)
    partnumber = models.CharField(max_length=25)
    description = models.CharField(max_length=25)
    duedate = models.DateField(null=True,blank=True)
    qty = models.FloatField()
    um = models.CharField(max_length=2)
    mtu = models.CharField(max_length=3)
    unitprice = models.FloatField()
    extpricerph = models.FloatField()
    vendor = models.CharField(max_length=6)
    vendorname = models.CharField(max_length=25)
    f2 = models.CharField(max_length=2)
    so = models.CharField(max_length=2)
    sr = models.CharField(max_length=2)
    # text = models.CharField(max_length=255)
    hs = models.CharField(max_length=15)
    received = models.DateField(null=True,blank=True)
    inspected = models.DateField(null=True,blank=True)
    stored = models.DateField(null=True,blank=True)
    posts3 = models.DateField(null=True,blank=True)
    c2 = models.CharField(max_length=1)
    p2 = models.CharField(max_length=1)
    dokument = models.CharField(max_length=20)
    engdisp = models.CharField(max_length=20)
    lifetime = models.CharField(max_length=25)
    country = models.CharField(max_length=25)

    class Meta:
        unique_together = [
            ['master', 'itm']
        ]

class TMIN71(models.Model):
    d_create = models.DateField(null=True,blank=True)
    c_nik = models.CharField(max_length=6,blank=True)
    c_nikappr = models.CharField(max_length=6,blank=True)
    c_po = models.CharField(max_length=8,blank=True)
    d_received = models.DateField(null=True,blank=True)
    b_isclosedr = models.BooleanField(default=False,blank=True)
    c_invoice = models.CharField(max_length=20,blank=True)
    c_packinglist = models.CharField(max_length=20,blank=True)
    c_boxno = models.CharField(max_length=10,blank=True)
    e_certificate = models.CharField(max_length=8,blank=True)
    e_other = models.CharField(max_length=29,blank=True)
    c_negaraasal = models.CharField(max_length=2,choices=CH_NEGARA_ASAL,blank=True)
    c_awb = models.CharField(max_length=20,blank=True)
    d_awb = models.DateField(null=True,blank=True)
    c_hawb = models.CharField(max_length=12,blank=True)
    d_hawb = models.DateField(null=True,blank=True)
    c_bc23 = models.CharField(max_length=20,blank=True)
    d_bc23 = models.DateField(null=True,blank=True)
    c_aju = models.CharField(max_length=29,blank=True)
    d_aju = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.c_po+"-"+self.d_received.strftime("%d %m %y")

    class Meta:
        unique_together = [
            ['c_po', 'd_received']
        ]
        permissions = (
            ('approve_tmin71','Can Approve TMIN71'),
            ('print_tmin71','Can Print TMIN71'),
        )
        ordering = ['-c_po','-d_create','-d_received']

class TMIN72(models.Model):
    d_create = models.DateField(null=True,blank=True)
    f_in71 = models.ForeignKey(TMIN71, on_delete=models.CASCADE)
    c_nik = models.CharField(max_length=6,blank=True)
    c_nikappr = models.CharField(max_length=6,blank=True)
    i_itemno = models.PositiveIntegerField(blank=True)
    i_qreceived = models.FloatField(blank=True)
    i_qship = models.FloatField(blank=True)
    n_um = models.CharField(max_length=2,blank=True)
    c_partnumber = models.CharField(max_length=20,blank=True)
    c_partin = models.CharField(max_length=20,blank=True)
    c_asterik = models.CharField(max_length=1,blank=True)

    def __str__(self):
        return "ITEM %s - %s : %s %s"%(self.i_itemno,self.c_partnumber,self.i_qship,self.n_um)

    class Meta:
        unique_together = [
            ['f_in71', 'i_itemno']
        ]
        permissions = (
            ('approve_tmin72','Can Approve TMIN72'),
        )
CH_CERT = (
    ('1','1 - Manual / Brocure'),('2','2 - Cert of Warranty'),
    ('3','3 - Engine Document'),('4','4 - Cert of Calibration'),
    ('5','5 - Cert of Origin'),('6','6 - Cert of Test / T Rep'),
    ('7','7 - Cert of Comformance'),('8','8 - Cert of Analys'),
    ('9','9 - Cert of Airworthines'),('A','A - Cert of Mech Char'),
    ('B','B - Form FAA 8130-4'),('C','C - Form FAA 8130-3'),
    ('D','D - EASA Form 1'),('E','E - Form FAA 8130-3 & DAAO 21-18'),
    ('F','F - EASA Form 1 & DAAO 21-18'),('G','G - TCCA 24-0078'),
    ('H','H - Dual EASA Form 1 & FAA 8130-3'),('I','I - DAAO 21-18'),
    ('J','J - Hydrostatic Test Result'),('K','K - Burst Test Result'),
    ('L','L - ECER110 & OR ISO 11439'),('M','M - Cert of Material'),
    ('N','N - IDS (Inspection Data Sheet)'),
    ('O','O - DUAL (FAA 8130-3 & EASA F1 or FAA 8130-3 Only'),
    ('P','P - DUAL (FAA 8130-3 & EASA F1 or EASA Form Only'),
    ('Q','Q - FAA 8130-3 or EASA Form 1'),('R','R - Ok for Assy'),
)
CH_ELIGIBILITY = (
    ('1','1 - DGCA'),('2','2 - FAA'),('3','3 - EASA'),('4','4 - FAA & EASA'),
    ('5','5 - DGCA & FAA'),('6','6 - DGCA & EASA'),('7','7 - ALL AUTHORITY'),
    ('8','8 - N/A'),
)
CH_COND = (
    ('0','0 - Unserviceable'),('1','1 - New'),('2','2 - Farm Out'),
    ('3','3 - Repair In House'),('4','4 - OHC'),('5','5 - Serviceable'),
    ('6','6 - Repairable for Trading'),('7','7 - Repair / Modified'),
    ('8','8 - Inspected / New'),('9','9 - Inspected / As Remove'),
    (' ','  - Unserviceable'),
)
class TMIN73(models.Model):
    d_create = models.DateField(null=True,blank=True)
    f_in72 = models.OneToOneField(TMIN72, on_delete=models.CASCADE)
    c_nik = models.CharField(max_length=6,blank=True)
    c_asterik = models.CharField(max_length=1,blank=True)
    i_qacc = models.FloatField(null=True,blank=True)
    c_cert = models.CharField(max_length=1,choices=CH_CERT)
    c_e = models.CharField(max_length=1,choices=CH_ELIGIBILITY)
    c_cond = models.CharField(max_length=1,choices=CH_COND)

    def __str__(self):
        return "ITEM %s - %s : %s %s"%(self.f_in72.i_itemno,self.f_in72.c_partnumber,self.i_qacc,self.f_in72.n_um)

    class Meta:
        permissions = (
            ('approve_tmin73','Can Approve TMIN73'),
        )

class TMIN75(models.Model):
    d_create = models.DateField(null=True,blank=True)
    f_in73 = models.OneToOneField(TMIN73, on_delete=models.CASCADE)
    c_nik = models.CharField(max_length=6,blank=True)
    c_ciridap = models.CharField(max_length=10,blank=True)
    c_owner = models.CharField(max_length=3)
    c_bin = models.CharField(max_length=10)
    c_recvno = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])

    def __str__(self):
        return "V"+self.d_create.strftime("%y")+str(self.c_recvno).zfill(5)


class TMIN76(models.Model):
    d_release = models.DateField()
    f_in73 = models.OneToOneField(TMIN73, on_delete=models.CASCADE)
    c_nik = models.CharField(max_length=6,blank=True)
    i_qreject = models.FloatField(null=True,blank=True)
    c_npo = models.CharField(max_length=1,blank=True)
    c_drno = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    c_sts = models.PositiveIntegerField(validators=[MaxValueValidator(9)])

    def __str__(self):
        return "D"+self.d_release.strftime("%y")+str(self.c_npo)+str(self.c_drno).zfill(4)
