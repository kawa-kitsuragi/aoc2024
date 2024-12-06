def find_next_mul(line_to_check: str) -> tuple[int, int]:
    # Given a string, find the next valid mul
    # if it's a valid mul, output[0] is the final multiplied value
    # if it's not, output[0]==0 (adding 0 to the total doesn't harm anything)
    # output[1] is an index of where to look next (or -1 if we really should just stop looking)
    possible_mul_start = line_to_check.find("mul(")
        # possible_mul_start is the index of the first mul (specifically of the m)
    if possible_mul_start == -1:
        # there's no mul here at all, just move on
        return (0,-1)
    else:
        possible_mul_end = line_to_check.find(")", possible_mul_start) # the index of the first close paren after
        if possible_mul_end == -1: 
            # so we have something like mul(aksjdsajlkfjadslkf with no close paren in the whole line
            # no substrings are possible here really
            return (0,-1)
        else:
            # so we have a string, from start to end+1, that looks like mul(contents)
            # we now have to check if the contents are well formed
            contents = line_to_check[possible_mul_start+4:possible_mul_end]
            contents_split = contents.split(",")
            if len(contents_split) != 2:
                # we could have something like mul(stuff,mul(3,5))
                # so the right return is 0 (we haven't checked the inner mul), but we should advance the check (but not too much)
                return (0,possible_mul_start+4)
            else:
                # contents_split is a list
                # things to check: non-ints, ints too big
                try: 
                    contents_ints = [int(number) for number in contents_split]
                except:
                    # again, we could have something weird in the contents
                    return (0, possible_mul_start+4)
                else:
                    # hey we successfully found two ints!!
                    # if the ints are the right size, yes, please give the contents
                    # otherwise, check after this otherwise well formed mul
                    if contents_ints[0] <= 999 and contents_ints[1] <= 999:
                        return (contents_ints[0] * contents_ints[1], possible_mul_end+1)
                    else: return (0, possible_mul_end+1)

def find_next_do(line_to_check: str) -> int:
    # found a don't(), find the next do()
    # might be -1 if there aren't any
    return line_to_check.find("do()")

def find_next_dont(line_to_check: str) -> int:
    return line_to_check.find("don't()")


file = open("day3-input.txt", "r")
instructions = file.read()
total = 0
position = 0
while position < len(instructions):
    #print("now looking at: "+ str(instructions[position:]))
    next_mul = find_next_mul(instructions[position:])
    next_dont = find_next_dont(instructions[position:])
    if next_mul[1] == -1: # there just aren't more muls no matter what
        break
    elif next_dont < next_mul[1] and next_dont != -1: # the next well formed don't happened before the start of next mul
        next_do = find_next_do(instructions[position:])
        if next_do == -1: # don't, then no do appears
            break 
        #print("Skipping until: "+ str(next_do))
        position=position + next_do
    else:
        # we found a mul, and we're safe from don't
        total = total + next_mul[0]
        #print("just multiplied: "+ str(next_mul[0])+" so current total is "+str(total))
        position = position + next_mul[1]
file.close()

print(total)