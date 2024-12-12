# cbb-tracker

Tracks the wins of college basketball teams. I am in a league where everyone picks 10 college basketball teams at the beginning of the year. At the end of the season, whoever's 10 teams have the most combined wins takes home the trophy. I made this program to send myself a daily email detailing the results for my teams from the day before so I do not constantly have to check google for their scores individually. It also keeps track of each team's individual record and my teams collective record as a whole for the season.

## Prerequisites

- Python
- Access to a Google/Gmail account

## Getting Started

### Cloning the Repository

First, clone the repository to your local machine:

```sh
git clone https://github.com/yourusername/cbb-tracker.git
cd cbb-tracker
```

### Making a Virtual Environment

Creating a virtual environment to manage dependencies:

```sh
python -m venv .env
source .env/bin/activate  # On Windows use `.env\Scripts\activate`
```

### Installing Requirements

Install the required packages to your virtual environment

```sh
pip install -r requirements.txt
```

### Making an SportsDataIO Account and Getting a Free API Key

1. Go to sportsdata.io
2. Sign up for a free account
3. Click the `API Free Trial` button on the home page
4. Select the `SportsDataIO API Free Trial` option
5. Select `CBB` for the "Product" option
6. Fill in the rest of the form with your information
7. Once you have received your free trial, click the `Account` button at the top of the page
8. Your API Key should be printed on the screen

### Getting a Google App Password

Follow these directions to create an app password for your Google account: https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237

### Setting Configuration Values

Set the values in the `config.py` file to work for your specific use case:
- `API_KEY` - Your SportsDataIO API Key
- `FROM_EMAIL` - The email that will be sending your reports (this should be the email associated with your Google account. It must be a Gmail account.)
- `FROM_PASSWORD` - The App Password created for your Google account associated with the `FROM_EMAIL`
- `TO_EMAIL` - The email you want to send the report to (can be any email service, doesn't have to be Gmail.)
- `TEAMS` - An array of the team keys for the teams you want to track and include in your report
    - Examples:
        - Syracuse -> `"SYRA"`
        - Kennesaw State -> `"KENEST"`
        - Maryland -> `"MARY"`
    - A full list of team keys can be accessed by sending a GET request to this endpoint: https://api.sportsdata.io/v3/cbb/scores/json/teams?key={YOUR_API_KEY}
        - This will return a list of all the game objects from the API
        - Each team object will have a `"KEY"` attribute that holds the team's key

Example of a filled out `config.py` file:

```python
config = {
    'API_KEY': 'abc123def456ghi789',
    'FROM_EMAIL': 'johndoe@gmail.com',
    'FROM_PASSWORD': 'abcd efgh ijkl mnop',
    'TO_EMAIL': 'janedoe@gmail.com',
    'TEAMS': ['SYRA', 'KENEST', 'MARY']
}
```

## Execution

To actually run the program and get the results, generate the report, and send out the report email, run the following command:

```python
python main.py
```

Here is an example of what your report should look like:

```
DAILY CBB REPORT: 12/10/2024
----------------------------
Yesterday's Record: 3-0
Season Record: 58-31

Yesterday's Results:
PRNCE 39 - 37 MONM (W)
UMKC 38 - 36 PORT (W)
ARLR 44 - 32 OCHT (W)

Updated Team Records:
Princeton: 8-4
Washington State: 8-2
Connecticut: 7-3
Arkansas State: 7-3
Little Rock: 6-4
BYU: 6-2
Grand Canyon: 6-2
McNeese State: 5-4
Kansas City: 5-7
```