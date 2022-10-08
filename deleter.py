from datetime import date, datetime
import os
import pathlib
import sched
import shutil
from time import gmtime, sleep, strftime

days_until_delete = 183
files_deleted = 0
time_interval = 0
root_folder = ""
files_in_folder = []

#Get todays date
def get_todays_date():
    today = date.today()
    return (today)
#get date of the folder
def get_modified_time(folder):
    time = pathlib.Path(folder).stat().st_mtime
    time = datetime.fromtimestamp(time).date()
    return (time)

def load_folder(folder):
    if pathlib.Path(folder).exists():
        try:
            for item in os.listdir(folder):
                files_in_folder.append(item)
        except FileNotFoundError:
            print("=> NOT FOUND")
            return
        except:
            print("=> UNKNOWN ERROR")
            return
    else:
        print("=> FOLDER NOT FOUND")
        return

def scan_files(time_threshold):
    print(f"\n=> FOUND {len(files_in_folder)} FILES")
    for file in files_in_folder:
        path = pathlib.Path().joinpath(root_folder, file)
        date = get_modified_time(path)
        canDelete = compare_dates(date, time_threshold)
        if canDelete:
            delete_file(path)
    print(f"=> FINISHED PROCESSING, DELETED {files_deleted}")

def compare_dates(dates, time_threshold):
    date1 = date(dates.year, dates.month, dates.day)
    date2 = get_todays_date()
    date2 = date(date2.year, date2.month, date2.day)
    delta = date2 - date1
    if delta.days > time_threshold:
        return True
    else:
        return False

def delete_file(file):
    try:
        if inBackground:
            shutil.rmtree(file, ignore_errors= False)
            files_deleted += 1
            print(f"=> DELETED {file}")
        else:
            confirmation = input(f"=> Confirm Deletion of {file}")
            confirmation = confirmation.lower()
            if confirmation == "yes" or "y":
                shutil.rmtree(file)
                files_deleted += 1
                print(f"=> DELETED {file}")
            elif confirmation == "no" or "n":
                print(f"=> SKIPPED {file}")
    except Exception as e:
        print(f"=> ERROR DELETING {file} - {e}")

def handle_timer(time_to_wait, time_threshold):
    time_elapsed = 0
    while time_elapsed != time_to_wait:
            countdown = strftime("%H:%M:%S", gmtime(time_to_wait - 1 - time_elapsed))
            time_elapsed += 1
            print(f"=> Time until next scan {countdown}", end="\r")
            sleep(1)
            if time_elapsed == time_to_wait:
                time_elapsed = 0
                files_in_folder.clear()
                load_folder(root_folder)
                scan_files(time_threshold)


def main():
    global root_folder
    time_interval = None
    time_threshold = None
    while True:
        root_folder = input("=> ENTER DIRECTORY TO WATCH: ")
        break
    load_folder(root_folder)
    while True:
        time_threshold = input("=> HOW MANY DAYS UNTIL FILE IS TO BE DELETED?: ")
        if time_threshold.isdigit():
            time_threshold = int(time_threshold)
            break
    if len(files_in_folder) == 0:
        answer = input("=> FOLDER IS EMPTY, DO YOU WISH TO WATCH THIS FOLDER? Y/N: ").strip().upper()
        if answer in ['Y', 'YES']:
                while True:
                    time_interval = input("=> HOW OFTEN WOULD YOU LIKE TO SCAN THE FOLDER? (ANSWER IN SECONDS): ")
                    if time_interval.isdigit():
                        time_interval = int(time_interval)
                        scan_files(time_threshold)
                        sleep(1)
                        handle_timer(time_interval, time_threshold)
                        break
        else:
            return
    else:
        while True:
            schedule_run = input("=> WOULD YOU LIKE TO SCHEDULE THIS SCRIPT? Y/N: ").strip().upper()
            if schedule_run in ['Y', 'YES']:
                    while True:
                        time_interval = input("=> HOW OFTEN WOULD YOU LIKE TO SCAN THE FOLDER? (ANSWER IN SECONDS): ")
                        if time_interval.isdigit():
                            time_interval = int(time_interval)
                            scan_files(time_threshold)
                            sleep(1)
                            handle_timer(time_interval, time_threshold)
                            break
            elif schedule_run in ['N', 'NO']:
                scan_files(time_threshold)
                quit = input()
                break

if __name__ == "__main__":
    main()
    
