# Autoplusnik Copyright (C) 2023 Igor Samsonov

import gspread as gp
import pandas as pd

def load_to_sheet(page: gp.Worksheet, path_to_data: str):
    data = pd.read_csv(path_to_data, error_bad_lines=False)
    data = data.fillna(' ')

    page.update([len(data.columns.values.tolist()) * ['', ]] * 70)
    page.update([data.columns.values.tolist()] + data.values.tolist())

def get_worksheet(sheet_name, worksheet_name, auth):
    info_plusnik = auth.open(sheet_name)
    return info_plusnik.worksheet(worksheet_name)