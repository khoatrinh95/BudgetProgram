



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


