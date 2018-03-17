import os
import sys

commands = ['run', 'exit']
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
        sys.exit(0)

def main():
    command = get_command()
    print command


if __name__ == "__main__":
    main()
