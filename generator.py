import random

""" EXPLANATION: 

We first get the answer by random, we decided what each digit gets what status(key or certain)
This status is what the number gets when we have all 3 verified. they all become keys after verified_sorting.

Then we assign those verified into lines with an addition to fake possibles, fake possibles are numbers that 
makes it through the filter line, but gets eliminated in the combination testing phase. 

Again, How you make a number to be a key? You do that by eliminating other numbers on the same line (incorrect = incorrect_counter). 
That's how you get your keys. Your position can be gotten by "misplaced" or "placed" hints. But now the question is how do
you eliminate others? (other than the hint "3 correct numbers and misplaced")
Ways to eliminate:
1-contradiction,
* all slots = 0  aka [0, 0, 0], if all slots are 0, then it cannot be a key
* already declared slot as true is now false, or vise versa. So a spot is both false and true...obviously contradiction. 
2-deletion, "everything is wrong"
3-disqualification, comes later keys = keys_counter
4-spot filtration, comes later, this is the fake possible:

The next step is to fill up with the empty slots with dead numbers (and verifieds maybe). Dead numbers are 
dead before the filter line/loop. We use the above methods to fill up empty slots

Lastly, the last thing you do is get the right format of information. You find the right hints based on the lines.
It counts how many verified in each line and whether it's misplaced or well placed and chooses the right hint for each
line. 

Now we have everything, send the information back. 
"""


def generate():
    print("((( *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* GENERATOR *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* )))")

    linesinfo = []  # this will hold the lines and the numbers inside them, and also whether they are placed/misplaced

    dead_numbers = []  # numbers that are false will be added here so we can use them for something later

    # lets get our final answer
    answer = [-1, -1, -1]  # just to initialize. -1 means empty
    while (answer[0] == answer[1]) or (answer[0] == answer[2]) or (
            answer[1] == answer[2]):  # if any 2 digits are the same
        answer = [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)]
    print("answer: " + str(answer))

    # this is what number get what status.
    status = ["key", "key"]  # at least 2 numbers will be key, the third can be either key or certain
    status.insert(random.randint(0, 2), random.choice(["certain", "key", "certain"]))
    print("status: " + str(status))
    # reminder: key, you already know its one of the keys, and you know it's location as well
    # certain, you don't know its exact location, but you can deduce it when comparing it to other keys

    # ------------------------------- assign verified numbers (+ fake possibles)----------------------------------#

    for digit in range(3):  # digit as in left digit(0), middle digit(1), and right digit(2)

        linesinfo = shuffle_lines(linesinfo)  # lets shuffle it

        if status[digit] == "certain" or random.choice([True, True, True, False]):  #---------------if misplaced

            # lets choose a spot(left, middle, right) to put the digit in
            spot = random.randint(0, 2)
            while spot == digit:  # if spot is in number's place
                spot = random.randint(0, 2)  # get another spot.

            # check if we may add it to an already existing line. see if there an available spot.
            # If yes, add it
            # If no, then we create another line
            # Best case scenario, each key gets 2 lines, certain gets 1. You get 5 lines max this section.
            done = False
            for i in range(len(linesinfo)):
                if (linesinfo[i][spot] == -1) and (linesinfo[i][3] == "misplaced")\
                and (linesinfo[i][0] != answer[digit] and linesinfo[i][1] != answer[digit] and linesinfo[i][2] != answer[digit])\
                and (len(linesinfo) >= 3) and random.choice([True, False, False, False, False]):  # (len(linesinfo) >= 3 to make sure you never end up with 2 lines overall
                    linesinfo[i][spot] = answer[digit]
                    done = True
                    break
            # if you didn't find available spot. aka done is still == False, then add a new line
            if not done:
                linesinfo.append([-1, -1, -1, "misplaced"])  # add a line at the end of the 2D array
                linesinfo[len(linesinfo) - 1][spot] = answer[digit]  # go to that last line and put the number in the line somewhere that isn't in its correct place.

            # Now you must add the number into a different line since it's misplaced and you need more than one line to
            # clarify its location. Only if it's a key of course. Cuz you don't need to specify the location of a certain
            if status[digit] == "key":
                second_spot = random.randint(0, 2)
                while (second_spot == digit) or (second_spot == spot):  # needs to be in a different spot
                    second_spot = random.randint(0, 2)  # get another spot.
                # check if we may add it to an already existing line. see if there an available spot, if not, then we just create another line
                done = False
                for i in range(len(linesinfo)):
                    if (linesinfo[i][second_spot] == -1) and (linesinfo[i][3] == "misplaced")\
                    and (linesinfo[i][0] != answer[digit] and linesinfo[i][1] != answer[digit] and linesinfo[i][2] != answer[digit])\
                    and random.choice([False, False, False, True, False]):
                        linesinfo[i][second_spot] = answer[digit]
                        done = True
                        break
                # if you didn't find available spot. aka done still == False, then add a new line
                if not done:
                    linesinfo.append([-1, -1, -1, "misplaced"])  # add a line at the end of the 2D array
                    linesinfo[len(linesinfo) - 1][second_spot] = answer[digit]

            # If it's a certain, then lets put a fake possible next to it. Fake possible is a number that doesn't contradict
            # itself, it dies in possible combination phase due to being unable to do verified_sorting with other keys
            elif status[digit] == "certain" and not done and random.choice([True, False]):  # the not done is important, it needs to be in the same line we added
                wrong_number = random.randint(0, 9)
                while (wrong_number == answer[0]) or (wrong_number == answer[1]) or (wrong_number == answer[2]):
                    wrong_number = random.randint(0, 9)  # get another spot.
                # dead_numbers.append(wrong_number)  # lets not add it in, complicated reasons.
                print("fake possible: " + str(wrong_number))

                if linesinfo[len(linesinfo) - 1][digit] == -1:  # make sure it's an empty slot
                    linesinfo[len(linesinfo) - 1][digit] = wrong_number


        else:  #-------------------------if well placed

            spot = digit

            # check if we may add it to an already existing line. see if there an available spot, if not, then we just create another line
            done = False
            for i in range(len(linesinfo)):
                if (linesinfo[i][spot] == -1) and (linesinfo[i][3] == "wellplaced") and random.choice([True, False, False, False, False])\
                and (len(linesinfo) >= 3):  # to make sure you never end up with 2 lines overall
                    linesinfo[i][spot] = answer[digit]
                    done = True
                    break
            # if you didn't find available spot. aka done still == False, then add a new line
            if not done:
                linesinfo.append([-1, -1, -1, "wellplaced"])  # add a line at the end of the 2D array
                linesinfo[len(linesinfo) - 1][spot] = answer[digit]  # go to that last line you just added and put the number


    print(linesinfo)
    # ------------------------------- assign false numbers ----------------------------------#

    # Let's fill up the empty slots(-1s) by dead numbers or even use a digit as long as it don't contradicts and kill itself or fellow digits.

    # check if we can do the contradiction by all slots of a number to be = 0
    good_lines = [-1, -1, -1]  # these three lines would have available spots
    for slot in range(3):
        for i in range(len(linesinfo)):
            if (linesinfo[i][slot] == -1) and (linesinfo[i][3] == "misplaced") \
                    and (i != good_lines[0] and i != good_lines[1] and i != good_lines[2]):
                good_lines[slot] = i
    # if we found the 3 good lines, then yes, go for it.
    if (good_lines[0] != -1) and (good_lines[1] != -1) and (good_lines[2] != -1):
        # oke lets assign it
        # first find a wrong number that isn't any of the verified
        wrong_number = random.randint(0, 9)
        while (wrong_number == answer[0]) or (wrong_number == answer[1]) or (wrong_number == answer[2])\
        or (wrong_number in dead_numbers):
            wrong_number = random.randint(0, 9)  # get another spot.
        dead_numbers.append(wrong_number)
        print("\nLet's do contradiction by all slots = 0, for the number " + str(wrong_number))
        # put it in the lines
        linesinfo[good_lines[0]][0] = wrong_number
        linesinfo[good_lines[1]][1] = wrong_number
        linesinfo[good_lines[2]][2] = wrong_number

        print(linesinfo)

    # contradiction by already declared slot as true is now false, or vise versa
    # check if its doable
    good_lines = [-1, -1]  # [misplaced, wellplaced]
    good_slot = -1  # this is the slot we put the wrong number in
    for slot in range(3):
        for i in range(len(linesinfo)):
            if (linesinfo[i][slot] == -1) and (linesinfo[i][3] == "misplaced"):
                good_lines[0] = i
            if (linesinfo[i][slot] == -1) and (linesinfo[i][3] == "wellplaced"):
                good_lines[1] = i
        if good_lines[0] == -1 or good_lines[1] == -1:
            good_lines = [-1, -1]  # if one of them didn't find a line, then go back, we will check the next slot
        else:
            good_slot = slot; break  # else, break because we already found the lines. Don't check the next slot.
    # if we found our good lines, lets go a ahead and do it.
    if good_lines != [-1, -1]:
        # first find a wrong number that isn't any of the verified
        wrong_number = random.randint(0, 9)
        while (wrong_number == answer[0]) or (wrong_number == answer[1]) or (wrong_number == answer[2]):
            wrong_number = random.randint(0, 9)  # get another spot.
        dead_numbers.append(wrong_number)
        print("\nLet's do contradiction by already declared slot as true is now false, or vise versa, for the number " + str(wrong_number))
        linesinfo[good_lines[0]][good_slot] = wrong_number
        linesinfo[good_lines[1]][good_slot] = wrong_number

        print(linesinfo)

    # ------- contradictions done -------------------------- #

    print("\nLet's shuffle here...")
    linesinfo = shuffle_lines(linesinfo)
    print(linesinfo)

    # lets check if all lines and slots filled
    done = True
    for i in linesinfo:
        if i[0] == -1 or i[1] == -1 or i[2] == -1:
            done = False
            break

    # do disqualification
    if not done:
        print("\nLets do disqualification")
        for i in dead_numbers:
            for ii in linesinfo:
                if ii[0] != i and ii[1] != i and ii[2] != i and random.choice([True, False, False, False]):
                    if ii[0] == -1: ii[0] = i; break
                    if ii[1] == -1: ii[1] = i; break
                    if ii[2] == -1: ii[2] = i; break
        print(linesinfo)

    # lets cover some of the empty slots with verified numbers that don't contradicts or cause issues.
    # lets check if all lines and slots filled
    done = True
    for i in linesinfo:
        if i[0] == -1 or i[1] == -1 or i[2] == -1:
            done = False
            break
    # if not done, then lets do it (may or may not happen)
    if not done:
        print("\nLet's cover up empty slots with verified numbers")
        for i in linesinfo:
            for h in range(3):
                if i[h] == -1:
                    for p in answer:
                        if i[0] == p or i[1] == p or i[2] == p: continue
                        if i[3] == "misplaced" and answer.index(p) != h and status[answer.index(p)] != "certain" and random.choice([True, False, False]):
                            i[h] = p
                        if i[3] == "wellplaced" and answer.index(p) == h and random.choice([True, False, False]):
                            i[h] = p
                            if [i[0], i[1], i[2]] == answer:  # if the line became identical to the answer, it will lead to 'everything is correct' hint
                                i[h] = -1  # put the -1 back because we don't want 'everything is correct' hint
        print(linesinfo)


    # lastly lets do "everything wrong" line that takes care of remaining open spots.
    # lets check if all lines and slots filled
    done = True
    for i in linesinfo:
        if i[0] == -1 or i[1] == -1 or i[2] == -1:
            done = False
            break
    # if not done, then lets do it
    if not done:
        used_numbers = answer + dead_numbers
        line = [-1, -1, -1, "misplaced"]
        # find the 3 wrong numbers and add them to the 'everything is wrong' line
        for i in range(3):
            num = random.randint(0, 9)
            while (num in line) or (num in used_numbers):
                num = random.randint(0, 9)
            line[i] = num
        print("\nLet's do 'everything is wrong', line is " + str(line))
        for i in linesinfo:
            for ii in range(3):
                wrong_number = random.choice([line[0], line[1], line[2]])  # we don't just type 'line' cuz it may take the "misplaced" element
                while wrong_number in i:  # if spot is left (number's place)
                    wrong_number = random.choice([line[0], line[1], line[2]])  # get another spot.
                if i[ii] == -1:
                    i[ii] = wrong_number
        linesinfo.append(line)

        print(linesinfo)

    # lets put all in the proper format and send it----------------------------
    linesinfo = shuffle_lines(linesinfo)

    hintboxes = []

    for i in linesinfo:

        corrects = 0  # amount of correct numbers in the line
        if i[0] in answer: corrects += 1
        if i[1] in answer: corrects += 1
        if i[2] in answer: corrects += 1

        if corrects == 0:
            hintboxes.append(0)
        if corrects == 1 and i[3] == "misplaced":
            hintboxes.append(1)
        if corrects == 1 and i[3] == "wellplaced":
            hintboxes.append(2)
        if corrects == 2 and i[3] == "misplaced":
            hintboxes.append(3)
        if corrects == 2 and i[3] == "wellplaced":
            hintboxes.append(4)
        if corrects == 3 and i[3] == "misplaced":
            hintboxes.append(5)

        i.pop()  # pop the builtin hints

    print("ONE LAST TIME___________")
    print("linesinfo: " + str(linesinfo))
    print("hintboxes: " + str(hintboxes))

    return [linesinfo, hintboxes, len(linesinfo), answer]  # we don't need to send the answer

# this line shuffles the order of the lines randomly
def shuffle_lines(linesinfo):
    new_lines = []

    for i in range(len(linesinfo)):
        num = random.randint(0, len(linesinfo) - 1)

        new_lines.append(linesinfo[num])

        linesinfo.pop(num)

    return new_lines


# add last segment, line pandering where it add useless lines just to increase lines [skipped]
