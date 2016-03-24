# coding=utf-8
from django import forms
from popular_proposal.models import ProposalTemporaryData
from votainteligente.send_mails import send_mail
from django.utils.translation import ugettext as _


WHEN_CHOICES = [
    ('1_month', u'1 mes después de ingresado'),
    ('6_months', u'6 Meses'),
    ('1_year', u'1 año'),
    ('2_year', u'2 años'),
    ('3_year', u'3 años'),
    ('4_year', u'4 años'),
]


class ProposalForm(forms.Form):
    problem = forms.CharField(label=_(u'Según la óptica de tu organización, describe un problema de tu comuna que quieras solucionar. líneas)'),
        help_text=_(u'Ej: Poca participación en el Plan Regulador, falta de transparencia en el trabajo de la municipalidad, pocos puntos de reciclaje, etc.'))
    solution = forms.CharField(label=_(u'Qué quieres que haga tu autoridad para solucionar el problema? (3 líneas)'),
        help_text=_(u'Ejemplo: "Que se aumenten en 30% las horas de atención de la especialidad Cardiología en los Cesfam y consultorios de la comuna", "Que se publiquen todos los concejos municipales en el sitio web del municipio".'))
    when = forms.ChoiceField(choices=WHEN_CHOICES, label=_(u'¿En qué plazo te gustaría que esté solucionado?'))
    allies = forms.CharField(label=_(u'¿Quiénes son tus posibles aliados?'))

    def __init__(self, *args, **kwargs):
        self.proposer = kwargs.pop('proposer')
        self.area = kwargs.pop('area')
        super(ProposalForm, self).__init__(*args, **kwargs)

    def save(self):
        return ProposalTemporaryData.objects.create(proposer=self.proposer,
                                                    area=self.area,
                                                    data=self.cleaned_data)


class CommentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.temporary_data = kwargs.pop('temporary_area')
        self.moderator = kwargs.pop('moderator')
        super(CommentsForm, self).__init__(*args, **kwargs)
        for field in self.temporary_data.comments.keys():
            self.fields[field] = forms.CharField(required=False)

    def save(self, *args, **kwargs):
        for field_key in self.cleaned_data.keys():
            self.temporary_data.comments[field_key] = self.cleaned_data[field_key]
        self.temporary_data.save()
        comments = {}
        for key in self.temporary_data.data.keys():
            if self.temporary_data.comments[key]:
                comments[key] = {
                    'original': self.temporary_data.data[key],
                    'comments': self.temporary_data.comments[key]
                }
        mail_context = {
            'area': self.temporary_data.area,
            'temporary_data': self.temporary_data,
            'moderator': self.moderator,
            'comments': comments
        }
        send_mail(mail_context, 'popular_proposal_moderation', to=[self.temporary_data.proposer.email])
        return self.temporary_data
