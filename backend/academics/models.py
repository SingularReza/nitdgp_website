from django.db import models
from base.models import BaseModel
import datetime


class NoticeType(BaseModel):
    notice_type = models.CharField(max_length=255, default="general")

    def __str__(self):
        return self.notice_type


class Notice(BaseModel):
    title = models.CharField(max_length=512)
    notice_type = models.ForeignKey(NoticeType, on_delete=models.CASCADE)
    file = models.FileField(upload_to='academics/notices/%Y/%m/%d')
    date = models.DateField()

    def __str__(self):
        return self.title

    def _file(self):
        return self.file

    def _date(self):
        return self.date

    def _notice_type(self):
        return self.notice_type.notice_type

    class Meta:
        ordering = ('-date',)


def rename_calendar(instance, filename):
    return 'academics/calendar/{1}/'.format(instance.year, filename)


class Calendar(BaseModel):
    YEAR_CHOICES = [(str(r)+'-'+str(r+1), str(r)+'-'+str(r+1)) for r in range(1965, datetime.date.today().year+1)]
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, default=str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().year + 1))
    file = models.FileField(upload_to=rename_calendar)

    def __str__(self):
        return "Academic Calendar for year " + self.year


class AdmissionDegree(BaseModel):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def _description(self):
        return self.description


class AdmissionProgramme(BaseModel):
    degree = models.ForeignKey(AdmissionDegree, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)

    def _degree(self):
        return self.degree.name

    def __str__(self):
        return self.name

    def _description(self):
        return self.description


def rename_admission_file(instance, filename):
    return 'academics/admission/{0}/{1}/{2}'.format(instance.programme.degree.name, instance.programme.name, filename)


class Admission(BaseModel):
    programme = models.ForeignKey(AdmissionProgramme, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=rename_admission_file)

    def _programme(self):
        return self.programme.name

    def _title(self):
        return self.title

    def _file(self):
        return self.file


def rename_examination_file(instance, filename):
    print(filename)
    return 'academics/examination/{0}/{1}'.format(instance.year, filename)


class Examination(BaseModel):
    CURRENT_YEAR = datetime.date.today().year
    YEAR_CHOICES = [(str(r)+'-'+str(r+1), str(r)+'-'+str(r+1)) for r in range(1965, CURRENT_YEAR+1)]
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, default=str(CURRENT_YEAR)+'-'+str(CURRENT_YEAR + 1))
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=rename_examination_file)

    def __str__(self):
        return self.title

    def _year(self):
        return self.year

    def _file(self):
        return self.file


class Document(BaseModel):
    CHOICES = (('Verification', 'Verification'), ('Transcript', 'Transcript'))
    type = models.CharField(choices=CHOICES, max_length=30)
    filename = models.FileField(upload_to='academics/documents')
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def _type(self):
        return self.type

    def _filename(self):
        return self.filename


class Regulation(BaseModel):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='academics/regulations/%Y')

    def __str__(self):
        return self.title

    def _file(self):
        return self.file


class Registration(BaseModel):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='academics/registrations/%Y')

    def __str__(self):
        return self.title

    def _file(self):
        return self.file


class Convocation(BaseModel):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='academics/convocation/%Y')

    def __str__(self):
        return self.title

    def _file(self):
        return self.file
