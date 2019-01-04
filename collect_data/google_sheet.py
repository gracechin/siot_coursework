# pip install gspread oauth2client
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
def enter_twitter(row):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    twitter_sheet = client.open("SIOT data collection").sheet1
    index = 2
    twitter_sheet.insert_row(row, index)

def enter_pollution(row):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    pollution_sheet = client.open("SIOT data collection").worksheet("pollution")
    index = 3
    pollution_sheet.insert_row(row, index)


if __name__== "__main__":
    enter_twitter(["hello", "please", "work"])
    enter_pollution(["hello", "please", "work"])