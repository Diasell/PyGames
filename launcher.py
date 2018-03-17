import os
import sys

commands = ['run', 'listGames', 'help']
games = {
    'asteroids': 'Asteroids/asteroids.py'
}

def get_command():
    if len(sys.argv) >= 2:
        command = sys.argv[1]
        if command in commands:
            return command
        else:
            print "command you've entered is not supported. Run: <python launcher.py help> to get list of the commands available"
    else:
        print "command parameter missing. Example: python launcher.py <command> <game>"


def get_game():
    if len(sys.argv) >= 3:
        game = sys.argv[2]
        if game in games:
            return games[game]
        else:
            print "game not found. Please check available games with <listGames> command"


def show_games():
    respond = "List of the games available to play: "
    for key in games:
        respond +=  ' <' + key + '>'
    print respond


def help():
    respond = "List of commands: "
    for key in commands:
        respond += " <" + key + ">"
    print respond


def main():
    command = get_command()
    game = get_game()
    if (command == "run"):
        os.system('python ' + game)
    elif (command == "listGames"):
        show_games()
    elif (command == 'help'):
        help()



if __name__ == "__main__":
    main()
