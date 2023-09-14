from bs4 import BeautifulSoup

html = """
<div class="col-sm text-center" id="Saturday"><div class="day sticky"><h5><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Sabbath</font></font></h5><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">16/09/2023</font></font></div><div class="time box-day">
<h5 class="bottom-details"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Pilates equipment</font></font></h5>
<span class="top-title-d"><i class="fas fa-chevron-left rotate"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9:00 | </font><font style="vertical-align: inherit;">50 minutes</font></font></span>
<div class="bottom-details"><p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Instructor: Diana Wegman</font></font></p>
<p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Pilates equipment</font></font></p><a href="#pills-tab" class="bt registerGuest" data-object="0" data-status="3" data-instruction="169" data-time="090000" data-lessonid="10364" data-date="2023/9/16" data-durationinminutes="50" data-desc=" " data-location="פילאטיס מכשירים" data-teacher="דיאנה ווגמן" data-lessonname="פילאטיס מכשירים" data-toggle="modal" data-target="#guest-reg-form"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">to register</font></font></a>
</div>
</div><div class="time box-day">
<h5 class="bottom-details"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Pilates equipment</font></font></h5>
<span class="top-title-d"><i class="fas fa-chevron-left rotate"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9:00 | </font><font style="vertical-align: inherit;">50 minutes</font></font></span>
<div class="bottom-details"><p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Instructor: Milena Shneor</font></font></p>
<p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Pilates equipment</font></font></p><a href="#pills-tab" class="bt registerGuest" data-object="0" data-status="3" data-instruction="126" data-time="090000" data-lessonid="200172" data-date="2023/9/16" data-durationinminutes="50" data-desc=" " data-location="פילאטיס מכשירים" data-teacher="מילנה שניאור" data-lessonname="פילאטיס מכשירים" data-toggle="modal" data-target="#guest-reg-form"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">to register</font></font></a>
</div>
</div><div class="time box-day">
<h5 class="bottom-details"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">yoga</font></font></h5>
<span class="top-title-d"><i class="fas fa-chevron-left rotate"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">9:15 | </font><font style="vertical-align: inherit;">70 min</font></font></span>
<div class="bottom-details"><p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Instructor: Milena Solomon</font></font></p>
<p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Studio 2</font></font></p><a href="#pills-tab" class="bt registerGuest" data-object="0" data-status="6" data-instruction="267" data-time="091500" data-lessonid="10173" data-date="2023/9/16" data-durationinminutes="70" data-desc="yoga vinyasa 
השילוב באידיאלי בין גוף נפש, באמצעות נשימות , תנועות הרפיה וריכוז" data-location="סטודיו 2" data-teacher="מילנה סולומון" data-lessonname="יוגה" data-toggle="modal" data-target="#guest-reg-form"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">to register</font></font></a>
</div>
</div><div class="time box-day">
<h5 class="bottom-details"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Spinning</font></font></h5>
<span class="top-title-d"><i class="fas fa-chevron-left rotate"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10:00 | </font><font style="vertical-align: inherit;">50 minutes</font></font></span>
<div class="bottom-details"><p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Instructor: Mittal Yehezkel</font></font></p>
<p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Spinning</font></font></p><a href="#pills-tab" class="bt registerGuest" data-object="0" data-status="6" data-instruction="178" data-time="100000" data-lessonid="10130" data-date="2023/9/16" data-durationinminutes="50" data-desc="אימון סיבולת לב ריאה ושריפת שומנים. רכיבה אינטנסיבית על אופני סטודיו, לקצב מוסיקה סוחפת ובליווי מדריך מקצועי
" data-location="ספינינג" data-teacher="מיטל יחזקאל" data-lessonname="ספינינג" data-toggle="modal" data-target="#guest-reg-form"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">to register</font></font></a>
</div>
</div><div class="time box-day">
<h5 class="bottom-details"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Pilates equipment</font></font></h5>
<span class="top-title-d"><i class="fas fa-chevron-left rotate"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10:00 | </font><font style="vertical-align: inherit;">50 minutes</font></font></span>
<div class="bottom-details"><p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Instructor: Diana Wegman</font></font></p>
<p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Pilates equipment</font></font></p><a href="#pills-tab" class="bt registerGuest" data-object="0" data-status="3" data-instruction="169" data-time="100000" data-lessonid="10365" data-date="2023/9/16" data-durationinminutes="50" data-desc=" " data-location="פילאטיס מכשירים" data-teacher="דיאנה ווגמן" data-lessonname="פילאטיס מכשירים" data-toggle="modal" data-target="#guest-reg-form"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">to register</font></font></a>
</div>
</div><div class="time box-day">
<h5 class="bottom-details"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Health exercise</font></font></h5>
<span class="top-title-d"><i class="fas fa-chevron-left rotate"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">10:30 | </font><font style="vertical-align: inherit;">50 minutes</font></font></span>
<div class="bottom-details"><p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Instructor: Maayan Segal</font></font></p>
<p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Studio 1</font></font></p><a href="#pills-tab" class="bt registerGuest" data-object="0" data-status="6" data-instruction="266" data-time="103000" data-lessonid="10113" data-date="2023/9/16" data-durationinminutes="50" data-desc="פילאטיס על מזרן עבודה על התפתחות אחידה של השרירים ושמירה על אורכם , תוך התמקדות במרכז הגוף בשרירי הבטן ונשימה ובהארכת והגמשת השרירים
" data-location="סטודיו 1" data-teacher="מעיין סגל" data-lessonname="התעמלות בריאותית" data-toggle="modal" data-target="#guest-reg-form"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">to register</font></font></a>
</div>
</div><div class="time box-day">
<h5 class="bottom-details"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Spinning</font></font></h5>
<span class="top-title-d"><i class="fas fa-chevron-left rotate"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11:00 | </font><font style="vertical-align: inherit;">60 min</font></font></span>
<div class="bottom-details"><p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Instructor: Mittal Yehezkel</font></font></p>
<p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Spinning</font></font></p><a href="#pills-tab" class="bt registerGuest" data-object="0" data-status="6" data-instruction="178" data-time="110000" data-lessonid="10126" data-date="2023/9/16" data-durationinminutes="60" data-desc="אימון סיבולת לב ריאה ושריפת שומנים. רכיבה אינטנסיבית על אופני סטודיו, לקצב מוסיקה סוחפת ובליווי מדריך מקצועי
" data-location="ספינינג" data-teacher="מיטל יחזקאל" data-lessonname="ספינינג" data-toggle="modal" data-target="#guest-reg-form"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">to register</font></font></a>
</div>
</div><div class="time box-day">
<h5 class="bottom-details"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Pilates equipment</font></font></h5>
<span class="top-title-d"><i class="fas fa-chevron-left rotate"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11:00 | </font><font style="vertical-align: inherit;">50 minutes</font></font></span>
<div class="bottom-details"><p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Instructor: Diana Wegman</font></font></p>
<p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Pilates equipment</font></font></p><a href="#pills-tab" class="bt registerGuest" data-object="0" data-status="3" data-instruction="169" data-time="110000" data-lessonid="10378" data-date="2023/9/16" data-durationinminutes="50" data-desc=" " data-location="פילאטיס מכשירים" data-teacher="דיאנה ווגמן" data-lessonname="פילאטיס מכשירים" data-toggle="modal" data-target="#guest-reg-form"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">to register</font></font></a>
</div>
</div><div class="time box-day">
<h5 class="bottom-details"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Pilates and stretching</font></font></h5>
<span class="top-title-d"><i class="fas fa-chevron-left rotate"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">11:30 | </font><font style="vertical-align: inherit;">60 min</font></font></span>
<div class="bottom-details"><p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Instructor: Maayan Segal</font></font></p>
<p><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Studio 1</font></font></p><a href="#pills-tab" class="bt registerGuest" data-object="0" data-status="6" data-instruction="266" data-time="113000" data-lessonid="10338" data-date="2023/9/16" data-durationinminutes="60" data-desc="שעור המעניק עצמה חוויתית גבוהה לשיפור הכח ,הגמישות והיציבה תוך זרימה תנועתית" data-location="סטודיו 1" data-teacher="מעיין סגל" data-lessonname="פילאטיס ומתיחות" data-toggle="modal" data-target="#guest-reg-form"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">to register</font></font></a>
</div>
</div></div>
"""

soup = BeautifulSoup(html, 'html.parser')

# Find all lesson blocks
lesson_blocks = soup.find_all("div", class_="time box-day")

lessons = []

for block in lesson_blocks:
    lesson = {}

    # Lesson Name.
    lesson_name_element = block.find('h5', class_='bottom-details')
    if lesson_name_element:
        lesson_type = lesson_name_element.get_text(strip=True)
        if lesson_type != 'Pilates equipment':
            # Lesson Type.
            lesson['type'] = lesson_type

            # Lesson Time.
            time_element = block.find('span', class_='top-title-d')
            if time_element:
                time_and_duration = time_element.get_text(strip=True).split('|')
                lesson['start_time'] = time_and_duration[0].strip() if len(time_and_duration) > 0 else None

            # Lesson Id and data time.
            lesson_details_element = block.find('a', class_="bt registerGuest")
            if lesson_details_element:
                lesson['lesson_id'] = lesson_details_element.attrs.get('data-lessonid')
                lesson['data_time'] = lesson_details_element.attrs.get('data-time')
            lessons.append(lesson)

for lesson in lessons:
    print(lesson)
