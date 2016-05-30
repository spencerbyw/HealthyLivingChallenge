import calculators as calc
import csv
import datetime
import ranking
import settings
import urllib2


def assemble_score_dict():
    score_dict = {'scores': {}}
    rows = fetch_drive_csv(settings.CSV_LOCATION)
    # USING LOCAL DATA
    # rows = []
    # with open('../hlc_data.csv', 'rd') as hlc_data:
    #     rdr = csv.reader(hlc_data, delimiter=',')
    #     for row in rdr:
    #         rows.append(row)

    rows_by_people = csv_to_data_dict(rows)
    # We now have a legible list of scores to send to the calculator.
    for person in rows_by_people.iteritems():
        score_dict['scores'][person[0]] = {'scores_by_date': {}}
        for date_list in person[1].iteritems():
            day_score = calculate_single(date_list[1][-1])
            score_dict['scores'][person[0]]['scores_by_date'][date_list[0]] = \
                day_score
        day_score_pairs = score_dict['scores'][person[0]]['scores_by_date'].iteritems()
        all_scores = [pair[1] for pair in day_score_pairs]
        score_dict['scores'][person[0]]['total_score'] = sum(all_scores)

    score_dict = _add_rankings(score_dict)
    return score_dict


def fetch_drive_csv(url):
    response = urllib2.urlopen(url)
    rows = csv.reader(response)
    return list(rows)


def csv_to_data_dict(rows):
    # Process header row
    rows.reverse()
    header_row = rows.pop()
    rows.reverse()
    # Process the rest of the rows
    clean_rows = [row for row in rows if _valid_date(row[0])]

    rows_by_people = {}
    for row in clean_rows:
        full_date = row[0]
        name = row[1]
        if rows_by_people.has_key(name):
            # print '0: {}, 1: {}'.format(full_date, name)
            if rows_by_people[name].has_key(full_date.split(' ')[0]):
                rows_by_people[name][full_date.split(' ')[0]].append(row)
            else:
                rows_by_people[name][full_date.split(' ')[0]] = [row]
        else:
            # print '0: {}, 1: {}'.format(full_date, name)
            rows_by_people[name] = {full_date.split(' ')[0]: [row]}

    return rows_by_people


def _valid_date(date):
    # Parse datetime from date
    # 5/23/2016 22:11:57
    if date:
        date_obj = datetime.datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
        print date_obj
        if date_obj > settings.COMP_START_DATE and \
            date_obj < settings.COMP_END_DATE:
            return True
        return False
    return False


def calculate_single(data_arr):
    big_six = calc.big_six(data_arr[2:5])
    single_points = calc.single_points(data_arr[5])
    bonus_points = calc.bonus_points(data_arr[6])
    accountability = calc.accountability(data_arr[7:])
    return sum([big_six, single_points, bonus_points, accountability])


def _add_rankings(score_dict):
    # Assemble a USER: TOTAL_SCORE dict
    user_score_pairs = [(user[0], user[1]['total_score']) for user in score_dict['scores'].iteritems()]
    user_score_pairs.sort(key=lambda x: x[1], reverse=True)
    rankings = list(ranking.Ranking(user_score_pairs, start=1, key=lambda x: x[1]))
    for rank in rankings:
        score_dict['scores'][rank[1][0]]['ranking'] = rank[0]
    return score_dict


def ordinal(n):
    return "%s" % ("tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])


def build_display_data():
    scores = assemble_score_dict()
    scores_arr = [person for person in scores['scores'].iteritems()]
    for person in scores_arr:
        person[1]['ordinal'] = \
            ordinal(person[1]['ranking'])
    scores_arr.sort(key=lambda x: x[1]['ranking'])
    year = datetime.datetime.now().year
    return year, scores_arr
