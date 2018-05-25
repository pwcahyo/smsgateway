# sms/view.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from .forms import SendSMSForm
from dal import autocomplete
from .models import Person, Job, Major, NextMajor, School, Parent, Inbox, Outbox, MessageStatus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import gammu
import sys

def index(request):
    """Write SMS Function"""

    # Start Pagination
    outbox = Outbox.objects.select_related().all().order_by('-time')
    page = request.GET.get('page', 1)

    paginator = Paginator(outbox, 10)
    try:
        outboxs = paginator.page(page)
    except PageNotAnInteger:
        outboxs = paginator.page(1)
    except EmptyPage:
        outboxs = paginator.page(paginator.num_pages)
    #End Pagination

    if request.method == 'POST':
        form = SendSMSForm(request.POST)
        save_sms = form.save(commit=False)

        if form.is_valid():
            if(save_sms.person_id != None):
                #single sms
                array_person = Person.objects.filter(id=save_sms.person_id).values_list('id','phone','school_id','major_id','graduate_id')
                BulkSMS(form, array_person)
            elif(save_sms.school_id!=None and save_sms.major_id!=None and save_sms.graduate_id!=None):
                # school = true, major = true, graduate = true
                array_person = Person.objects.filter(school_id=save_sms.school_id, major_id=save_sms.major_id, graduate_id=save_sms.graduate_id).values_list('id','phone','school_id','major_id','graduate_id')
                BulkSMS(form, array_person)
            elif(save_sms.school_id!=None and save_sms.major_id!=None and save_sms.graduate_id==None):
                # school = true, major = true, graduate = false
                array_person = Person.objects.filter(school_id=save_sms.school_id, major_id=save_sms.major_id).values_list('id','phone','school_id','major_id','graduate_id')
                BulkSMS(form, array_person)
            elif(save_sms.school_id!=None and save_sms.major_id==None and save_sms.graduate_id!=None):
                # school = true, major = false, graduate = true
                array_person = Person.objects.filter(school_id=save_sms.school_id, graduate_id=save_sms.graduate_id).values_list('id','phone','school_id','major_id','graduate_id')
                BulkSMS(form, array_person)
            elif(save_sms.school_id==None and save_sms.major_id!=None and save_sms.graduate_id!=None):
                # school = false, major = true, graduate = true
                array_person = Person.objects.filter(major_id=save_sms.major_id, graduate_id=save_sms.graduate_id).values_list('id','phone','school_id','major_id','graduate_id')
                BulkSMS(form, array_person)
            elif(save_sms.graduate_id!=None):
                # school = false, major = false, graduate = true
                array_person = Person.objects.filter(graduate_id=save_sms.graduate_id).values_list('id','phone','school_id','major_id','graduate_id')
                BulkSMS(form, array_person)
            elif(save_sms.school_id!=None):
                # school = true, major = false, graduate = false
                array_person = Person.objects.filter(school_id=save_sms.school_id).values_list('id','phone','school_id','major_id','graduate_id')
                BulkSMS(form, array_person)
            elif(save_sms.major_id!=None):
                # school = false, major = true, graduate = false
                array_person = Person.objects.filter(major_id=save_sms.major_id).values_list('id','phone','school_id','major_id','graduate_id')
                BulkSMS(form, array_person)
            return HttpResponseRedirect('/')

        else:
            return HttpResponseRedirect('/')
    else:
        form = SendSMSForm()

    return render(request, 'sms/index.html', {'form': form, 'outbox': outboxs})

def BulkSMS(form, array_person):
    # Function Broadcast SMS 

    #Gammu 
    sm = gammu.StateMachine()
    sm.ReadConfig()
    sm.Init()
    #End Gammu

    data = form.save(commit=False)
    pesan = data.text
    data = []
    for data_person in array_person:
        message = {
        'Text': pesan,
        'SMSC': {'Location': 1},
        'Number': data_person[1],
        }

        person_id = data_person[0]
        school_id = data_person[2]
        major_id = data_person[3]
        graduate_id = data_person[4]
        text = pesan

        try:
          # Send SMS if all is OK
          sm.SendSMS(message)
          print('Success, SMS was Sent')
          status = MessageStatus.objects.get(id=2) # 2 : Terkirim

        except gammu.GSMError:
            # Show error if message not sent
            print('Error, SMS not Sent')
            status = MessageStatus.objects.get(id=1) # 1 : Tidak Terkirim

        sms = Outbox(person_id=person_id,text=text,status=status,school_id=school_id,major_id=major_id,graduate_id=graduate_id)
        data.append(sms)
    Outbox.objects.bulk_create(data)

def delete(request, pk):
    sms = Outbox.objects.get(pk=pk)
    sms.delete()
    return HttpResponseRedirect('/')