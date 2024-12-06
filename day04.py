# library: numpy gives us nice 2d arrays
import numpy as np

file = open("day4-input.txt","r")
lines = file.readlines()
# luckily, we have a well formed input: every line is the same number of characters. this all breaks if it doesn't, tbh.

total_rows = len(lines)
total_cols = len(lines[0]) - 1 # that is to say, without the newline/carriage return

wordsearch_onedim = np.array(lines, dtype=str("U"+str(total_cols + 1))) # this creates a long 1D array; each entry is a row with a newline char at the end
wordsearch_array = np.empty((total_rows,total_cols), dtype='U1')

for row in range(total_rows) :
    current_string = wordsearch_onedim[row].rstrip() # bye newlines!
    for col in range(total_cols) :
        wordsearch_array[row, col] = current_string[col]

file.close()

# okay so now that we have this 2D array, now what?
found_total_part1 = 0
searching_for_part1 = ['X','M','A','S']

def look_p1 (array_searched) -> int:
# Within a given 1 dimensional array, look forwards and backwards
# and output the total found that time
    found_this_search = 0    
    current_string = np.char.join(sep="",seq=array_searched)
    for word_start in range(len(array_searched) - 3):
        current_attempt = current_string[word_start:word_start+4] # so here's 4 characters
        comparison_f = np.char.compare_chararrays(current_attempt, searching_for_part1, "==", True) # look at them forwards
        comparison_b = np.char.compare_chararrays(np.flip(current_attempt,0), searching_for_part1, "==", True) # flip the 4 and look backwards
        if sum(comparison_f) == 4 or sum(comparison_b) == 4: #i. e. all characters match
            found_this_search = found_this_search + 1
    return found_this_search

for row in range(total_rows): 
    found_total_part1 = found_total_part1 + look_p1(wordsearch_array[row])
#print("Total after rows:" + str(found_total))
# searching vertically: transpose the whole array (so now the rows are columns and vice versa)
for row_t in range(total_cols):
    found_total_part1 = found_total_part1 + look_p1(wordsearch_array.T[row_t])
#print("total after cols:" + str(found_total))

# now time to find diagonals
def look_diags (array_searched) -> int:
    # looks in the upper right of an array, then we'll do a bunch of spinning the array around
    found_this_search = 0
    for offset in range(len(array_searched) - 2): # the itty bitty corners are too small for our phrase
        upper_diag = np.diagonal(array_searched, offset)
        #print(upper_diag)
        found_this_search = found_this_search + look_p1(upper_diag)
        #print(found_this_search)
    return found_this_search

# I'm not sure how to notate in text that these work, but they do...
found_total_part1 = found_total_part1 + look_diags(wordsearch_array)
found_total_part1 = found_total_part1 + look_diags(np.fliplr(wordsearch_array))
found_total_part1 = found_total_part1 + look_diags(wordsearch_array.T)
found_total_part1 = found_total_part1 + look_diags(np.fliplr(wordsearch_array).T)

# but these will have counted the two major diagonals twice
found_total_part1 = found_total_part1 - look_p1(np.diag(wordsearch_array)) - look_p1(np.diag(np.fliplr(wordsearch_array)))

print("Part 1 total is: "+ str(found_total_part1))

######## part 2

found_total_part2 = 0
searching_for_part2 = [['M', 'k', 'M'],['k','A','k'],['S','k','S']]
# this is a 3 x 3 array, it looks like this.
# [M, k, M]
# [k, A, k]
# [S, k, S]
# The other versions of this exist by flipping it around a bunch of ways, but fundamentally this is what it is
# 'k' is there as a single-char dummy, it's *always* false in our comparison

for row in range(1, total_rows - 1):
    for col in range(1, total_cols - 1):
        current_subarray = wordsearch_array[row-1:row+2,col-1:col+2]
        # now some checks if this 3x3 is a part2 match
        if current_subarray[1,1] != 'A' or current_subarray[0,0] == current_subarray[2,2]: # center mismatch, or corners that definitely don't have M/S pairs
            continue
        elif current_subarray[0,0] == 'M':
            # two options for the other M: (0,2) ("across") or (2,0) ("down")
            # and yep you guessed it, one swaps to the other with a transpose, truly NumPy is saving my ass today
            comparison_across = np.char.compare_chararrays(current_subarray,searching_for_part2,'==',True)
            comparison_down = np.char.compare_chararrays(current_subarray.T,searching_for_part2,'==',True)
            if np.sum(comparison_across) == 5 or np.sum(comparison_down) == 5:
                found_total_part2 = found_total_part2 + 1
                #print(current_subarray)
        elif current_subarray[0,0] == 'S':
            # new options!
            # [S, k, S]    [S, k, M]
            # [k, A, k] or [k, A, k]
            # [M, k, M]    [S, k, M]
            # these are basically the ones above, but flipped around
            comparison_across = np.char.compare_chararrays(np.flipud(current_subarray), searching_for_part2, '==', True)
            comparison_down = np.char.compare_chararrays(np.flipud(current_subarray.T), searching_for_part2,'==',True)
            if np.sum(comparison_across) == 5 or np.sum(comparison_down) == 5:
                found_total_part2 = found_total_part2 + 1
                #print(current_subarray)
        # no else statement! literally anything else is a failed case and so gets skipped

print("Part 2 total is: "+str(found_total_part2))
