from googleapiclient.discovery import build
from .oauth import run_oauth_flow

class GS_API:
    def __init__(self, spreadsheet_id):
        self.credentials = run_oauth_flow()
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.spreadsheet_id = spreadsheet_id

    def get_sheets_list(self):
        result = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        sheets = result.get('sheets', [])
        return sheets

    # [{'properties': {'sheetId': 1395442271,
    #    'title': "Thiessen's Properties",
    #    'index': 0,
    #    'sheetType': 'GRID',
    #    'gridProperties': {'rowCount': 1000, 'columnCount': 26}}},
    #  {'properties': {'sheetId': 1814342492,
    #    'title': 'Sheet4',
    #    'index': 1,
    #    'sheetType': 'GRID',
    #    'gridProperties': {'rowCount': 999, 'columnCount': 27}}},
    #  {'properties': {'sheetId': 194745247,
    #    'title': 'Sheet6',
    #    'index': 2,
    #    'sheetType': 'GRID',
    #    'gridProperties': {'rowCount': 1000, 'columnCount': 26}}},
    #  {'properties': {'sheetId': 1170358251,
    #    'title': 'Horizon Listings',
    #    'index': 3,
    #    'sheetType': 'GRID',
    #    'gridProperties': {'rowCount': 1000, 'columnCount': 20}}},
    #  {'properties': {'sheetId': 503445267,
    #    'title': 'internal_data',
    #    'index': 4,
    #    'sheetType': 'GRID',
    #    'gridProperties': {'rowCount': 1000, 'columnCount': 26}}}]


    def get_header_row(self, sheet_name):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet_name}!1:1"
        ).execute()
        values = result.get('values', [])
        if len(values) > 0:
            return values[0]
        else:
            return []


    def append_to_sheet(self, sheet_name, values):
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="USER_ENTERED",
            body={
                "majorDimension": "ROWS",
                "values": values
            }
        ).execute()
