from .formatter import FormatterBase
from request_internal import run_oauth_flow
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import inquirer
import pandas as pd


class GoogleSheetsFormatter(FormatterBase):
    def configure(self, interface, source_filename, seed):
        def assign_variables(user_settings):
            self.source_filename = source_filename
            self.credentials = run_oauth_flow()
            self.sheet_id = user_settings["google_sheets_id"]
            self.sheet_range = user_settings["sheet_range"]

        interface\
            .get_input(
                "google_sheets_id",
                "Entered the id for the Google Sheet you want to export to",
                "",
                True
            )\
            .get_input(
                "sheet_range",
                "Enter the range of the sheet you want to export to",
                "A1",
                True
            )\
            .queue_handler(assign_variables)

    def export(self):
        self.look_for_new_data()
        export_data = self.new_data_two_dimensional_array()

        if len(export_data) == 0:
            should_continue = inquirer.confirm("No new data found. Do you want to export all data?", default=False)
            if should_continue == False:
                return
            export_data = pd.read_csv(self.source_filename).fillna("").values.tolist()

        try:
            service = build('sheets', 'v4', credentials=self.credentials)
            sheet = service.spreadsheets()
            result = sheet.values().append(
                spreadsheetId=self.sheet_id,
                range=self.sheet_range,
                valueInputOption="USER_ENTERED",
                body=dict(
                    majorDimension="ROWS",
                    values=export_data
                )
            ).execute()
        except HttpError as e:
            print(e)

    def get_id_from_url(self, url):
        # Use a regular expression to extract the part of the link that
        # contains the sheet ID. The regular expression looks for the
        # "spreadsheets/d/" part of the link, followed by some characters
        # that represent the sheet ID, followed by a "/".
        matches = re.search(r'spreadsheets/d/([^/]+)', link)
        if matches is None:
            # If the regular expression didn't match, return None.
            return None
        # Return the sheet ID, which is the first match group of the regular
        # expression.
        return matches.group(1)

    def new_data_two_dimensional_array(self):
        if len(self.new_data) == 0:
            return []
        return [[row[key] for key in row] for row in self.new_data]
