import re

CAL_START = "BEGIN:VCALENDAR" + \
            "\nPRODID:-//Google Inc//Google Calendar 70.9054//EN" +  \
            "\nVERSION:2.0" + \
            "\nCALSCALE:GREGORIAN" + \
            "\nMETHOD:PUBLISH" + \
            "\nX-WR-CALNAME:tester" + \
            "\nX-WR-TIMEZONE:America/Toronto" + \
            "\nX-WR-CALDESC: " + \
            "\nBEGIN:VTIMEZONE" + \
            "\nTZID:America/Toronto" + \
            "\nX-LIC-LOCATION:America/Toronto" + \
            "\nBEGIN:DAYLIGHT" + \
            "\nTZOFFSETFROM:-0500" +  \
            "\nTZOFFSETTO:-0400" + \
            "\nTZNAME:EDT" + \
            "\nDTSTART:19700308T020000" + \
            "\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU" + \
            "\nEND:DAYLIGHT" + \
            "\nBEGIN:STANDARD" + \
            "\nTZOFFSETFROM:-0400" + \
            "\nTZOFFSETTO:-0500" + \
            "\nTZNAME:EST" + \
            "\nDTSTART:19701101T020000" + \
            "\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU" + \
            "\nEND:STANDARD" + \
            "\nEND:VTIMEZONE\n"
        

CAL_END = "END:VCALENDAR\n"


def makeTags(tag):
    return ("<" + tag + ">", "</" + tag + ">")


#parse html
# extract content in multiple pairs of the given tag
def extract(s, tag):
    #print ("***********************************************************") 
    if s != None:
        tags = makeTags(tag)
        contents = []
        #print "tags", tags
        #print "unprocessed:", s 

        #start tags may contain tag with attributes set in it, 
        s0 = s.split(tags[0][:-1])        #split on "<tr" instead of "<tr>"
        # assumed that html is well formed
        del s0[0]
        #print "s0:", s0

        for thing in s0:
            #print "thing: ", thing
            if thing[0] == '>':           #start tag contains no attributes
                #print 'has no attributes in start tag'
                thang = thing[1:].split(tags[1])[0]
                contents.append(thang)
                #print 'thang', thang

            else:                         #start tag contains attributes
                #print "has attributes in start tag"
                thang = thing[thing.index(">")+1:].split(tags[1])[0]
                #print 'thang', thang
                contents.append(thang)
        #print("************************************************************")
        return contents

        #unprocessed = s.split(tags[0])
        #del unprocessed[0] 
        #content = []

        #print "unprocessed:", unprocessed
        
        #for thing in unprocessed:
            #print("thing: ", thing)
            #if tags[1] in thing:
                #print (thing.split(tags[1]))
                #content.append(thing.split(tags[1])[0])
        #print 'content', content
        #return innerContent
    return s 
#print("************************************************************")
#print('TESTING EXTRACT: ')
#print (extract("sdf<tr>this is </tr>sdfs s fsdf <tr>the content</tr>sdfsdf", "tr"))
#print (extract("dsfsdfsdf<b>sdf</b>jsdklfjdksfjd<table>table reached</table>sdfdsfdsf<hisdfkdfj<table>table 2 reached</table>sdfdsf<hi>Hdsfsdf</hi>", "table"))
#print (extract("not content<tr>hello this is the content</tr>not content", "tr"))
#print (extract("<td>1</td><td>2</td>  <td>3</td>", "td"))
# will fail on tag with attributes in them
#print(extract("<tr attr=12>content</tr>", "tr"))
#print(extract("<tr atrt=122 123123 12 31 23 1>one</tr><tr>two</tr>", "tr"))
#print("************************************************************")
#print('TESTING EXTRACT: ')

'''extract_str replaces this function ''' 
def extract_courseCode(href):
    if (href != None):
        return href.split("#")[1]
    return href

def extract_str(s):
    s0 = s.split(">")
    for thing in s0:
        if "</" in thing:
            if len(thing.split("</")[0]) > 0:
                return thing.split("</")[0]
    

''' Extracts content in a single html row(within <tr> </tr> tags).
'''
def getRawRow(fo):
    tag = "tr"
    tags = makeTags(tag)
    start = tags[0]
    end = tags[1]

    line = fo.readline()
    unproc = ""
    while (start not in line):
        if start in line:
            unproc = start + line.split(start)
        line = fo.readline()

    if end in unproc:
        return extract(unproc, tag)
    else:
        while (end not in line):
            unproc = unproc + line
            line = fo.readline()
        unproc = unproc + line.split(end)[0] + end

        return extract(unproc, tag)[0]

    return None

''' From a single row's html content, return an array of a course's information.
    The array is in the format: 
        course code, 
        course title, 
        course type(H or Y), 
        semester, 
        meeting section code, 
        time slots, 
        location 
'''

CODE = "code"
TITLE = "title"
TYPE = "type"
SEMESTER = "semester"
SECTION = "section"
TIMES = "times"
LOCATION = "location"
INSTRUCTOR = "instructor"



#@static_var("currentCourse", '')
#@static_var("section", '')
#@static_var("title", '')
def processRow(row):

    cells = extract(row, "td")
    data = {} 
    print "cell 0", cells[0]
    j = 0 
    for cell in cells: 
        print "cell #", j
        print (extract_str(cell))
        j = j + 1
    if len (cells) < 5:  
        return None
    print() 
    
    
    if ('nbsp' in (cells[0] + cells[1] + cells[2])) or cells[0] == '' or cells[0] == None:
        data[CODE] = processRow.currentCourse
        data[SECTION] = processRow.section
        data[TITLE] = processRow.title

    else:
        data[CODE] = extract_str(cells[0])
        data[SECTION] = extract_str(cells[1]) 
        data[TITLE] = extract_str(cells[2])
        processRow.currentCourse = data.get(CODE) 
        processRow.section = data.get(SECTION)
        processRow.title= data.get(TITLE) 
    print "cell[7]", cells[7]
    print "currentCourse: ", processRow.currentCourse
    print "section", processRow.section
    print "title", processRow.title


    print "--------------------"
    print "cell[7]", cells[7]
    data[TYPE] = data.get(TITLE)[-1]
    data[SEMESTER] = extract_str(cells[1])
    data[TIMES] = extract_str(cells[5])
    data[LOCATION] = extract_str(cells[6])
    data[INSTRUCTOR] = extract_str(cells[7])
 
    return data
processRow.currentCourse = ''
processRow.section = ''
processRow.title = ''



'''
    Parse processed row data to iCal event. 
'''
def rowToICalEvent(row):
    MONDAY = "MO"
    TUESDAY = "TU"
    WEDNESDAY = "WE"
    THURSDAY = "TH"
    FRIDAY = "FR"
    SATURDAY = "SA"
    SUNDAY = "SU"

    WEEKDAYS = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]
    RAW_TO_DAY = {'M': MONDAY,
                    'T': TUESDAY,
                'W': WEDNESDAY,
                'R': THURSDAY,
                'F': FRIDAY}

    
    
    
    timeSlots = row[TIMES]


    # NOTE: UTC time format: YYYYMMDD'T'HHMM00
    START_DATE1 = "2015010"      # all events start at this month and year,
                                 # must be exact
    END_DATE = "20150401T"       # all events end/stop repeating by this date 

     # get day number of start date
    BASE_START_DAY = 5
    
    print "------------------------------------!!!!!!!!"
    print "row:", row
    print "timeslots: ", timeSlots
    startDay = str(BASE_START_DAY + WEEKDAYS.index(RAW_TO_DAY[timeSlots[0]]))  + "T"
    startDate = START_DATE1 + startDay                         #iCal startDate
    
    timeIndex = re.search('\d', row[TIMES]).start()
    
    repDays = row[TIMES][:timeIndex]
    
    timings = row[TIMES][timeIndex:]
    
    t0 = timings.split("-")
    if len (t0) == 1: 

        if len (t0[0]) == 1:
            startTime = '0' + t0[0]
            numStartTime = ord(t0[0]) - 48
        else:
            startTime = t0[0]
            numStartTime = (ord(t0[0][0])-48)*10 + (ord(t0[0][1]) - 48)

        numEndTime = numStartTime + 1
        endTime = ''
        
        if numEndTime >=10:
            if numEndTime == 12:
                endTime = '01'
            endTime = str(numEndTime)
        else: 
            endTime = '0' + str(numEndTime)

    else:
        startTime = t0[0]
        print("t0", t0)
        endTime = t0[1]
    # create iCal str of days and timing this event reoccurs at
    iCal_repDays = RAW_TO_DAY[repDays[0]]
    for i in range(1, len(repDays), 1):
        iCal_repDays = iCal_repDays + ', ' +  RAW_TO_DAY[repDays[i]]
 

    print 'repDays:', repDays
    dateEnd = startDate + endTime + '0000'
    startDate = startDate + startTime + '0000'
    endDate = END_DATE + endTime+ '0000Z'
    # iCal event text description
    #courseInfo[]
    descr = row[CODE] + " - " + row[SECTION] + "\\n" \
            + row[TITLE]  + "\\n" + row[INSTRUCTOR] + "\\n\\n" \
            + row[TIMES] + "\\n" + row[LOCATION]

    # return final iCal scipt for event
    return  "\nBEGIN:VEVENT"\
            + "\nDTSTART;TZID=America/Toronto:" + startDate\
            + "\nDTEND;TZID=America/Toronto:" + dateEnd\
            + "\nRRULE:FREQ=WEEKLY;UNTIL=" + endDate + ";BYDAY=" + iCal_repDays\
            + "\nDESCRIPTION:" + descr \
            + "\nLOCATION:" + row[LOCATION]\
            + "\nSEQUENCE:1" \
            + "\nSTATUS:CONFIRMED" \
            + "\nSUMMARY:" + row[CODE]\
            + "\nTRANSP:OPAQUE" \
            + "\nEND:VEVENT\n"



''' do the magic.
'''

processedRows = []
fi = open("csc.html", "r+")
fo = open("output.ical", "wb")
fo.write(CAL_START)
row = getRawRow(fi)
#print("getting raw row", row)

print "-----------------------"
i = 0               # number of rows to read from input
while (i!= 241):
    # extract the raw html data in a single row
    row = getRawRow(fi) 
    currentCourse = ""
    section = ""
    title = ""
    processedRow = []

    if (i > 1): 
        print("===================================--------RAW")
        print 'ROW: ', i
        print "===========================================" 
        # extract data from htmli
        processedRow= processRow(row)
        print "currentCourse: ", currentCourse
        print processedRow[SEMESTER]
        #print (processedRow)
        if processedRow[SEMESTER] == "S" or processedRow[SEMESTER] == 'Y':
            processedRows.append(processedRow)   # remove later

            # parse data to ical
            iCalEvent = rowToICalEvent(processedRow)
            fo.write(iCalEvent)

    i = i + 1

fo.write(CAL_END)

fi.close()
fo.close()
