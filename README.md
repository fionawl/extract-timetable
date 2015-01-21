# extract-timetable
some extremely messy ad hoc messy code to parse html from UofT's CSC course sponsor timetable page into an iCal formatted calendar
http://www.artsandscience.utoronto.ca/ofr/timetable/winter/csc.html

because maybe there's already an excel sheet of this data i have access to or possibly even exists so i can extract from instead of html anyways..


#Bugs
- PM timings not accurately parsed in iCal format
- cannot skip over rows with cancelled classes correctly
- ad hoc solution: remove liens with cancelled classes from csc.html
- cannot read time slots for courses completely accurately:
-   ex) format T1, WF2 cannot be translated correctly as Thursday 1pm, Wednesday 2pm, Friday 2pm, instead it will only read T1.
-   solution: refactor
-   create function that splits on, then call another fn translates chars to time slots correctly
-   "><>F<><" original function for extract_str cannot read 1 char, current function splits and accidentally cuts out all text content in between "><"
