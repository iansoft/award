from django.http import HttpResponse,JsonResponse, HttpResponseNotFound
from django.template import RequestContext, loader
import json
import datetime
import os
import random
import math
from django.db import connection

def index(request):
    template = loader.get_template('dashboard/index.html')
    context = RequestContext(request,{})
    return HttpResponse(template.render(context))

def get_awards(request):
    level = int(request.GET["level"])
    award_count = 0
    award_students = []
    student_pool_index = 0

    #get the students that never selected
    student_pool = get_award_source()
    #get the students count
    student_pool_count = len(student_pool)

    if level == 1: #award 1
        award_count = 1
    elif level ==2: #award 2
        award_count = 3
    elif level ==3: #award 3
        award_count = 5
    elif level == 4: #award 4
        award_count = 20
    else: #nothing
        pass

    for i in range(0,award_count):
        student_pool_index = random.randint(0,student_pool_count)
        #add the award students
        award_students.append(student_pool[student_pool_index])

    #print award_students
    # print ""
    # print "====the result======"
    # print award_students
    award_dict = {"students": award_students}
    return JsonResponse(award_dict)


def get_award_source():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students WHERE status = 0")
    students = cursor.fetchall()
    return students

def record_selected_students(request):
    if request.method == 'GET':
        print ""
        print "====POST======"
        req = json.loads(request.raw_get_data)
        print req

    award_dict = {"students": "heheh"}
    return JsonResponse(award_dict)


def init_db(request):
    cursor = connection.cursor();
    #first of all: delete all the students
    cursor.execute("DELETE FROM students")

    for i in range(1,49):
        strCount = str(i);
        if i<10:
            strCount = "0" + strCount
        sql = ("INSERT INTO students VALUES (%s,%s,%s)" % (strCount, "80"+strCount, str(0)))
        print sql
        cursor.execute(sql);
    cursor.execute("SELECT * FROM students")
    row = cursor.fetchall()
    print row
    print type(row)
    vsm_status_dict = {"students":row}
    return JsonResponse(vsm_status_dict)