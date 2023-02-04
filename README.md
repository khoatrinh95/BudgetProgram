![banner-budget](https://user-images.githubusercontent.com/59627012/216791975-3865fe09-55ee-4532-8e94-b9db218d9ff5.png)




## Overview
Is tracking expenses a monotonous task that you dread doing every month? You want to know how much you spend on eating out but you hate going through all the transactions on your banking statement? 

This python program automates that task and categorizes your expenses. It aggregates them by category, compares them to your budget and highlights any category where you overspend.

The goal is to automate the repetitive and time-consuming task so that you’ll have more time to focus on the other areas of your budgeting.

### Security
Unlike other budgeting apps, this program only uses your banking statements and runs locally on your computer. It does not have access to your bank account or communicate with an outside server. In short, the information stays inside your computer.


## Key Features

* Categorize expenses based on pre-determined word association
    - You decide how the program categorizes your expenses.
* Provide an overview of spending and indicate overspending
* Allow personalization in terms of budgets for each category



## Instructions
### Prerequisites
* Have Python installed on your computer

### Installation
* Download the [zip](https://drive.google.com/file/d/1VtKbPxz59oHonwtxGh31ATK15H2AnBPu/view?usp=share_link) file
* Unzip it. There should be several files in the unzipped folder. The notable files/folders to pay attention to:
    - ___BudgetProgram.py___: the main program
    - ___profiles___
        - ___budget.json___: This file contains your budget in the format of _"category" : amount_.
        - ___words.json___: This file contains the words that are associated to each category in the format of _"category" : ["word1", "word2", ...]_. When the program sees an expense, if if recognizes any word that matches the information in this file, it will categorize that expense accordingly.
    - ___output___: The result Excel sheet will reside in this folder.


### How To Use
1. Download RBC statement in csv format
2.  Create your budget
    - In your unzipped folder, navigate to folder _profiles_
    - Open folder _profile1_
    - Open _budget.json_ with a TextEditor.  You can add/remove category, change amount by modifying this json file. Eventually, the json file should look something like this:
    ```json
    {
    "rent": 1800,
    "hydro": 80,
    "internet": 50,
    "phone": 80,
    "transport": 100,
    "grocery": 500,
    "gym": 50,
    "food": 300,
    "shopping": 300,
    "activity": 100,
    "loan": 120
    }
    ```
3. Add word association
    - Open _words.json_ with a TextEditor.  You can add/remove category as well as words in each category. Eventually, the json file should look something like this:
    ```json
    {
    "transport":[
        "gare",
        "bixi",
        "stm",
        "uber",
        "essence",
        "gas station",
        "ultramar",
        "shell",
        "petro",
        "esso"
    ],
    "phone":[
        "telus",
        "fizz",
        "fido",
        "rogers",
        "koodo"
    ],
    "shopping":[
        "amazon",
        "apple",
        "zara",
        "sports experts",
        "decathlon",
        "pharmaprix",
        "jean coutu"
    ],
    "food":[
        "tim hortons",
        "presotea",
        "subway",
        "cafe",
        "starbucks",
        "shawarmaz",
        "nouilles",
        "noodles",
        "patisserie",
        "poke",
        "sushi",
        "hotpot",
        "sandwich",
        "pho",
        "cuisine",
        "mcdonald"
    ],
    "grocery":[
        "adonis",
        "iga",
        "metro",
        "maxi"
    ],
    "ignore":[
        "investment",
        "find & save"
    ]
    }
    ``` 


    __Note__: 
    - Check your spelling: These 2 json files work together. Therefore, it is important that you make sure the categories in both json files are written the same way, otherwise the program won't be able to link them properly.
    - in _words.json_, the category _"ignore"_ is a special category. It is reserved for expenses that you would like to ignore aka not visible in the result. In the example above, any expense that has the word "investment" or "find & save" will be removed from the result.

4. Run the BudgetProgram.py by double-clicking on it.
5. When prompted, drop your bank statement in the window, then press Enter.
6. Follow prompt to enter the year and month for which you would like to analyze.
7. If all is correct, the program should run successfully and you will see this message: _"Analysis complete. The Excel sheet is saved in the following folder: ..."_
8. Navigate to the mentioned folder, and voilà, the result is inside the file _BUDGET.xlsx_
9. Open the file _BUDGET.xlsx_, for every month that you choose to analyze, there will be a sheet generated for it. For example, if you enter 2022 and 11 (or November) when prompted for year and date at the beginning of the program, now the Excel file should contain a sheet named _"2022-11"_
10. Note that the program can't process all 100% transactions. You can now go through the remaining unprocessed expenses to categorize them. The result will be reflected in real time in the Summary table at the bottom of the sheet.


## Limitations
- For now, this program only works with csv bank statements from RBC (Royal Bank of Canada). However, enhancements are being planned so it can work with any type of bank statements.
- The program can’t analyze all transactions. It will attempt to categorize as many transactions as possible (transactions with words that it recognizes)
- Users must be familiar with JSON
- The program has only been tested on MacOS M1 machines. I am aware that there could be issues when runnning on other OS systems. However, this will be fixed in future versions.

## Future enhancements
- Improve program to work with any bank statement
- Develop CLI to let users modify budget (instead of modifying directly JSON files)
- Develop a logging system
- Integrate AI to learn from user's manual categorization and apply to future processing

## Technical principles in this project
1. helpers: separation of concerns
2. Scalable and reusable 
3. Maintainability
    1. Low coupling: Helpers are independent → changes in one won’t affect the other
    2. High cohesion: designated helpers for different functionalities
4. backup system
5. logging system


## Credits
- Openpyxl
- [@JCLaHoot](https://github.com/JCLaHoot)for designing the beautiful banner

## Troubleshooting
If you encounter error: _"BudgetProgram.py cannot be opened because the developer cannot be verified."_
- By default, macOS allows users to install only approved apps from developers registered with Apple that have verified their apps for use on Macs.
- To resolve this error, you must disable GateKeeper of macOS
- In the Terminal, type the following command and press Enter:
    ```bash
    sudo spctl --master-disable
    ```


