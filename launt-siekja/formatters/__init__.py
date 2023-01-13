from .formatter import FormatterBase
from .csv_formatter import CSVFormatter
from .google_sheets import GoogleSheetsFormatter

FORMATTERS = {
    "CSV": CSVFormatter,
    "Google Sheets": GoogleSheetsFormatter
}
