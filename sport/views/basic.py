# -*- coding: utf-8 -*-
#

import pdb

import datetime

from flask import session, request, redirect, render_template, url_for

from gettext import gettext as _

from wtforms import (Form, SelectField, DateTimeField, TextAreaField,
                    DecimalField, RadioField, IntegerField, TextField,
                    validators)

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy.sql.expression import func

from sportweb import app
from models import meta, basic, swim, bodydata

from log import index

sport_type_list = [ (0, "swim") ] #, (1, "jogging") ]


class NewPlaceForm(Form):
    place = TextAreaField(_('place'), [ validators.Required() ])
    comment = TextAreaField(_('comment'))
#    last_use = DateTimeField('last_use')

class NewSessionForm(Form):
    place_id = SelectField(_('place'), coerce=int)
    start = DateTimeField(_('start'), 
                            format="%Y-%m-%dT%H:%M:%S",
                            default=datetime.datetime.today, 
                            validators=[validators.Required() ])
    duration = DecimalField(_('duration'), 
                            validators=[validators.Required() ])
    duration_unit = RadioField(_('duration\'s unit'), 
                                choices = [ (0, _("hour")), (1, _("minutes")),
                                            (2, _("seconds")) ],
                                default=1,
                                coerce=int)
    comment = TextAreaField(_('comment'))

class NewSetForm(Form):
       
    sport_type = SelectField(_('sport_type'), coerce=int)
    sequence = IntegerField(_('which set'))
    start = DateTimeField(_('start'), format="%Y-%m-%dT%H:%M:%S",
                            validators=[validators.Optional()])
    duration = DecimalField(_('duration'),
                            validators=[validators.Optional()])
    duration_unit = RadioField(_('duration\'s unit'),
                                choices = [(0, _("hour")), (1, _("minutes")),
                                            (2, _("seconds")) ],
                                default=1,
                                coerce=int)
    comment = TextAreaField(_("comment"))

class SwimForm(Form):
    swim_name = TextField(_('swim_type_name'),
                        validators=[validators.Required(), 
                        validators.length(max=20)])

class SwimDataForm(Form):
    swim_id = SelectField(_('swim_type'), coerce=int)
    distance = IntegerField(_('distance in meters'), 
                                validators=[validators.DataRequired()])
    start = DateTimeField(_('start'), format="%Y-%m-%dT%H:%M:%S",
                                validators=[validators.Optional()])
    duration = DecimalField(_('duration'), validators=[validators.Optional()])
    duration_unit = RadioField(_('duration\'s unit'),
                                choices = [(0, _("hour")), (1, _("minutes")),
                                            (2, _("seconds")) ],
                                default=1,
                                coerce=int)
    comment_swim = TextAreaField(_("comment"))
    effort = IntegerField(_("Effort on scale from 0 to 10"),
                        validators=[validators.Optional(),
                                    validators.NumberRange(min=0, max=10)])
    pulsation = IntegerField(_('Heart beat pulsation by minute'),
                        validators=[validators.Optional(),
                                    validators.NumberRange(min=0, max=300)])
    blood_pressure_systole = IntegerField(_('Blood Pressure systole'),
                        validators=[validators.Optional(),
                                    validators.NumberRange(min=0, max=500)])
    blood_pressure_diastole = IntegerField(_('Blood Pressure diastole'),
                        validators=[validators.Optional(),
                                    validators.NumberRange(min=0, max=450)])
    comment_cardio = TextAreaField(_('Cardio\'s comment'))
                                


def get_new_place_field_list():
    return [ "place", "comment" ]

def get_new_session_field_list():
    return [ "place_id", "start", "duration", "duration_unit", "comment" ]

def get_set_field_list():
    return [ "start", "duration", "duration_unit", "comment" ]

def turn_duration_to_seconds(duration, unit):
    if unit.data == 0:
        return duration.data * 3600
    elif unit.data == 1:
        return duration.data * 60
    elif unit.data == 2:
        return duration.data
    else:
        return False

def add_new_comment(comment):
    """ return id of comment or False"""
    timestamp = datetime.datetime.now()
    if not comment.data:
        return None
    comment_args = { 'comment': comment.data.decode("utf_8"),
                    'timestamp': timestamp 
                    }
    new_comment = basic.Comment(**comment_args)
    meta.session.add(new_comment)
    meta.session.commit()
    return new_comment.id

@app.route('/new_place_add', methods=['GET', 'POST'])
def new_place_add():
    form = NewPlaceForm(request.form)
    if request.method == 'POST' and form.validate():
        comment_id = add_new_comment(form.comment)
        place_args = { 'place': form.place.data.decode("utf_8"),
                        'last_use': datetime.datetime.now(),
                        'comment_id': comment_id
                    }
        new_place = basic.Place(**place_args)
        meta.session.add(new_place)
        meta.session.commit()
        return redirect(url_for('new_session_add'))
    return render_template('new_place.html', form=form)

@app.route('/new_session_add', methods=['GET', 'POST'])
def new_session_add():

    def _get_place_choices_list():
        return [ (choice.id, choice.place) for choice in
                    meta.session.query(basic.Place).all() ]

    form = NewSessionForm(request.form)
    form.place_id.choices = _get_place_choices_list()
    if request.method == 'POST' and form.validate():
        comment_id = add_new_comment(form.comment)
        duration = turn_duration_to_seconds(form.duration, form.duration_unit)
        session_args = { 'place_id': form.place_id.data,
                        'start': form.start.data,
                        'duration': datetime.timedelta(seconds=int(duration))
                        }
        if comment_id:
            session_args['comment_id'] = comment_id

        new_session = basic.Session(**session_args)
        meta.session.add(new_session)
        meta.session.commit()
        session['session_id'] = new_session.id
        return redirect(url_for('add_set_to_session'))
    if not form.place_id.choices:
        return redirect(url_for('new_place_add'))
    return render_template('new_session.html', form=form)

@app.route('/add_set_to_session', methods=['GET', 'POST'])
def add_set_to_session():
    def _get_set_sequence_in_session():
        query = meta.session.query(basic.Set).filter(
                        basic.Set.session_id == session['session_id'])
        if not query.all():
            return 1
        query = meta.session.query(func.max(basic.Set.sequence)).filter(
                        basic.Set.session_id == session['session_id']
                        )[0][0]
        sequence = query + 1
        return sequence
 
    form = NewSetForm(request.form)
    form.sequence.data = _get_set_sequence_in_session()
    form.sport_type.choices = sport_type_list

    if request.method == 'POST' and form.validate():
        set_args = { 'session_id': session['session_id'],
                    'sequence': form.sequence.data
                    }
        if form.start.data:
            set_args['start'] = form.start.data
        if form.duration.data:
            duration = turn_duration_to_seconds(form.duration, 
                                                form.duration_unit)
            set_args['duration'] = datetime.timedelta(seconds=int(duration))
        if form.comment.data:
            comment_id = add_new_comment(form.comment)
            set_args['comment_id'] = comment_id

        new_set = basic.Set(**set_args)
        meta.session.add(new_set)
        meta.session.commit()
        session['set_id'] = new_set.id
        if form.sport_type.data == 0:
            return redirect(url_for('add_swim_to_set'))
    return render_template('add_set_to_session.html', form=form)

@app.route('/new_swim_add', methods=['GET', 'POST'])
def new_swim_add():
    form = SwimForm(request.form)
    if request.method == 'POST' and form.validate():
        swim_args = { 'name': form.swim_name.data }
        new_swim = swim.Swim(**swim_args)
        meta.session.add(new_swim)
        meta.session.commit()
        return redirect(url_for('add_swim_to_set'))
    return render_template('new_swim.html', form=form)

@app.route('/add_swim_to_set', methods=['GET', 'POST'])
def add_swim_to_set():

    def _get_swim_choices_list():
        return [ (choice.id, choice.name) for choice in
                    meta.session.query(swim.Swim).all() ]

    form = SwimDataForm(request.form)
    form.swim_id.choices = _get_swim_choices_list()
    if request.method == 'POST' and form.validate():
        bodydatas_id = None
        if (form.effort.data or form.pulsation.data 
            or form.blood_pressure_systole.data 
            or form.blood_pressure_diastole.data
            or form.comment_cardio.data):

            bodydatas_args = {}
            if form.effort.data:
                bodydatas_args['effort'] = form.effort.data
            if form.pulsation.data:
                bodydatas_args['pulsation'] = form.pulsation.data
            if form.blood_pressure_systole.data:
                bodydatas_args['blood_pressure_systole'] =\
                                        form.blood_pressure_systole.data
            if form.blood_pressure_diastole.data:
                bodydatas_args['blood_pressure_diastole'] =\
                                        form.blood_pressure_diastole.data
            comment_cardio_id = add_new_comment(form.comment_cardio)
            if comment_cardio_id:
                bodydatas_args['comment_cardio_id'] = comment_cardio_id
            
            new_bodydatas = bodydata.Cardio(**bodydatas_args)
            meta.session.add(new_bodydatas)
            meta.session.commit()
            bodydatas_id = new_bodydatas.id

        swimdatas_args = { 'set_id': session['set_id'],
                            'swim_id': form.swim_id.data,
                            'distance': form.distance.data,
                            }
        comment_swim_id = add_new_comment(form.comment_swim)
        if comment_swim_id:
            swimdatas_args['comments_id'] = comment_swim_id
        if form.start.data:
            swimdatas_args['start'] = form.start.data
        if form.duration.data:
            duration = turn_duration_to_seconds(form.duration, 
                                                form.duration_unit)
            swimdatas_args['duration'] = datetime.timedelta(
                                                    seconds=int(duration))

        if bodydatas_id:
            swimdatas_args['bodydata_id'] = bodydatas_id
        new_swimdatas = swim.SwimData(**swimdatas_args)
        meta.session.add(new_swimdatas)
        meta.session.commit()
        session['set_id'] = None
        return redirect(url_for('add_set_to_session'))

    if not form.swim_id.choices:
        return redirect(url_for('new_swim_add'))
    return render_template('add_swim_to_set.html', form=form)

@app.route('/quit_adding_set_to_session')
def quit_adding_set_to_session():
   session['set_id'] = None
   session['session_id'] = None
   return redirect(url_for('index'))


## create filter for fields of wtforms
#def upper_field(value):
#    if value:
#        return value.upper()
#    return value
#
#def lower_field(value):
#    if value:
#        return value.lower()
#    return value
#
#def title_field(value):
#    if value:
#        return value.title()
#    return value
#
## Create new wtforms Fields
#class ColorInput(widgets.TextInput):
#    input_type = "color"
#
#class ColorField(Field):
#    widget = ColorInput()
#    def _value(self):
#        if self.data:
#            return self.data
#
#
#class EmailInput(widgets.TextInput):
#    input_type = "email"
#
#class EmailField(Field):
#    widget = EmailInput()
#    def _value(self):
#        if self.data:
#            return self.data
#
#
#class TelInput(widgets.TextInput):
#    input_type = "tel"
#
#class TelField(Field):
#    widget = TelInput()
#    def _value(self):
#        if self.data:
#            return self.data
#
#
#class DateInput(widgets.TextInput):
#    input_type = "date"
#
#class DateField(Field):
#    widget = DateInput()
#    def _value(self):
#        if self.data:
#            return self.data
#
#class TimeInput(widgets.TextInput):
#    input_type = "time"
#
#class TimeField(Field):
#    widget = TimeInput()
#    def _value(self):
#        if self.data:
#            return self.data
#
#
## Generic Forms
#class PhoneForm(Form):
#    phonename = TextField('phonename', validators=[validators.Optional()])
#    phonenum = TextField('phonenum', [validators.Optional()])
#
#class AddressForm(Form):
#    address_id = TextField('address_id')
#    street = TextField('street', validators=[validators.Optional(),
#                                 validators.Length(max=50, message=_("""Number
#                                 and street must be less than 50 characters 
#                                 please"""))])
#    building = TextField('building', validators=[validators.Optional(), 
#                                     validators.Length(max=50)])
#    city = TextField('city', validators=[validators.Optional(),
#                             validators.Length(max=25,
#                             message=_("City's name"))], 
#                             filters=[title_field])
#    postal_code = TextField('postal_code')
#    county = TextField('county', validators=[validators.Optional(), 
#                                  validators.Length(max=15)], 
#                                 filters=[title_field])
#    country = TextField('country', validators=[validators.Optional(),
#                                   validators.Length(max=15)],
#                                   filters=[title_field])
#
#class MailForm(Form):
#    email = TextField('email', validators=[validators.Optional(),
#                                      validators.Email()],
#                                      filters=[lower_field])
#
## verify the user is allowed to update
#def _check_body_perm(body, body_type):
#    """ Return True if the odontux user trying to perform an
#        update on administrative data is allowed.
#        Otherwise, return False
#    """
#    # Only ADMIN (and own body) may update infos
#    if body_type == 'user':
#        if session['role'] != constants.ROLE_ADMIN \
#        and session['username'] != body.username:
#            return False
#    # Only ADMIN may update dental_office infos        
#    elif body_type == 'dental_office':
#        if session['role'] != constants.ROLE_ADMIN:
#            return False
#    # DENTISTS, NURSE, ASSISTANT, SECRETARIES can make update in 
#    # administration patient's files.
#    elif body_type == 'md':
#        if session['role'] == constants.ROLE_ADMIN:
#            return False
#    elif body_type == 'patient':
#        if session['role'] == constants.ROLE_ADMIN:
#            return False
#    else:
#        raise Exception(_("Unknown body type"))
#        return False
#    return True
#
## Get body information in the database
#def _get_body(body_id, body_type):
#    """ Return sqlalchemy object representing the person in database
#        we want to update ; could be a patient, an OdontuxUser, a
#        medecine doctor.
#    """
#    if body_type == 'user':
#        body = meta.session.query(users.OdontuxUser).filter\
#            (users.OdontuxUser.id == body_id).one()
#    elif body_type == 'md':
#        body = meta.session.query(md.MedecineDoctor).filter\
#            (md.MedecineDoctor.id == body_id).one()
#    elif body_type == 'patient':
#        body = meta.session.query(administration.Patient).filter\
#            (administration.Patient.id == body_id).one()
#    elif body_type == "dental_office":
#        body = meta.session.query(users.DentalOffice).filter\
#            (users.DentalOffice.id == body_id).one()
#    else:
#        raise Exception(_("please specify known body_type"))
#    return body
#
#def update_body_address(body_id, body_type):
#    """ An address exists for body in database but is erroneus (typo, wrong 
#        town, anything) : this function will update the address to right thing.
#    """
#    body = _get_body(body_id, body_type)
#    if not _check_body_perm(body, body_type):
#        return False
#    form = AddressForm(request.form)
#    address_index = int(request.form["address_index"])
#    if request.method == 'POST' and form.validate():
#        for f in address_fields:
#            if body_type == "patient":
#                setattr(body.family.addresses[address_index], f, 
#                        getattr(form, f).data)
#                meta.session.commit()
#                # update address in gnucash for patient.
#                comptability = gnucash_handler.GnuCashCustomer(body.id,
#                                                 body.dentist_id)
#                customer = comptability.update_customer()
#            else:
#                setattr(body.addresses[address_index], f, 
#                        getattr(form, f).data)
#                meta.session.commit()
#        return True
#        
#def add_body_address(body_id, body_type):
#    body = _get_body(body_id, body_type)
#    if not _check_body_perm(body, body_type):
#        return False
#    form = AddressForm(request.form)
#    if request.method == 'POST' and form.validate():
#        args = {f: getattr(form, f).data for f in address_fields}
#        if body_type == "patient":
#            body.family.addresses.append(administration.Address(**args))
#            meta.session.commit()
#            # in gnucash
#            comptability = gnucash_handler.GnuCashCustomer(body.id,
#                                                          body.dentist_id)
#            customer = comptability.update_customer()
#        else:
#            body.addresses.append(administration.Address(**args))
#            meta.session.commit()
#        return True
#
#def delete_body_address(body_id, body_type):
#    body = _get_body(body_id, body_type)
#    if not _check_body_perm(body, body_type):
#        return False
#    form = AddressForm(request.form)
#    address_id = int(request.form['address_id'])
#    if request.method == 'POST' and form.validate():
#        address = meta.session.query(administration.Address)\
#                .filter(administration.Address.id == address_id).one()
#        meta.session.delete(address)
#        meta.session.commit()
#        return True
#
#def update_body_phone(body_id, body_type):
#    body = _get_body(body_id, body_type)
#    if not _check_body_perm(body, body_type):
#        return False
#    form = PhoneForm(request.form)
#    phone_index = int(request.form["phone_index"])
#    if request.method == 'POST' and form.validate():
#        for (f,g) in phone_fields:
#            setattr(body.phones[phone_index], g, getattr(form, f).data)
#        meta.session.commit()
#        return True 
#    
#
#def add_body_phone(body_id, body_type):
#    body = _get_body(body_id, body_type)
#    if not _check_body_perm(body, body_type):
#        return False
#    form = PhoneForm(request.form)
#    if request.method == 'POST' and form.validate():
#        args = { g: getattr(form, f).data for f, g in phone_fields }
#        body.phones.append(administration.Phone(**args))
#        meta.session.commit()
#        return True
#
#def delete_body_phone(body_id, body_type):
#    body = _get_body(body_id, body_type)
#    if not _check_body_perm(body, body_type):
#        return False
#    form = PhoneForm(request.form)
#    phone_id = int(request.form["phone_id"])
#    if request.method == 'POST' and form.validate():
#        try:
##            phone = (
##                meta.session.query(administration.Phone)
##                    .filter(and_(
##                        and_(
##                            administration.Phone.name == form.phonename.data,
##                            administration.Phone.number == form.phonenum.data
##                        ),
##                        administration.Phone.id == phone_id)
##                    )
##                ).one()
#            phone = meta.session.query(administration.Phone)\
#                    .filter(administration.Phone.id == phone_id).one()
#            meta.session.delete(phone)
#            meta.session.commit()
#            return True
#        except:
#            raise Exception("phone delete problem")
#
#def update_body_mail(body_id, body_type):
#    body = _get_body(body_id, body_type)
#    if not _check_body_perm(body, body_type):
#        return False
#    form = MailForm(request.form)
#    mail_index = int(request.form["mail_index"])
#    if request.method == 'POST' and form.validate():
#        for f in mail_fields:
#            setattr(body.mails[mail_index], f, getattr(form, f).data)
#        meta.session.commit()
#        return True
#
#def add_body_mail(body_id, body_type):
#    body = _get_body(body_id, body_type)
#    if not _check_body_perm(body, body_type):
#        return False
#    form = MailForm(request.form)
#    if request.method == 'POST' and form.validate():
#        args = {f: getattr(form, f).data for f in mail_fields }
#        body.mails.append(administration.Mail(**(args)))
#        meta.session.commit()
#        return True
#
#def delete_body_mail(body_id, body_type):
#    body = _get_body(body_id, body_type)
#    if not _check_body_perm(body, body_type):
#        return False
#    form = MailForm(request.form)
#    mail_id = int(request.form['mail_id'])
#    if request.method == 'POST' and form.validate():
#        mail = meta.session.query(administration.Mail)\
#                .filter(administration.Mail.id == mail_id).one()
#        meta.session.delete(mail)
#        meta.session.commit()
#        return True
