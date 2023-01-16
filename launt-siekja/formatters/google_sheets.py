from .formatter import FormatterBase
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import inquirer
import pandas as pd
from .google_sheets_api import GS_API
from thefuzz import process, fuzz


class GoogleSheetsFormatter(FormatterBase):
    def configure(self, interface, source_filename, seed):
        def assign_variables(user_settings):
            self.source_filename = source_filename
            self.api = GS_API(spreadsheet_id=user_settings["google_sheets_id"])
            self.sheet_name = user_settings["sheet_name"]

        interface\
            .get_input(
                "google_sheets_id",
                "Entered the id for the Google Sheet you want to export to",
                "",
                True
            )\
            .get_input(
                "sheet_name",
                "Enter the name of the sheet you want to export to",
                "Sheet",
                True
            )\
            .queue_handler(assign_variables)

    def export(self):
        self.look_for_new_data()

        if isinstance(self.new_data, list) and len(self.new_data) == 0:
            should_continue = inquirer.confirm(
                "No new data found. Do you want to export all data?", default=False)
            if should_continue == False:
                return
            self.new_data = pd.read_csv(self.source_filename)

        try:
            sheet_header_row = self.api.get_header_row(self.sheet_name)
            csv_header_row = list(self.new_data.columns)

            def run_in_case_csv_is_short(diff):
                for item in diff:
                    self.new_data[item] = ""

            def run_in_case_sheet_is_short(diff):
                raise RuntimeError(
                    """The google sheet you are trying to append to is missing these columns:
                    {diff}
                    I will fix this in the future.""".format(diff))

            if len(sheet_header_row) != len(csv_header_row):
                resolve_mismatched_datasets(
                    header_row1=csv_header_row,
                    header_row2=sheet_header_row,
                    run_in_case_row1_is_short=run_in_case_csv_is_short,
                    run_in_case_row2_is_short=run_in_case_sheet_is_short)
                csv_header_row = list(self.new_data.columns)


            if compare_header_rows(csv_header_row, sheet_header_row):
                self.api.append_to_sheet(
                    self.sheet_name,
                    self.new_data.fillna("").values.tolist())
            elif compare_header_rows_unordered(csv_header_row, sheet_header_row):
                self.new_data = self.new_data[align_list(sheet_header_row, csv_header_row)]
                self.api.append_to_sheet(
                    self.sheet_name,
                    self.new_data.fillna("").values.tolist())
            else:
                print("Could not match up header rows.")
                return
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


def compare_header_rows(row1, row2, threshold=55):
    for item1, item2 in zip(row1, row2):
        if fuzz.partial_ratio(item1.lower(), item2.lower()) < threshold:
            return False

    return True


def compare_header_rows_unordered(row1, row2):
    return compare_header_rows(sorted([x.lower() for x in row1]), sorted([x.lower() for x in row2]))


def build_index_finder(ref):
    def find_index(word):
        if word in ref:
            return ref.index(word)
        else:
            result = process.extractOne(word, ref)
            return ref.index(result[0])

    return find_index


def align_list(ref, target):
    return sorted(target, key=build_index_finder(ref))


def find_row_difference(row1, row2):
    if len(row1) < len(row2):
        shorter = row1
        longer = row2
        action = "row1 is short"
    else:
        shorter = row2
        longer = row1
        action = "row2 is short"

    diff = set([x.lower() for x in longer]).difference(
        [x.lower() for x in shorter])
    find_index = build_index_finder(longer)

    return (
        [longer[find_index(item)] for item in diff],
        action
    )


def resolve_mismatched_datasets(
    header_row1,
    header_row2,
    run_in_case_row1_is_short,
    run_in_case_row2_is_short
):
    diff, action = find_row_difference(header_row1, header_row2)
    if action == "row1 is short":
        return run_in_case_row1_is_short(diff)
    else:
        return run_in_case_row2_is_short(diff)
