import csv


project_name_bindings = {
    'OCP': 'RGSB-66',
    '#': 'RGSB-66',
    'OTP': 'OTP-4791'
}
timesheet_rows = []
date_row = []
result_csv_rows = []


def read_hubstaff_timesheet(path):
    with open(path) as file:
        rows_timesheet = csv.reader(file, delimiter=',')

        for row in rows_timesheet:
            if 'Member' in row:
                del row[0:4]
                row.pop(-1)
                print(row)
                date_row.extend(row)
                continue

            del row[0:4]
            row.pop(-1)
            print(row)
            timesheet_rows.append(row)


def convert_time(time: str):
    time_list = time.split(':')
    hours = int(time_list[0])
    minutes = int(time_list[1])
    seconds = int(time_list[2])

    if hours == 0 and minutes == 0:
        return ''

    result_time = ''

    if seconds > 30:
        minutes += 1

    if minutes >= 60:
        hours += 1
        minutes = 0

    if hours != 0:
        result_time = str(hours) + 'h'

    if minutes != 0:
        if hours != 0:
            result_time += ' ' + str(minutes) + 'm'
        else:
            result_time += str(minutes) + 'm'

    return result_time


def transform_rows():
    for timesheet_row in timesheet_rows:

        issue_name = timesheet_row[0].split(' ', 1)[0]
        issue_name_prefix = issue_name.split('-', 1)[0]

        for key, value in project_name_bindings.items():
            if key in issue_name_prefix:
                issue_name = value

        for (i, date) in enumerate(date_row):
            if i == 0:
                continue

            time = convert_time(timesheet_row[i])
            if time == '':
                continue

            result_row = [issue_name, date, time, timesheet_row[0]]
            result_csv_rows.append(result_row)

    print()
    for i in result_csv_rows:
        print(i)


def write_jira_csv(path):
    new_path = path.replace('.csv', '_new.csv', 1)
    with open(new_path, 'w') as jira_csv:
        writer = csv.writer(jira_csv, delimiter=',')
        writer.writerows(result_csv_rows)
        print()
        print('write success!')


if __name__ == '__main__':
    path_to_file = "/home/stayer/downloads/sergey bogdanov_timesheet_report_2021-06-28_to_2021-07-04.csv"
    read_hubstaff_timesheet(path_to_file)
    transform_rows()
    write_jira_csv(path_to_file)
