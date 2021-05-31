import csv
import settings
import urllib2

from lib.utils import fetch_drive_csv, assemble_score_dict
from flask import jsonify

def get_user_data():
    row_dict = {'rows': []}
    rows = fetch_drive_csv(settings.CSV_LOCATION)
    for row in rows:
        row_dict['rows'].append(row)

    return jsonify(assemble_score_dict())
