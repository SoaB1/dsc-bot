import os
import dotenv
from dotenv import load_dotenv
load_dotenv('../.env')

# Load a Library for google sheets
from hashlib import new
from google.oauth2.service_account import Credentials
import gspread

# Google Sheets API Scopes
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

async def getTicketNumber():
    # Load the credentials from the JSON file
    credentials = Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=scopes
    )

    # Authorize the credentials and create a client
    gc = gspread.authorize(credentials)

    # Open the spreadsheet by the URL
    spreadsheet_url = os.environ['SHEET_URL']
    spreadsheet = gc.open_by_url(spreadsheet_url)
    # Open the worksheet by the name
    ticketList = spreadsheet.worksheet('tickets')
    # Get the last row of the worksheet
    lastTicketRow = len(ticketList.get_all_values())
    # Get the last ticket number
    newTicketNumber = int(ticketList.cell(lastTicketRow, 1).value) + 1

    # Return the new ticket number
    return str(newTicketNumber).zfill(5)