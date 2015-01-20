CAL_START = "N:STANDARD\nTZOFFSETFROM:-0400\nTZOFFSETTO:-0500\nTZNAME:EST\
        \nDTSTART:19701101T020000\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\
        \nEND:STANDARD\nEND:VTIMEZONE\n"

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

#def extract_val(s):
    #i = 0

    #while (i < len (s)):
        #if s[i] == '>':
            #start = i
            #end = s[i+1:].index('<') + i
            #if end - start > 1:
                #return s[start+1:end+1]
        #i = i + 1
    #return s


#''' Extract the human-readable text content within the given html tags '''

#def extract_str(s):
    #i = 0

    #while (i < len (s)):
        #if s[i] == '>':
            #start = i
            #s0 = s[i+1:]
            #return s0.split("<")[0]
        #i = i + 1
    #return s

##print(extract_str("<><><>hello<>"))






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

courseInfo = {CODE: 0,
        TITLE: 1,
        TYPE: 2,
        SEMESTER: 3,
        SECTION: 4,
        TIMES: 5,
        LOCATION: 6, 
        INSTRUCTOR: 7}
def processRow(row, currentCourse):

    cells = extract(row, "td")
    #print("-------------------")
    #print ("HERE ARE THE CELLS")
    data = {} 
    print "cell 0", cells[0]
    j = 0 
    for cell in cells: 
        print "cell #", j
        print (extract_str(cell))
        j = j + 1
    print ("no more cells")
    print() 
    print "currentCourse: ", currentCourse
    if currentCourse == '':
        data[courseInfo[CODE]] = extract_str(cells[0])
        print "course", extract_str(cells[0]) 
        currentCourse = extract_str(cells[0]) 

        print currentCourse
    else: 
        data[courseInfo[CODE]] = currentCourse

    print "currentCourse: ", currentCourse
    data[courseInfo[TITLE]] = extract_str(cells[2])
    data[courseInfo[TYPE]] = currentCourse[-1]
    data[courseInfo[SEMESTER]] = extract_str(cells[1])
    data[courseInfo[SECTION]] = extract_str(cells[3])
    data[courseInfo[TIMES]] = extract_str(cells[5])
    data[courseInfo[LOCATION]] = extract_str(cells[6])
    data[courseInfo[INSTRUCTOR]] = extract_str(cells[7])
 
    return data, currentCourse 
    #return  ([courseCode, \
            #cells[courseInfo['title']], \
            #courseType, \
            #[cells[courseInfo['semester']]], \
            #[cells[courseInfo['section']]], \
            #[cells[courseInfo['time']]], \
            #[cells[courseInfo['location']]], \
            #[cells[courseInfo['instructor']]]], currentCourse)


'''
    Parse row data to iCal event. 
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
    startDay = BASE_START_DAY + WEEKDAYS.index(RAW_TO_DAY[timeSlots[0]])  + "T"
    startDate = START_DATE1 + startDay                         #iCal startDate

    repDays = ""
    for char in timeSlots[:readUpTo]:
        if char == timeSlots[:-3]:
            repDays = repDays + rawToDay[char]
        else: 
            repDays = repDays + rawToDay[char] + ", "

    startDate = startDate + startTime
    endDate = endDate + endTime

    # create iCal str of days and timing this event reoccurs at
    if timing[-2].isAlpha():
        startTime = chr(baseStart + timeSlot[-2]) + "00"
        endTime = chr(timeSlots[-1]) + "00" 
        readUpTo = -2

    else:
        startTime = chr(baseStart + timeSlots[-1]) + "00"
        # to convert char to int, subtract 48
        # end time is one hr later, add 1
        endTime = chr(ord(timeSlots[-1]) - 47) + "00"
        readUpTo = -1

    # iCal event text description
    #courseInfo[]
    descr = row[CODE] + " - " + row[SECTION] + "\n" \
            + row[TITLE]  + "\n" + row[INSTRUCTOR] + "\n\n" \
            + row[TIMES] + "\n" + row[LOCATION]

    # return final iCal scipt for event
    return  "\nBEGIN:VEVENT"\
            + "\nDTSTART;TZID=America/Toronto:" + startDate\
            + "\nDTEND;TZID=America/Toronto:" + endDate\
            + "\nRRULE:FREQ=WEEKLY;UNTIL=" + dateEnd + "T130000Z;BYDAY=" + repDays\
            + "\nDESCRIPTION:" + descr \
            + "\nSEQUENCE:1" \
            + "\nSUMMARY:" + courseTitle\
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
while (i!= 7):
    # extract the raw html data in a single row
    row = getRawRow(fi) 
    currentCourse = ""
    processedRow = []

    if (i > 1): 
        print 'current course', currentCourse
        print("--------RAW")
        print 'ROW'
        print row
        
        # extract data from html
        processedRow, currentCourse = processRow(row, currentCourse)
        
        #print ("---PROCESSED")
        #print (processedRow)
        processedRows.append(processedRow)   # remove later

        # parse data to ical
        iCalEvent = rowToICalEvent(processedRow)
        #print ("--- PARSED ICAL")
        #print(iCalEvent)
        #print("-----------")
        fo.write(iCalEvent)

    i = i + 1

fo.write(CAL_END)

fi.close()
fo.close()
