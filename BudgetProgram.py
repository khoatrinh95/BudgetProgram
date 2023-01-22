from Helpers import Prompts
import constants
import MainProgram

# Greetings
Prompts.greeting()

# User input
run = True
while run:
    droppedFile = Prompts.prompt_for_file()
    constants.BANKING_CSV_PATH = droppedFile.strip()

    year = Prompts.prompt_for_year()
    constants.YEAR = int(year.strip())

    month = Prompts.prompt_for_month()
    constants.MONTH = month

    Prompts.prompt_ok()

    MainProgram.main_program()

    run = Prompts.prompt_after_run()

# Close program
Prompts.end()