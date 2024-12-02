def print_high_scores(size: int, high_score_number: int, all_scores: dict):
    '''The high_score is  presented - the top players. If more than one player has the same score they will be 
    presented on the same row. 
    In parameters: Number of high scores to be presented, the size of the board and the dictionary with all results. 
    The key in the dictionary is size, and the results are stored in a list of lists [score, name]
    Development - comment on the players position using index after looping'''
    score_position = 1  # position on the score list
    index = 0  # position in the first list in all_scores[size]
    score_list_length = len(all_scores[size])

    if score_list_length > 1:
        all_scores[size] = sorted(
            # sorting the list from highest to lowest score
            all_scores[size], key=lambda x: x[0])
    print(f"\n***THE TOP PLAYERS FOR THE {
          size}x{size} board*** \n")
    print_scores = True
    while print_scores:
        if score_list_length < index+1:
            print_scores = False
        else:
            if score_position < 6:
                print(f"Rank {score_position}: ", end="")
                # prints score and name of the player
                print(
                    f"{all_scores[size][index][0]} rounds - {all_scores[size][index][1]}", end="")
                check_same_score = True
                while check_same_score:
                    if index == score_list_length-1:
                        print("\n")
                        check_same_score = False
                        print_scores = False
                    elif all_scores[size][index][0] != all_scores[size][index+1][0]:
                        index += 1
                        score_position += 1
                        print("\n")
                        check_same_score = False
                    else:
                        index += 1
                        print(f", {all_scores[size][index][1]} ", end="")


size = 2
my_score = 5
gaming_name = "Anna"
all_scores = {2: [[6, "Pelle"], [8, "Johan"],
                  [6, "Jens"], [5, "Mia"]], 4: [], 6: []}
all_scores[size].append([my_score, gaming_name])
print(all_scores)


print_high_scores(2, 5, all_scores)
