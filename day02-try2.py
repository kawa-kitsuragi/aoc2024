
# libraries
# import pandas as pd
import regex as re
import numpy as np

safe_reports = []

def subreport(report: list, remove_this: int) -> list:
    # removes one item at index remove_this from a report
    new_report = report.copy()
    new_report.pop(remove_this)
    return new_report

def safety(report: list, tolerance_used: bool) -> bool:
    # report is a list of unknown length
    # tolerance_used is a bool that starts off false
    # in the overall function, tolerance_used can be flipped once, but not again
    # set initial polarity
    
    diff = report[1] - report[0]
    polarity = 0
    if abs(diff) > 3 or diff == 0: #outside of bounds, or repeated digit
        # part 2: we should check if it would change if we remove report[0] or report[1]
        if tolerance_used:
            return False # if we've been here before, get out of the safety function
        else: 
            tolerance_used = True
            subreport0 = subreport(report,0)
            subreport1 = subreport(report,1)
            # look at the subreport. if the subreport worked, then continue, but 'know' that we used the tolerance
            if safety(subreport0, True) or safety(subreport1, True):
                return True
            else: 
                return False # but if it's still false, we can just get out of here
    elif diff > 0: # increasing, within bounds
        polarity = 1
    # decreasing, within bounds 
    else: 
        polarity = -1

    for i in range(1, len(report)-1):
        diff = report[i+1] - report[i] # so this starts at checking (x[2] - x[1]) and will end at (x[len-1] - x[len-2])
        if abs(diff) > 3 or diff == 0 or diff * polarity < 0: 
            # if we're here again and tolerance_used has already been flipped, get out
            if tolerance_used:
                return False
            else:
                # we're here the first time, set tolerance_used to true
                tolerance_used = True    
                subreport_minus = subreport(report,i-1)
                subreport_i = subreport(report,i)
                subreport_plus = subreport(report,i+1)
                if safety(subreport_minus, True) or safety(subreport_i, True) or safety(subreport_plus, True):
                    return True
                else:
                    return False
    
    # if we never returned false after all that, we should be good
    return True

file = open('day2-input.txt', 'r')
for line in file: 
    report = line.split()
    report_ints = [int(number) for number in report]
    # do the function on the reported line
    if safety(report_ints, False):
        safe_reports.append(line)
        print('Right: ' + str(report_ints))
    else:
        print('Wrong: ' + str(report_ints))
    # if the function returns false, don't add it to safe_reports
    # if the function returns true, add it to safe_reports
file.close()
print(len(safe_reports))