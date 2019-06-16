"""Brief Explanation:
This program solves the puzzle provided by the main program. The 'solve' function will be called by the main program,
and it will hand it the following parameters:
1- amount_of_lines: an integer representing the number of lines.
2- info_stored_in_lines: 2D array, length of 10. Each sun-array is like a line, carries 3 integers, representing the
3 numbers it holds.
3- hint_boxes: array of 10 integers. Holding which hint each hint box has.

The first step is to set up the data object which is an object that helps us carry information between functions
freely.

Next up, we go into 1st step which is a grand loop. This loop is we go through each line from top to bottom to examine
information and try to implement process of elimination to boil down to our answer. So we take the line we're working
with and we 1st apply the function loop_phase1_check_and_distribute to it which basically takes information and distributes
it to the numbers. phase1 only needs to be done once, so once we do it, we don't repeat it again. Only phase2 gets
repeated as long as the line isn't retired. The line retires when it finishes all its duties in phase2. But some lines
may not even get to retire by the time the loop ends. Speaking of phase2, short for the function loop_phase2_disqualify_and_retire,
this function counts how many correct/incorrect numbers in the line and checks if either of them is reached. If one of them
is, then it updates the status of the line's number objects appropriately, and we declare the line as retired so it
doesn't have to do anything ever again. However, if none is reached, then it moves on, and it checks the next time
when the loop recycles. Note that if any number gets the "dead" status at any point in the loop, then we recycle the
loop where non retired lines only gotta do phase2. When it recycle, it basically goes back to the 1st line and goes
down. Eventually, it will pass the final line and exists the loop. And perhaps not all lines are retired by then, some
may have not retired.

Now that we are done with the loop, next is the filter line. Basically, we gather the numbers that are not dead and
not initial(initials aren't even presented in the data so they defiantly not keys) and we put them in an array.
Then we split them into two arrays; verified and non verified. We take the verified and we check if they are the
keys by sorting them and do a checking process. If there are logic error, then we return that. If everything is good,
then we have our answer. If we still don't have all information, then we move on to the next step, combination testing
phase.

In combination testing phase, we take the nonverified objects and we make all kinds of possible combinations with it.
Because the answer can be one of those combinations. So we take one combination at a time and test to see if it conflicts,
and if it does, then we scratch this combination and move on to test the next. The test is basically let them do
verified_sorting function, and it shouldn't return "process failed", then they have to do check_line_retirement to make
sure they satisfy all the hints in terms of how many numbers are correct in each line. If the combination passes both
tests, then we add it to another array successful_combinations. This phase is over once we finished testing all
combinations.

Finally, we have successful_combinations (a 2D array). There needs to be only one sub-array. If it's more than one,
then we have more than one possible solutions. If it's zero, then there are no solutions. So we need it to be one.
We take this one, give a last look, organize it and return the result to the main program in a form of an array.

Note the following:
* I use the names list and array interchangeably here.
* I am making drastic changes from the original script.
* This program is not designed to be extendable to more slots. I was aiming to make it compatible with whatever amount
of slots/columns, but I stopped midway through and decided to only make it restricted to 3 slots. Heck, I'd have to
worry about the hints boxes. How would they work if we add more slots, how many hints we get? So no, forget about
the whole thing. 3 slots it is.
* The program could have been cut shorter at some parts, but I kept it layed out to perhaps makes it easier to understand.
* When I came back to add the part where it counts possible solutions in the case of info error, I made changes and
found flaws. So I made changes, but I was sleepy at the time, so I might have screwed something up. I don't know. But
you can fix whatever bug you find in the future.
"""

def solve(amount_of_lines, info_stored_in_lines, hint_boxes):

    print("\n\n((( *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* SOLVER *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* )))")
    # ---------------------SET UP DATA OBJECT--------------------- #
    # a class that we will use to create data object
    # we will store all data in this object so we can access and modify it from any function
    class Structure(object):
        pass
    # create the data object
    data = Structure()

    # give it information
    data.lines = amount_of_lines  # a number between 1-10
    data.linesinfo = info_stored_in_lines  # 2D array
    data.hintboxes = hint_boxes  # each element will range from 0 to 6

    # lets give it what lines have retired; gave out their information and fulfilled their count for keys.
    # if a line completed phase1 and phase2 successfully, it will retire.
    data.retired = [False, False, False, False, False, False, False, False, False, False]  # 10 elements for 10 lines

    # lets give it what lines has already distributed it information. If a line complete phase1, its corresponding
    # element will become True
    data.phase1_done = [False, False, False, False, False, False, False, False, False, False]  # 10 elements for 10 lines

    # this is how many correct numbers in each line. These values will be extracted from the hints
    data.line_correct_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 10 elements for 10 lines

    # this is used for the grand loop
    data.recycle = False  # when number dies, it will be triggered to True. We put this var here so that it reset itself..
    # ..every iteration. Otherwise if it ever set to yes, then it will keep recycling.

    # lets do the numbers
    class numbeer:  # you cant call the class 'number' because that will cause bugs and problems. IDK why. This is fine.
        def __init__(self, value):
            # more info to be added
            self.num = value  # just in case we needed this
            self.slots = [-1, -1, -1]  # -1 = unidentified, 0 = no, 1 = yes
            self.status = "initial"  # this can be "initial", "possible", "certain", "key", "dead"
            # initial: the status each object start as
            # possible: when the object is involved but we don't know much about it
            # certain: if the object is definitely one of the keys, but we don't know its location
            # key: a confirmed to be one of the digits. We know its location also.
            # dead: the object has been entirely disqualified and cannot be a key whatsoever.
    data.numbers = [numbeer(0), numbeer(1), numbeer(2), numbeer(3), numbeer(4), numbeer(5), numbeer(6), numbeer(7), numbeer(8),
                    numbeer(9)]

    print("-------------------LOOP BEGINS-------------------")
    turn = 0
    while turn < data.lines:  # 'turn' is which line currently working on. (line = turn + 1)
        print("turn: " + str(turn))

        if not (data.retired[turn]):
            if not(data.phase1_done[turn]):
                # phase 1 only need to be executed once for each line and before phase 2
                print("\nPhase 1 for the turn " + str(turn) + " begins")
                data = loop_phase1_check_and_distribute(data, turn)
                if data == "process failed":
                    print("phase1 Failed")
                    return ["?", "?", "?", "Error: Information provided is conflicted.\n         Hence, there is no solution!"]
                data.phase1_done[turn] = True
            print("Phase 2 for the turn " + str(turn) + " begins")
            data = loop_phase2_disqualify_and_retire(data, turn)
            if data == "process failed":
                print("phase2 Failed")
                return ["?", "?", "?", "Error: Information provided is conflicted.\n         Hence, there is no solution!"]

        if data.recycle:
            print("We will recycle!")
            turn = 0
            data.recycle = False  # reset this variable.
        else:
            turn += 1
    print("---------------------LOOP DONE---------------------")
    print("\ndata.numbers: ")
    for i in range(10):
        print("[" + str(i) + "]: " + str(data.numbers[i].slots) + ", " + data.numbers[i].status)
    print("retired: " + str(data.retired))
    print("Phase 1 done:" + str(data.phase1_done))
    print("line correct numbers: " + str(data.line_correct_numbers))
    print()
    print("---------------------FILTER LINE---------------------")

    # Now we have finished the loop. Let's take all the numbers who's not disqualified and put them in an array.
    remaining_numbers = []  # made out of number objects.
    for i in range(10):
        if (data.numbers[i].status != "dead") and (data.numbers[i].status != "initial"):
            remaining_numbers.append(data.numbers[i])

    print("remaining numbers: ")
    for i in range(len(remaining_numbers)):
        print("Number : " + str(remaining_numbers[i].num) + ", slots :" + str(remaining_numbers[i].slots)
              + ", status: " + str(remaining_numbers[i].status))

    if len(remaining_numbers) < 3:
        #ERROR
        print("ERROR #1")
        return ["?", "?", "?", "Error: Information provided is conflicted.\n         Hence, there is no solution!"]

    # now we gonna split them into two lists. "verified" which includes all the keys and certains, and the "non_verified" that includes possibles.
    verified = []
    non_verified = []  # both made out of number objects
    for i in range(len(remaining_numbers)):
        if (remaining_numbers[i].status == "key") or (remaining_numbers[i].status == "certain"):
            verified.append(remaining_numbers[i])
        elif remaining_numbers[i].status == "possible":
            non_verified.append(remaining_numbers[i])

    print("verified:")
    for i in range(len(verified)):
        print("Num: " + str(verified[i].num) + ", slots: " + str(verified[i].slots) + ", status: " + str(verified[i].status))
    print("non_verified:")
    for i in range(len(non_verified)):
        print("Num: " + str(non_verified[i].num) + ", slots: " + str(non_verified[i].slots) + ", status: " + str(non_verified[i].status))

    if len(verified) > 3:
        #ERROR
        print("ERROR #2")
        return ["?", "?", "?", "Error: Information provided is conflicted.\n         Hence, there is no solution!"]

    print("\nLet's sort the verified objects.")
    verified = verified_sorting(verified)
    if verified == "process failed":
        #ERROR
        print("ERROR #3, verified couldn't be sorted.")
        return ["?", "?", "?", "Error: Information provided is conflicted.\n         Hence, there is no solution!"]

    print("\nverified after getting sorted:")
    for i in range(len(verified)):
        print("Num: " + str(verified[i].num) + ", slots: " + str(verified[i].slots) + ", status: " + str(
            verified[i].status))

    # CHECK IF THE VERIFIED IS COMPLETE BEFORE MOVING ON, if so, then we Won! we can stop this whole operation.
    if len(verified) == 3:
        print("\nWe got 3 verified, lets check them last time.")

        #Let's check if the 3 verified numbers fulfill line retirement:
        if not check_line_retirement(data.numbers, data.linesinfo, data.line_correct_numbers, data.lines):
            #ERROR logic
            print("ERROR #4, Line retirement don't checks out")
            return ["?", "?", "?", "Error: Information provided is conflicted.\n         Hence, there is no solution!"]

        #Let's check if all verified numbers are keys(aka know their positions)
        if (verified[0].status != "key") or (verified[1].status != "key") or (verified[2].status != "key"):
            # ERROR info
            print("ERROR #654, information provided isn't enough")
            return ["?", "?", "?", "Error: Information provided is inconclusive!\n        There are 2 possible solutions."]
            # Through testing, I discovered that you could only have 2 or 3 objects to be certain, and in both cases, possible solutions is always 2
        else:
            print("VICTORY! the 3 keys have been found.")

            print("num: " + str(verified[0].num) + ", slots: " + str(verified[0].slots))
            print("num: " + str(verified[1].num) + ", slots: " + str(verified[1].slots))
            print("num: " + str(verified[2].num) + ", slots: " + str(verified[2].slots))

            if verified[0].slots[0] == 1: left_digit = verified[0].num
            elif verified[1].slots[0] == 1: left_digit = verified[1].num
            else: left_digit = verified[2].num  # verified[2].slots[0] == 1
            if verified[0].slots[1] == 1: middle_digit = verified[0].num
            elif verified[1].slots[1] == 1: middle_digit = verified[1].num
            else: middle_digit = verified[2].num  # verified[2].slots[1] == 1
            if verified[0].slots[2] == 1: right_digit = verified[0].num
            elif verified[1].slots[2] == 1: right_digit = verified[1].num
            else: right_digit = verified[2].num  # verified[2].slots[2] == 1

            return [left_digit, middle_digit, right_digit, "Puzzle Solved!"]

    print("\nWe haven't found the answer yet, therefore we must move on to the next step.")


    print("\n---------------------COMBINATIONS TESTING PHASE---------------------\n")

    needed = 3 - len(verified)  # the needed variable counts how many objects do we need from the unverified to complete the verified into 3.
    possible_combinations = create_possible_combinations(non_verified, needed)

    # add verified to each possible combination
    for i in range(len(possible_combinations)):
        for k in range(len(verified)):
            possible_combinations[i].append(verified[k])

    # now we have possible_combinations ready.

    # print them out
    for i in range(len(possible_combinations)):
        print("possible_combinations[" + str(i) + "] (+ verified objects):")
        for p in range(3):
            print("Num: " + str(possible_combinations[i][p].num) + ", slots: " + str(possible_combinations[i][p].slots)
                  + ", status: " + str(possible_combinations[i][p].status))

    successful_combinations = []  # the combinations that succeed will end up here.

    print("\nLet's test them out................................................")

    for i in range(len(possible_combinations)):

        print("\npossible_combinations[" + str(i) + "]: ")
        for p in range(3):
            print("Num: " + str(possible_combinations[i][p].num) + ", slots: " + str(possible_combinations[i][p].slots)
            + ", status: " + str(possible_combinations[i][p].status))

        # lets create the possible combination duplicate so we can change values to the objects without affecting all objects of the same kind.
        # You have to create brand new objects that are duplicates of the current combination because if you use the original objects and you
        # make changes to its attributes (in verified_sorting), then it will modify all other objects of the same number in other combinations,
        # which will jeopardize  the testing of other combinations. Ex: if your current combination has number 6, and 6 has "possible" status,
        # then it will become to "certain" or "key" in all other combinations beside the current one.
        obj_1 = numbeer(possible_combinations[i][0].num)
        obj_2 = numbeer(possible_combinations[i][1].num)
        obj_3 = numbeer(possible_combinations[i][2].num)
        # you can't say obj_1.slots = possible_combinations[i][0].slots because that will trigger an awful bug, so you gotta keep it the long way.
        # The bug is basically change the number object in all combinations besides the current. It's an issue with how Python operates.
        obj_1.slots = [possible_combinations[i][0].slots[0], possible_combinations[i][0].slots[1], possible_combinations[i][0].slots[2]]
        obj_2.slots = [possible_combinations[i][1].slots[0], possible_combinations[i][1].slots[1], possible_combinations[i][1].slots[2]]
        obj_3.slots = [possible_combinations[i][2].slots[0], possible_combinations[i][2].slots[1], possible_combinations[i][2].slots[2]]
        obj_1.status = "certain"
        obj_2.status = "certain"
        obj_3.status = "certain"

        # Since we switched all objects to certain before we send them to here(including keys),
        # this will fix the status back to "key" for those who were keys.
        if (obj_1.slots[0] == 1) or (obj_1.slots[1] == 1) or(obj_1.slots[2] == 1):
            obj_1.status = "key"
        if (obj_2.slots[0] == 1) or (obj_2.slots[1] == 1) or(obj_2.slots[2] == 1):
            obj_2.status = "key"
        if (obj_3.slots[0] == 1) or (obj_3.slots[1] == 1) or(obj_3.slots[2] == 1):
            obj_3.status = "key"
        # oke done

        current_combination = [obj_1, obj_2, obj_3]  # the combination we are currently testing

        # print stuff
        print("current combination: ")
        for p in range(3):
            print("Num: " + str(current_combination[p].num) + ", slots: " + str(current_combination[p].slots)
            + ", status: " + str(current_combination[p].status))

        # To preform the line retirement test, I need to make new temporary data.number_objects. But for the numbers that
        # are in the current_combination, I will take them from current_combination and replace the ones in
        # data.number_objects with the one from current_combination. This new array will be called number_objects_clone.
        number_objects_clone = []
        for number in range(10):
            if current_combination[0].num == number:
                number_objects_clone.append(current_combination[0])
            elif current_combination[1].num == number:
                number_objects_clone.append(current_combination[1])
            elif current_combination[2].num == number:
                number_objects_clone.append(current_combination[2])
            else:
                number_objects_clone.append(data.numbers[number])

        # print stuff
        print("number_objects clone: ")
        for t in range(10):
            print("Num: " + str(number_objects_clone[t].num) + ", slots: " + str(number_objects_clone[t].slots) +
                  ", status: " + str(number_objects_clone[t].status))


        # Now we test current_combination as if it's verified. If we encounter an issue or get "process failed", then we scratch this combination.
        if (verified_sorting(current_combination) != "process failed") and\
        (check_line_retirement(number_objects_clone, data.linesinfo, data.line_correct_numbers, data.lines)):
            print("|||\nSuccess! It is added to successful_combinations.")
            successful_combinations.append(verified_sorting(current_combination))
        else:
            print("|||\nFailure! It is NOT added to successful_combinations.")

    print("\n---------------------COMBINATIONS TESTING PHASE OVER---------------------\n")
    print("\nWe now have successful_combinations: ")
    # print them out
    for i in range(len(successful_combinations)):
        print("successful_combinations[" + str(i) + "]:")
        for p in range(3):
            print("Num: " + str(successful_combinations[i][p].num) + ", slots: " + str(successful_combinations[i][p].slots)
                  + ", status: " + str(successful_combinations[i][p].status))

    if len(successful_combinations) > 1:
        # INFO ERROR
        print("ERROR #5")
        # Lets count how many possible solutions there are. Through testing, I discovered this...
        total_solutions = 0
        for i in successful_combinations:
            if (i[0].status == "certain") or (i[1].status == "certain") or (i[2].status == "certain"):
                total_solutions += 2
            else:
                total_solutions += 1
        return ["?", "?", "?", "Error: Information provided is inconclusive!\n        There are " + str(total_solutions) + " possible solutions."]
    elif len(successful_combinations) == 0:
        # LOGIC ERROR
        print("ERROR #6")
        return ["?", "?", "?", "Error: Information provided is conflicted.\n         Hence, there is no solution!"]
    else:  # len(successful_combinations) == 1
        print("There is only 1 successful combination. Let's see if it checks out.")
        # final check & send keys. no way about this, when we calling this method, the array is 3 and already sorted/wrapped up
        if (successful_combinations[0][0].status != "key") or (successful_combinations[0][1].status != "key") or (successful_combinations[0][2].status != "key"):
            # ERROR info
            print("|ERROR #235")
            return ["?", "?", "?", "Error: Information provided is inconclusive!\n        There are 2 possible solutions."]
        else:
            print("|HOORAY!!! the 3 keys have been found.")

            print("num: " + str(successful_combinations[0][0].num) + ", slots: " + str(successful_combinations[0][0].slots))
            print("num: " + str(successful_combinations[0][1].num) + ", slots: " + str(successful_combinations[0][1].slots))
            print("num: " + str(successful_combinations[0][2].num) + ", slots: " + str(successful_combinations[0][2].slots))

            if successful_combinations[0][0].slots[0] == 1: left_digit = successful_combinations[0][0].num
            elif successful_combinations[0][1].slots[0] == 1: left_digit = successful_combinations[0][1].num
            else: left_digit = successful_combinations[0][2].num  # successful_combinations[0][2].slots[0] == 1
            if successful_combinations[0][0].slots[1] == 1: middle_digit = successful_combinations[0][0].num
            elif successful_combinations[0][1].slots[1] == 1: middle_digit = successful_combinations[0][1].num
            else: middle_digit = successful_combinations[0][2].num  # successful_combinations[0][2].slots[1] == 1
            if successful_combinations[0][0].slots[2] == 1: right_digit = successful_combinations[0][0].num
            elif successful_combinations[0][1].slots[2] == 1: right_digit = successful_combinations[0][1].num
            else: right_digit = successful_combinations[0][2].num  # successful_combinations[0][2].slots[2] == 1

            return [left_digit, middle_digit, right_digit, "Puzzle Solved!"]
#  ITS OVER

def loop_phase1_check_and_distribute(data, turn):  # This function is tested, seems to be working properly.
    """This function takes data[object] and turn [integer] that represents the line we are working with in this function(line = turn+1).
    This function is executed only once for each line.
    The first thing it does is give values to the data.line_correct_numbers array from data.hintboxes, this won't do anything
    here, but we will use the data.line_correct_numbers array later on in the program, we just give it the appropriate
    values here.
    The rest of this function is to preform a process on each number objects in the line we have [turn]. The process is
    to take the number object and decide if it's well placed or misplaced based on what the hint boxes says. It will
    eventually help us narrow down where this object land(if it ever), it also helps us to detect whether it's a valid
    number and it's status. Basically process of elimination. It checks if there are conflict and if a number does
    so, then it kills it by giving it "dead" status. if no conflict, then it distribute information. """

    print("\nloop_phase1_check_and_distribute:\n|turn = " + str(turn))
    print("|data.hintboxes: " + str(data.hintboxes))
    print("|the hint box # of this line is " + str(data.hintboxes[turn]))

    if data.hintboxes[turn] == 0:  # 0 numbers are correct
        data.line_correct_numbers[turn] = 0
        placement = "misplaced"
    elif data.hintboxes[turn] == 1:  # 1 number is correct, but misplaced
        data.line_correct_numbers[turn] = 1
        placement = "misplaced"
    elif data.hintboxes[turn] == 2:  # 1 number is correct, and well placed
        data.line_correct_numbers[turn] = 1
        placement = "well placed"
    elif data.hintboxes[turn] == 3:  # 2 numbers are correct, but misplaced
        data.line_correct_numbers[turn] = 2
        placement = "misplaced"
    elif data.hintboxes[turn] == 4:  # 2 numbers are correct, and well placed
        data.line_correct_numbers[turn] = 2
        placement = "well placed"
    elif data.hintboxes[turn] == 5:  # 3 numbers are correct, but misplaced
        data.line_correct_numbers[turn] = 3
        placement = "misplaced"
    else:  # as in data.hintboxes[turn] == 6: # 3 number are correct, and well placed
        data.line_correct_numbers[turn] = 3
        placement = "well placed"

    # we will repeat this process 3 time. 1st for the left slot, 2nd for middle slot, 3rd for right slot. All for a single line
    for line_slot in range(3):  # cuz there are 3 slots in the line. The following code is done 3 times, once for each slot.

        print("|*We in the [" + str(line_slot) + "] slot of the turn " + str(turn))
        print("|The number object is: " + str(data.numbers[data.linesinfo[turn][line_slot]].num) + ", its slots: "
        + str(data.numbers[data.linesinfo[turn][line_slot]].slots) + ", its status: " + str(data.numbers[data.linesinfo[turn][line_slot]].status))

        if placement == "misplaced":
            print(" |placement is misplaced")
            if data.numbers[data.linesinfo[turn][line_slot]].slots[line_slot] != 1:  # no contradiction
                print(" |no contradiction")
                data.numbers[data.linesinfo[turn][line_slot]].slots[line_slot] = 0
                if data.numbers[data.linesinfo[turn][line_slot]].status == "initial":
                    data.numbers[data.linesinfo[turn][line_slot]].status = "possible"
            else:  # if it's = 1 (a.k.a it's indeed located in this slot, that is a contradiction with the hint. the hint says it isn't.)
                print(" |yes contradiction")
                if (data.numbers[data.linesinfo[turn][line_slot]].status == "initial")\
                or (data.numbers[data.linesinfo[turn][line_slot]].status == "possible"):
                    data.numbers[data.linesinfo[turn][line_slot]].status = "dead"
                    print(" |set recycle = True")
                    data.recycle = True
                elif (data.numbers[data.linesinfo[turn][line_slot]].status == "key") \
                or (data.numbers[data.linesinfo[turn][line_slot]].status == "certain"):
                    # ERROR
                    print(" |ERROR #7")
                    return "process failed"


        elif placement == "well placed":
            print(" |The placement is well placed")

            # This part is to check for contradiction. Not well writing, but works fine.
            contradiction = 0  # just to initialize
            for number_slot in range(3):  # cuz there is 3 slots in the number object
                if ((number_slot != line_slot) and (data.numbers[data.linesinfo[turn][line_slot]].slots[number_slot] != 1)) \
                or ((number_slot == line_slot) and (data.numbers[data.linesinfo[turn][line_slot]].slots[number_slot] != 0)):
                    contradiction = False  # we're good, no contradiction
                else:
                    contradiction = True  # there is contradiction
                    break

            if not contradiction:  # if there is no contradiction
                print(" |no contradiction")
                if (data.numbers[data.linesinfo[turn][line_slot]].status == "initial") \
                or (data.numbers[data.linesinfo[turn][line_slot]].status == "possible") \
                or (data.numbers[data.linesinfo[turn][line_slot]].status == "certain"):
                    # grant info
                    for number_slot in range(3):
                        if number_slot != line_slot:
                            data.numbers[data.linesinfo[turn][line_slot]].slots[number_slot] = 0
                        else:
                            data.numbers[data.linesinfo[turn][line_slot]].slots[number_slot] = 1
                    if data.numbers[data.linesinfo[turn][line_slot]].status == "initial":
                        data.numbers[data.linesinfo[turn][line_slot]].status = "possible"
                    if data.numbers[data.linesinfo[turn][line_slot]].status == "certain":
                        data.numbers[data.linesinfo[turn][line_slot]].status = "key"

            else:  # if there is contradiction
                print(" |yes contradiction")
                # if the status is initial or possible, then go ahead and declare it dead.
                if (data.numbers[data.linesinfo[turn][line_slot]].status == "initial")\
                or (data.numbers[data.linesinfo[turn][line_slot]].status == "possible"):
                    data.numbers[data.linesinfo[turn][line_slot]].status = "dead"
                    print(" |set data.recycle = True")
                    data.recycle = True
                # else if it's already verified, then we have an  ERROR
                elif (data.numbers[data.linesinfo[turn][line_slot]].status == "key") \
                or (data.numbers[data.linesinfo[turn][line_slot]].status == "certain"):
                    # ERROR, a validated number has contradicted.
                    print(" |ERROR #8: a validated number has contradicted.")
                    return "process failed"

        print("|The number object after distribution: " + str(data.numbers[data.linesinfo[turn][line_slot]].num) + ", its slots: " + str(
                data.numbers[data.linesinfo[turn][line_slot]].slots) + ", its status: " + str(
                data.numbers[data.linesinfo[turn][line_slot]].status))

        # lastly, we send the number object to obj_number_self_wrap_up where it fills some of the holes. For Example:
        # if two spots are "false", it tick the third as "true".
        if (data.numbers[data.linesinfo[turn][line_slot]].status != "dead")\
        and (data.numbers[data.linesinfo[turn][line_slot]].status != "key"):  # if it's dead or key, then no need to preform the next step.
            print("|Lets hand off the number object to obj_number_self_wrap_up\n|||")
            data.numbers[data.linesinfo[turn][line_slot]] = obj_number_self_wrap_up(data.numbers[data.linesinfo[turn][line_slot]])
            print("|||\n|Okay we back to phase1 with the same number object")
            if data.numbers[data.linesinfo[turn][line_slot]] == "process failed":
                #ERROR
                print("|ERROR #9")
                return "process failed"
            # so you sent the object, and it may very much have died. so check now if it died to reset the cycle
            if data.numbers[data.linesinfo[turn][line_slot]].status == "dead":
                print("|set data.recycle = True")
                data.recycle = True

    print("Function Done\n")
    return data
# This the end of this function.

def loop_phase2_disqualify_and_retire(data, turn):  # This function is tested, seems to be working properly.
    """This function takes data [object] and turn [int] which represents what line we are working with in this function
    (line = turn + 1). It focuses on taking the number objects in this line and count how many of them is correct and
    incorrect and it compares it to what is provided by the hint boxes. To see if it matches. If it does accurately match,
    then it updates the status of these number objects accordingly."""
    print("\nloop_phase2_disqualify_and_retire:\n|turn = " + str(turn))
    print("|Left object of the line: " + str(data.numbers[data.linesinfo[turn][0]].num) + ", its status: " + str(data.numbers[data.linesinfo[turn][0]].status))
    print("|Middle object of the line: " + str(data.numbers[data.linesinfo[turn][1]].num) + ", its status: " + str(data.numbers[data.linesinfo[turn][1]].status))
    print("|Right object of the line: " + str(data.numbers[data.linesinfo[turn][2]].num) + ", its status: " + str(data.numbers[data.linesinfo[turn][2]].status))

    # SET VAR
    correct_numbers = data.line_correct_numbers[turn]  # a.k.a keys
    incorrect_numbers = 3 - data.line_correct_numbers[turn]

    incorrect_numbers_counter = 0
    correct_numbers_counter = 0

    # COUNT the status of the number objects in this line

    # the number object in the left slot of the line:
    if data.numbers[data.linesinfo[turn][0]].status == "dead":
        incorrect_numbers_counter += 1
    elif (data.numbers[data.linesinfo[turn][0]].status == "key") or (data.numbers[data.linesinfo[turn][0]].status == "certain"):
        correct_numbers_counter += 1

    # the number object in the middle slot of the line:
    if data.numbers[data.linesinfo[turn][1]].status == "dead":
        incorrect_numbers_counter += 1
    elif (data.numbers[data.linesinfo[turn][1]].status == "key") or (data.numbers[data.linesinfo[turn][1]].status == "certain"):
        correct_numbers_counter += 1

    # the number object in the right slot of the line:
    if data.numbers[data.linesinfo[turn][2]].status == "dead":
        incorrect_numbers_counter += 1
    elif (data.numbers[data.linesinfo[turn][2]].status == "key") or (data.numbers[data.linesinfo[turn][2]].status == "certain"):
        correct_numbers_counter += 1

    print("|correct_numbers: " + str(correct_numbers))
    print("|incorrect_numbers: " + str(incorrect_numbers))
    print("|correct_numbers_counter: " + str(correct_numbers_counter))
    print("|incorrect_numbers_counter: " + str(incorrect_numbers_counter))

    # CHECK FOR LOGIC ERRORS
    if incorrect_numbers_counter > incorrect_numbers:
        #ERROR
        print("|ERROR #10: incorrect_numbers_counter > incorrect_numbers")
        return "process failed"

    if correct_numbers_counter > correct_numbers:
        #ERROR
        print("|ERROR #11: correct_numbers_counter > correct_numbers")
        return "process failed"

    # CHECK IF the GOAL reached
    print("|Check if goal is reached.... ")
    if incorrect_numbers_counter == incorrect_numbers:
        print("|Yup, incorrect_numbers_counter == incorrect_numbers")
        if data.numbers[data.linesinfo[turn][0]].status != "dead":
            data.numbers[data.linesinfo[turn][0]].status = "certain"
        if data.numbers[data.linesinfo[turn][1]].status != "dead":
            data.numbers[data.linesinfo[turn][1]].status = "certain"
        if data.numbers[data.linesinfo[turn][2]].status != "dead":
            data.numbers[data.linesinfo[turn][2]].status = "certain"
        print("|set recycle = True")
        data.recycle = True
        data.retired[turn] = True
        print("|--This line has retired--")

    elif correct_numbers_counter == correct_numbers:
        print("|Yup, correct_numbers_counter == correct_numbers")
        if (data.numbers[data.linesinfo[turn][0]].status != "key") and (data.numbers[data.linesinfo[turn][0]].status != "certain"):
            data.numbers[data.linesinfo[turn][0]].status = "dead"
        if (data.numbers[data.linesinfo[turn][1]].status != "key") and (data.numbers[data.linesinfo[turn][1]].status != "certain"):
            data.numbers[data.linesinfo[turn][1]].status = "dead"
        if (data.numbers[data.linesinfo[turn][2]].status != "key") and (data.numbers[data.linesinfo[turn][2]].status != "certain"):
            data.numbers[data.linesinfo[turn][2]].status = "dead"
        print("|set recycle = True")
        data.recycle = True
        data.retired[turn] = True
        print("|--This line has retired--")

    print("|Left object of the line: " + str(data.numbers[data.linesinfo[turn][0]].num) + ", its status: " + str(data.numbers[data.linesinfo[turn][0]].status))
    print("|Middle object of the line: " + str(data.numbers[data.linesinfo[turn][1]].num) + ", its status: " + str(data.numbers[data.linesinfo[turn][1]].status))
    print("|Right object of the line: " + str(data.numbers[data.linesinfo[turn][2]].num) + ", its status: " + str(data.numbers[data.linesinfo[turn][2]].status))

    # NUMBER OBJECTS WRAP UP. Take all 3 number objects, one at a time.
    for i in range(3):
        if data.numbers[data.linesinfo[turn][i]].status != "dead":
            print("|Let's take the number object in line's slot[" + str(i) + "] to obj_number_self_wrap_up\n|||")
            data.numbers[data.linesinfo[turn][i]] = obj_number_self_wrap_up(data.numbers[data.linesinfo[turn][i]])
            print("|||\n|Okay we back to phase2 with the same number object")

            if data.numbers[data.linesinfo[turn][i]] == "process failed":
                # ERROR
                print("|ERROR #12: process failed at obj_number_self_wrap_up")
                return "process failed"
            # if the object died, then set recycle to True
            if data.numbers[data.linesinfo[turn][i]].status == "dead":
                print("|set data.recycle = True")
                data.recycle = True


    print("Function Done\n")
    return data
# This the end of this function.

def obj_number_self_wrap_up(number_object):  # This function is tested, seems to be working properly.
    # This function takes a number object and uses the information it has to find the rest of information. It updates...
    # ...the object and returns it back. So if the number_object.slots = [-1, 0, 0], then it will...
    # ...update it to [1, 0, 0]. And it also update the status appropriately. If there are any conflicts, then...
    # ...this function returns "process failed".

    # I noticed that there are no cases to get a number objects with slots like [-1, 0, 1]. You can't have a slot to...
    # ...be = 1 and other(s) to be = -1, they both have to be = 0. That's because any part of code in this program...
    # ...that makes a slot = 1, it will make others = 0. Therefore, I do not need a case that would change...
    # [1, 0 -1] to [1, 0 0] here. A lot of code is questionable because you don't think it covers all cases and you...
    # ...ask what ifs. Know that it's all covered. You just don't know.

    print("obj_number_self_Wrap_up:\n|number_object = " + str(number_object.num))
    print("|slots = " + str(number_object.slots) + ", status = " + str(number_object.status))

    # if u have two false positions, then just verify the third as true.
    if (number_object.slots[0] != 0) and (number_object.slots[1] == 0) and (number_object.slots[2] == 0):
        number_object.slots[0] = 1
    if (number_object.slots[0] == 0) and (number_object.slots[1] != 0) and (number_object.slots[2] == 0):
        number_object.slots[1] = 1
    if (number_object.slots[0] == 0) and (number_object.slots[1] == 0) and (number_object.slots[2] != 0):
        number_object.slots[2] = 1

    # if the object is certain, and you have all the position info, then make it key.
    if number_object.status == "certain" and \
    ((number_object.slots[0] == 1) or (number_object.slots[1] == 1) or (number_object.slots[2] == 1)):
        number_object.status = "key"

    # if all positions are false, then the object can't be true, so declare it false.
    if (number_object.slots[0] == 0) and (number_object.slots[1] == 0) and (number_object.slots[2] == 0):
        if number_object.status == "certain":
            # ERROR
            print("|process failed")
            return "process failed"
        else:
            number_object.status = "dead"

    print("|After....")
    print("|slots = " + str(number_object.slots) + ", status = " + str(number_object.status))

    return number_object
# This the end of this function.

def verified_sorting(number_objects):  # This function is tested, seems to be working properly.
    # This function takes a list contains 3 number objects, it's as if they were the keys, and it uses information...
    # ...from one object to help another find its location. If this function encountered a conflict between the...
    # ...objects, it returns "process failed". Otherwise it returns the same list(but now with the updated objects).
    # Example: if number_objects[0].slots = [0, 1, 0] and number_objects[1].slots = [-1, -1, 0], then number_objects[1]...
    # knows it can't be in the middle, so it becomes number_objects[1].slots = [-1, 0, 0]. So then it uses obj_self_wrap_up...
    # ...function and becomes number_objects[1].slots = [1, 0, 0]
    # This function doesn't seem to be perfect as in could be cut shorter and more efficient, but this works, so I'll keep it.
    # The whole print statements are getting annoying and confusing. They aren't even necessary. Feel free to erase them.
    # Note: in the original program, it's not exclusively designed to have 3 number objects in number_objects. It can...
    # be anywhere (0-3), but I realized you don't need to call this function only when you have 3 objects. So this...
    # ...can still accept more or less than 3 objects, but I will only call it when I have exactly 3. JS.
    # Actually, nvm. This function take any amount. 1, 2 or 3.

    print("|||\nverified_sorting:")
    for i in range(len(number_objects)):
        print("|number_objects[" + str(i) + "], num: " + str(number_objects[i].num) + ", slots: " + str(number_objects[i].slots) +
        ", status: " + str(number_objects[i].status))

    current = 0
    while current < len(number_objects):

        '''Brief explanation: So we will take one object at a time from number_objects and take it though a process.
         The process is we take the object(current) and compare it to all other objects in number_objects. We collect
         information throughout this process, and at the end of it, we will use this information to deduce where the 
         current object can or can't be. Again, the process will be repeated 3 times, each time is for each object 
         in number_objects. This will be especially useful when dealing with objects of certain status where we don't
         know their exact slot. And if we came across a conflict, we would return "process failed".  
         TBH, I don't remember this part very well, so if you want more info on this, refer back to the original program. 
         '''

        # those variables are used when we check a number object whose condition is certain with another number object...
        # ... whose condition is also certain. It will help us eliminate slots.
        left_counter = 0  # will count how many 'certain's can possibly land in the left slot
        middle_counter = 0
        right_counter = 0
        certain_interactions = 0
        slots_used = 0

        for other in range(len(number_objects)):

            if number_objects[other].num == number_objects[current].num:
                continue  # if we are comparing the same object with itself then skip this iteration.

            if number_objects[current].status == "key":
                if (number_objects[current].slots[0] == 1) and (number_objects[other].slots[0] == 1):
                    #ERROR, the two objects overlap in the left slot
                    print("|return process failed")
                    return "process failed"
                if (number_objects[current].slots[1] == 1) and (number_objects[other].slots[1] == 1):
                    #ERROR, the two objects overlap in the middle slot
                    print("|return process failed")
                    return "process failed"
                if (number_objects[current].slots[2] == 1) and (number_objects[other].slots[2] == 1):
                    #ERROR, the two objects overlap in the right slot
                    print("|return process failed")
                    return "process failed"

            # if object_other.status == "key". we don't really need to write this if else statement. it will do the same thing either way.
            if number_objects[current].status == "certain":
                if number_objects[other].slots[0] == 1:
                    number_objects[current].slots[0] = 0
                if number_objects[other].slots[1] == 1:
                    number_objects[current].slots[1] = 0
                if number_objects[other].slots[2] == 1:
                    number_objects[current].slots[2] = 0

                if number_objects[other].status == "certain":  # if meeting with a certain.
                    if number_objects[other].slots[0] == -1:
                        left_counter += 1  # it may land on the left so we add one to this counter
                    if number_objects[other].slots[1] == -1:
                        middle_counter += 1
                    if number_objects[other].slots[2] == -1:
                        right_counter += 1
                    certain_interactions += 1

                print("|send current object " + str(number_objects[current].num) + " to obj_number_self_wrap_up\n|||")
                number_objects[current] = obj_number_self_wrap_up(number_objects[current])
                print("|||\n|back to verified_sorting:")
                if number_objects[current] == "process failed":
                    #ERROR
                    print("|return process failed")
                    return "process failed"

                if number_objects[current].status == "key":
                    current = -1  # if a certain has been confirmed to a key, then reset the cycle so that previous certains has the chance.

        # now that we compared the current object with the other objects and collected some information, now we use that...
        # ...information to eliminate slots and narrow it down to one where the current object must be. We may eliminate...
        # ...one or two slots, and hopefully that leaves us with the one correct slot. This may leads to all slots being...
        # ...crossed out which leads to return "process failed".
        if number_objects[current].status == "certain":
            if left_counter > 0:
                slots_used += 1
            if middle_counter > 0:
                slots_used += 1
            if right_counter > 0:
                slots_used += 1
            # if (the amount of times the current object interacted with other objects that are also certain) matches the amount of slots they may lan on,
            # then all these slot will be used. Those other certain objects will land on these slots and take them.
            #  so the current object cannot be in any of those slots whether its the right, middle, or left.
            if slots_used == certain_interactions:
                if left_counter > 0:  # those slots doesnt have to be filled to the top so write >0. It doesn't matter how much in each. if it's >0, then it's taken.
                    number_objects[current].slots[0] = 0
                if middle_counter > 0:
                    number_objects[current].slots[1] = 0
                if right_counter > 0:
                    number_objects[current].slots[2] = 0

            print("|send current object " + str(number_objects[current].num) + " to obj_number_self_wrap_up\n|||")
            number_objects[current] = obj_number_self_wrap_up(number_objects[current])
            print("|||\n|back to verified_sorting:")
            if number_objects[current] == "process failed":
                # ERROR
                print("|return process failed.")
                return "process failed"

            if number_objects[current].status == "key":
                current = -1  # if it became key, then lets begin all over with previous objects.
                # We say -1 cuz current will get += 1 at the last line of the loop so it gets to 0
        current += 1


    print("|After...")
    for i in range(len(number_objects)):
        print("|number_objects[" + str(i) + "], num: " + str(number_objects[i].num) + ", slots: " + str(number_objects[i].slots)
              + ", status: " + str(number_objects[i].status))

    return number_objects
# This the end of this function.

def check_line_retirement(number_objects, lines_data, amount_of_keys, amount_of_lines):  # This function is tested, seems to be working properly.
    # This function takes 4 parameters:
    # 1- number_objects: 1 dimensional array that carries 10 number objects (0-9) and their attributes.
    # 2- lines_data: 2 dimensional array (length of 10) that carries the numbers in each line. Each element is a...
    # ...sub-array of 3 integers that represents a line and carries the line's three numbers.
    # 3- amount_of_keys: 1 dimensional array that carries 10 integers which represents the amount of correct...
    # ..numbers at each hint box.
    # 4- amount_of_lines: self explanatory (1-10)
    # This function take these parameters and checks if the information satisfies the hint boxes by reaching the...
    # ...amount of keys as specified in hint box. If it does, it returns True. If it doesn't, it returns False.

    print("|||\ncheck_line_retirement: ")

    for turn in range(amount_of_lines):

        # SET UP VARIABLES
        keys = amount_of_keys[turn]
        key_counter = 0

        print("|*turn:" + str(turn) + ", keys = " + str(keys))
        print("|Num: " + str(number_objects[lines_data[turn][0]].num) + ", status: " + str(number_objects[lines_data[turn][0]].status))
        print("|Num: " + str(number_objects[lines_data[turn][1]].num) + ", status: " + str(number_objects[lines_data[turn][1]].status))
        print("|Num: " + str(number_objects[lines_data[turn][2]].num) + ", status: " + str(number_objects[lines_data[turn][2]].status))

        # COUNT
        #left slot of the line #(turn +1):
        if (number_objects[lines_data[turn][0]].status == "key") or (number_objects[lines_data[turn][0]].status == "certain"):
            key_counter += 1
        # middle slot of the line #(turn +1):
        if (number_objects[lines_data[turn][1]].status == "key") or (number_objects[lines_data[turn][1]].status == "certain"):
            key_counter += 1
        # right slot of the line #(turn +1):
        if (number_objects[lines_data[turn][2]].status == "key") or (number_objects[lines_data[turn][2]].status == "certain"):
            key_counter += 1

        # CHECK IF GOAL IS REACHED
        print("|key_counter = " + str(key_counter))
        if key_counter != keys:
            print("|return False")
            return False
    print("|return True")
    return True
# This the end of this function.

def create_possible_combinations(list_1d, quantity):  # This function is tested, seems to be working properly.
    # This function takes 2 parameters:
    # 1- list_1d: 1 dimensional array. It can contain any data type, but in this particular program, the data type is always a number object.
    # 2- quantity: an integer. It has to be either 1, 2, or 3.
    # This function will take the 2 parameters and create a 2D array that contain all possible combinations of the elements in...
    # ... the list_1d, each combination will have the size of the quantity. The function will return the 2D array.
    # For example:
    # list_1d = [0, 3, 7, 9], quantity = 3
    # the function returns [[0, 3, 7], [0, 3, 9], [0, 7, 9], [3, 7, 9]]

    #let's initialize the 2D array
    possible_combinations = []

    combination_num = 0

    for t in range(len(list_1d)):
        if quantity == 1:
            # if the quantity is 1, then we preform the simple action of taking one element from list_1d and add...
            # ...it to the sub-array at 'combination_num' within the larger possible_combinations array, and we...
            # ...don't do anything in the following loops.
            possible_combinations.append([list_1d[t]])
            combination_num += 1
        for tt in range(t+1, len(list_1d)):
            if quantity == 2:
                # however, if quantity is 2, then we preform these simple actions which takes...
                # ...into account the the first loop but ignores the next one.
                possible_combinations.append([list_1d[t]])
                possible_combinations[combination_num].append(list_1d[tt])
                combination_num += 1
            for ttt in range(tt+1, len(list_1d)):
                if quantity == 3:
                    # moreover, if quantity is 3, then we preform these actions and skip the previous actions but we...
                    # ...still take into account the previous loops.
                    possible_combinations.append([list_1d[t]])
                    possible_combinations[combination_num].append(list_1d[tt])
                    possible_combinations[combination_num].append(list_1d[ttt])
                    combination_num += 1
    return possible_combinations
# This the end of this function.



# Testing the create_possible_combinations function
'''
array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
array = create_possible_combinations(array, 3)
print(array)
'''

# Testing the check_line_retirement function
'''
class number:
    def __init__(self, value):
        # more info to be added
        self.num = value  # just in case we needed this
        self.slots = [-1, -1, -1]  # -1 = unidentified, 0 = no, 1 = yes
        self.status = "initial"
number_objects = [number(0), number(1), number(2), number(3), number(4), number(5), number(6), number(7), number(8),
                number(9)]
number_objects[0].status = "dead"
number_objects[1].status = "key"
number_objects[2].status = "certain"
number_objects[3].status = "certain"
number_objects[4].status = "initial"
number_objects[5].status = "possible"
number_objects[6].status = "key"
number_objects[7].status = "key"
number_objects[8].status = "key"
number_objects[9].status = "dead"
lines_data = [
    [1, 0, 0],
    [1, 2, 0],
    [8, 6, 3],
    [7, 6, 1],
    [5, 4, 0],
    [2, 6, 1],
    [0, 8, 7],
    [0, 8, 0],
    [2, 0, 0],
    [0, 4, 9],
]

amount_of_keys = [1, 2, 3, 3, 0, 3, 2, 1, 1, 0]

amount_of_lines = 6

print(check_line_retirement(number_objects, lines_data, amount_of_keys, amount_of_lines))

'''

# Testing the obj_number_self_wrap_up function
'''
class number:
    def __init__(self, value):
        # more info to be added
        self.num = value  # just in case we needed this
        self.slots = [-1, -1, -1]  # -1 = unidentified, 0 = no, 1 = yes
        self.status = "initial"
obj = number(3)
obj.slots = [0, -1, 0]
obj.status = "certain"

obj = obj_number_self_wrap_up(obj)

print("\nobj: " + str(obj))
'''

# Testing the verified_sorting function
'''
class number:
    def __init__(self, value):
        # more info to be added
        self.num = value  # just in case we needed this
        self.slots = [-1, -1, -1]  # -1 = unidentified, 0 = no, 1 = yes
        self.status = "initial"
obj1 = number(3)
obj1.slots = [-1, -1, 0]
obj1.status = "certain"
obj2 = number(6)
obj2.slots = [0, 0, -1]
obj2.status = "possible"
obj3 = number(7)
obj3.slots = [0, -1, -1]
obj3.status = "possible"
print(verified_sorting([obj1, obj2, obj3]))
'''

# Testing the loop_phase2_disqualify_and_retire function
'''
class Structure(object):
    pass
# create the data object
data = Structure()

class number:
    def __init__(self, value):
        # more info to be added
        self.num = value  # just in case we needed this
        self.slots = [-1, -1, -1]  # -1 = unidentified, 0 = no, 1 = yes
        self.status = "initial"

data.linesinfo = [[1, 2, 3]]
data.line_correct_numbers = [1]
data.recycle = False
data.retired = [False]
data.numbers = [number(0),number(1),number(2),number(3),number(4),number(5),number(6),number(7),number(8),number(9)]

data.numbers[1].slots = [-1, -1, 0]; data.numbers[1].status = "dead"
data.numbers[2].slots = [-1, 0, 0]; data.numbers[2].status = "initial"
data.numbers[3].slots = [0, 0, 1]; data.numbers[3].status = "dead"

loop_phase2_disqualify_and_retire(data, 0)
'''

# Testing the loop_phase1_check_and_distribute function
'''
class Structure(object):
    pass
# create the data object
data = Structure()

class number:
    def __init__(self, value):
        # more info to be added
        self.num = value  # just in case we needed this
        self.slots = [-1, -1, -1]  # -1 = unidentified, 0 = no, 1 = yes
        self.status = "initial"

data.linesinfo = [[1, 2, 3]]
data.recycle = False
data.hintboxes = [2]
data.line_correct_numbers = [0]
data.numbers = [number(0),number(1),number(2),number(3),number(4),number(5),number(6),number(7),number(8),number(9)]

data.numbers[1].slots = [-1, -1, 0]; data.numbers[1].status = "dead"
data.numbers[2].slots = [-1, 0, 0]; data.numbers[2].status = "certain"
data.numbers[3].slots = [0, 0, 1]; data.numbers[3].status = "initial"

loop_phase1_check_and_distribute(data, 0)
'''