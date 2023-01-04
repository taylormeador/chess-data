import sys
import math
from db import DB

# attempt db connection
try:
    print('\nAttempting to connect to database...')
    db = DB()
    print('Success!')
except:
    print('Error connecting to database. Exiting...')
    sys.exit()


def greet():
    print('**************************************************************************************')
    print('Welcome to chess-data cli. Type commands below. Type "help" for details about commands')
    print('**************************************************************************************')

def help():
    # print commands and arguments
    print('\n*********************************************************************************************')
    print('Valid commands:')
    print('  exit')
    print('  help')
    print('  bo -white_username -black_username [--strict]')
    print('       This returns the best opening for white and the best opening for black based on given usernames')
    print('       The optional "--strict" flag means that recommended openings output will only list openings that both colors have games in')
    print()


def best_opening(input):
    # check input for validity
    if len(input) < 3:
        print('invalid arguments for best opening command')
        return

    if input[1][0] != '-' or input[2][0] != '-':
        print('invalid syntax for best opening command')
        return

    # parse input
    white_username, black_username = input[1].replace('-', ''), input[2].replace('-', '')
    strict_mode = True if len(input) > 3 else False
    
    # query db
    white_best_openings_query = db.get_best_openings(white_username, 'white')
    black_best_openings_query = db.get_best_openings(black_username, 'black')
    white_worst_openings_query = db.get_worst_openings(white_username, 'white')
    black_worst_openings_query = db.get_worst_openings(black_username, 'black')

    # score openings and match best/worst to get composite score
    black_worst_openings = {}
    for result in black_worst_openings_query:
        black_worst_openings[result[0]] = {'ratio': float(result[3]), 'black_score': float((result[3] - 50) ** 2)}

    white_best_openings = {}
    for result in white_best_openings_query:
        white_score = float((result[3] - 50) ** 2)
        black_score = black_worst_openings[result[0]]['black_score'] if result[0] in black_worst_openings else 0
        white_best_openings[result[0]] = {
            'white_score': white_score, 
            'black_score': black_score,
            'composite_score': math.sqrt(white_score + black_score)}

    white_worst_openings = {}
    for result in white_worst_openings_query:
        white_worst_openings[result[0]] = {'ratio': float(result[3]), 'white_score': float((result[3] - 50) ** 2)}

    black_best_openings = {}
    for result in black_best_openings_query:
        black_score = float((result[3] - 50) ** 2)
        white_score = white_worst_openings[result[0]]['white_score'] if result[0] in white_worst_openings else 0
        black_best_openings[result[0]] = {
            'white_score': white_score, 
            'black_score': black_score,
            'composite_score': math.sqrt(white_score + black_score)}

    # pprint.pprint(white_best_openings)
    # pprint.pprint(black_best_openings)

    # print('White best ***************')
    # print(white_best_openings_query)
    # print('Black best ***************')
    # print(black_best_openings_query)
    # print('White worst ***************')
    # print(white_worst_openings_query)
    # print('Black worst ***************')
    # print(black_worst_openings_query)



    # print results to console
    print('\n***** White Best Openings *****')
    for result in white_best_openings_query:
        print(result[0])
        print('  # of Games: ' + str(result[1]))
        print('  # of Wins: ' + str(result[2]))
        print('  Win Ratio: ' + str(round(result[3], 2)))

    print('\n***** White Worst Openings *****')
    for result in white_worst_openings_query:
        print(result[0])
        print('  # of Games: ' + str(result[1]))
        print('  # of Losses: ' + str(result[2]))
        print('  Loss Ratio: ' + str(round(result[3], 2)))

    print('\n***** Black Best Openings *****')
    for result in black_best_openings_query:
        print(result[0])
        print('  # of Games: ' + str(result[1]))
        print('  # of Wins: ' + str(result[2]))
        print('  Win Ratio: ' + str(round(result[3], 2)))

    print('\n***** Black Worst Openings *****')
    for result in black_worst_openings_query:
        print(result[0])
        print('  # of Games: ' + str(result[1]))
        print('  # of Losses: ' + str(result[2]))
        print('  Loss Ratio: ' + str(round(result[3], 2)))

    print('\n***** Recommended Openings for White *****')
    i = 0
    for opening, stats in {k: v for k, v in sorted(white_best_openings.items(), key=lambda item: item[1]['composite_score'], reverse=True)}.items():
        if strict_mode:
            if stats['black_score'] == 0:
                continue
        i += 1
        print('\n#' + str(i), opening)
        print('  Composite Score:', round(stats['composite_score'], 2), '  White Score:', round(stats['white_score'], 2), '  Black Score:', round(stats['black_score'], 2))

    print('\n***** Recommended Openings for Black *****')
    i = 0
    for opening, stats in {k: v for k, v in sorted(black_best_openings.items(), key=lambda item: item[1]['composite_score'], reverse=True)}.items():
        if strict_mode:
            if stats['white_score'] == 0:
                continue
        i += 1
        print('\n#' + str(i), opening)
        print('  Composite Score:', round(stats['composite_score'], 2), '  White Score:', round(stats['white_score'], 2), '  Black Score:', round(stats['black_score'], 2))


def main():
    greet()

    # main loop - get user input and print results for valid commands
    while True:
        user_input = input('> ')
        user_input = user_input.split(' ')
        cmd = user_input[0]

        if cmd == 'help':
            help()

        elif cmd == 'exit':
            print('Exiting... goodbye!')
            sys.exit()

        elif cmd == 'bo':
            best_opening(user_input)
            

if __name__ == '__main__':
    main()
