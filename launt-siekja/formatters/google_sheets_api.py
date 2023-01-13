from googleapiclient.discovery import build

def get_sheets_list(spreadsheet_id, credentials):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.get(spreadsheetId=spreadsheet_id).execute()
    sheets = result.get('sheets', '')
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

def get_header_row(spreadsheet_id, sheet_name, credentials):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_id}!1:1"
    ).execute()
    values = result.get('values', [])
    if len(values) > 0:
        return values[0]
    else:
        return []

def append_to_sheet(spreadsheet_id, sheet_name, credentials, values):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="USER_ENTERED",
        body= {
            "majorDimension": "ROWS",
            "values": values
        }
    ).execute()
