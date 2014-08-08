#! /usr/bin/env python
"""
    Print a list of tests to see whether all required tools
    for this code package.
"""

from os import getcwd, unlink, path
from subprocess import call, Popen

number_of_spaces = 5


def print_warning(warning_string):
    print("-" * (number_of_spaces - 2) + "> " + warning_string)


def print_msg(message):
    print(" " * number_of_spaces + message)


def check_command(cmd_string, utility_name=None):
    """
        Try to execute "cmd_string", then use "utility_name" to echo messages.
    """
    temp_file = open("response.txt", 'w')
    if not utility_name:
        utility_name = cmd_string
    call("%s " % cmd_string, shell=True, cwd=getcwd(), stdout=temp_file,
         stderr=temp_file)
    temp_file.close()
    if "command not found" in open("response.txt").readline():
        print_warning("%s *NOT* installed." % utility_name)
        unlink("response.txt")
        return False
    else:
        print_msg("%s installed." % utility_name)
        unlink("response.txt")
        return True


def check_module(module_name):
    """
        Try to import "module_name", then echo messages.
    """
    try:
        __import__(module_name)
        print_msg("python %s module installed." % module_name)
        return True
    except NameError:
        print_warning("python %s module *NOT* installed." % module_name)
        return False


def check_environment():
    """
        Check if the required compiler and running environment are complete.
        Return True if the environment is complete, otherwise return False.
    """
    final_msgs = []

    print("Start checking...")
    print("-" * 80)

    # check g++ and icpc
    if not check_command("g++") and not check_command("icpc"):
        final_msgs.append("You need to install icpc or g++.")

    # check gfortran and ifort
    if not check_command("gfortran") and not check_command("ifort"):
        final_msgs.append("You need to install ifort or gfortran.")

    # check make utility
    if not check_command("make"):
        final_msgs.append("You need to install the make utility.")

    # check gsl
    if not check_command("gsl-config", "gsl"):
        final_msgs.append("You need to install gsl library.")

    # check zip and unzip
    if not check_command("zip --help", "zip") or not check_command(
            "unzip --help", "unzip"):
        final_msgs.append("You need both zip and unzip utilities.")

    # check numpy
    if not check_module("numpy"):
        final_msgs.append("You need to install python numpy package.")

    # check hdf5 library
    if not check_command("h5fc") or not check_command("h5c++"):
        final_msgs.append("You need to install hdf5 library.")

    # check matplotlib
    if not check_module("pylab"):
        print_warning("You need to install python matplotlib package to "
                      "automatically generating plots compared to "
                      "experimental data.")

    # print final messages
    print("-" * 80)
    if not final_msgs:
        print("All essential packages installed. Test passed.")
        return True
    else:
        for msg in final_msgs:
            print(msg)
            if 'hdf5' in msg:
                choice = raw_input("Do you want to install hdf5 now? ")
                if choice.lower() in ['y', 'yes']:
                    Popen('./localintall_hdf5.py', shell=True,
                          cwd=path.abspath('./hdf5_support'))
        return False


def greetings(selection):
    if selection == 1:
        print(r"""
          _______ _________ _        _______
|\     /|(  ____ \\__   __/( (    /|/ ___   )
| )   ( || (    \/   ) (   |  \  ( |\/   )  |
| (___) || (__       | |   |   \ | |    /   )
|  ___  ||  __)      | |   | (\ \) |   /   /
| (   ) || (         | |   | | \   |  /   /
| )   ( || (____/\___) (___| )  \  | /   (_/\
|/     \|(_______/\_______/|/    )_)(_______/

 _______  _______  _______           _______
(  ____ \(  ____ )(  ___  )|\     /|(  ____ )
| (    \/| (    )|| (   ) || )   ( || (    )|
| |      | (____)|| |   | || |   | || (____)|
| | ____ |     __)| |   | || |   | ||  _____)
| | \_  )| (\ (   | |   | || |   | || (
| (___) || ) \ \__| (___) || (___) || )
(_______)|/   \__/(_______)(_______)|/

        """)
    elif selection == 2:
        print(r"""
         _       _    _             _          _                _
        / /\    / /\ /\ \          /\ \       /\ \     _      /\ \
       / / /   / / //  \ \         \ \ \     /  \ \   /\_\   /  \ \
      / /_/   / / // /\ \ \        /\ \_\   / /\ \ \_/ / /__/ /\ \ \
     / /\ \__/ / // / /\ \_\      / /\/_/  / / /\ \___/ //___/ /\ \ \
    / /\ \___\/ // /_/_ \/_/     / / /    / / /  \/____/ \___\/ / / /
   / / /\/___/ // /____/\       / / /    / / /    / / /        / / /
  / / /   / / // /\____\/      / / /    / / /    / / /        / / /    _
 / / /   / / // / /______  ___/ / /__  / / /    / / /         \ \ \__/\_\
/ / /   / / // / /_______\/\__\/_/___\/ / /    / / /           \ \___\/ /
\/_/    \/_/ \/__________/\/_________/\/_/     \/_/             \/___/_/
         _              _           _      _                  _
        /\ \           /\ \        /\ \   /\_\               /\ \
       /  \ \         /  \ \      /  \ \ / / /         _    /  \ \
      / /\ \_\       / /\ \ \    / /\ \ \\ \ \__      /\_\ / /\ \ \
     / / /\/_/      / / /\ \_\  / / /\ \ \\ \___\    / / // / /\ \_\
    / / / ______   / / /_/ / / / / /  \ \_\\__  /   / / // / /_/ / /
   / / / /\_____\ / / /__\/ / / / /   / / // / /   / / // / /__\/ /
  / / /  \/____ // / /_____/ / / /   / / // / /   / / // / /_____/
 / / /_____/ / // / /\ \ \  / / /___/ / // / /___/ / // / /
/ / /______\/ // / /  \ \ \/ / /____\/ // / /____\/ // / /
\/___________/ \/_/    \_\/\/_________/ \/_________/ \/_/

        """)
    elif selection == 3:
        print(r"""


   .              __.....__     .--.   _..._
 .'|          .-''         '.   |__| .'     '.
<  |         /     .-''"'-.  `. .--..   .-.   .
 | |        /     /________\   \|  ||  '   '  |
 | | .'''-. |                  ||  ||  |   |  |.--------.
 | |/.'''. \\    .-------------'|  ||  |   |  ||____    |
 |  /    | | \    '-.____...---.|  ||  |   |  |    /   /
 | |     | |  `.             .' |__||  |   |  |  .'   /
 | |     | |    `''-...... -'       |  |   |  | /    /___
 | '.    | '.         .-'''-.       |  |   |  ||         |
 '---'   '---'       '   _    \     '--'   '--'|_________|
                   /   /` '.   \       _________   _...._
  .--./)          .   |     \  '       \        |.'      '-.
 /.''\\   .-,.--. |   '      |  '       \        .'```'.    '.
| |  | |  |  .-. |\    \     / /         \      |       \     \
 \`-' /   | |  | | `.   ` ..' /_    _     |     |        |    |
 /("'`    | |  | |    '-...-'`| '  / |    |      \      /    .
 \ '---.  | |  '-            .' | .' |    |     |\`'-.-'   .'
  /'""'.\ | |                /  | /  |    |     | '-....-'`
 ||     ||| |               |   `'.  |   .'     '.
 \'. __// |_|               '   .'|  '/'-----------'
  `'---'                     `-'  `--'
        """)


if __name__ == '__main__':
    greetings(2)
    check_environment()
