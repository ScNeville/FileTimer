import pathlib
from datetime import date, datetime
import os
import shutil

folder_root = "E:\Movies" # Change the path to the folder you want to delete
days_until_delete = 183 # Change the timer to the amount of days you want to wait before deleting
files_in_folder = []
inBackground = False;
files_deleted = 0


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
    try:
        for item in os.listdir(folder):
            files_in_folder.append(item)
    except FileNotFoundError:
        print("-> NOT FOUND")
    except:
        print("-> UNKNOWN ERROR")

def read_files():
    for file in files_in_folder:
        path = pathlib.Path().joinpath(folder_root, file)
        date = get_modified_time(path)
        canDelete = compare_dates(date)
        if canDelete:
            delete_file(path)
    print(f"******* FINISHED PROCESSING, DELETED {files_deleted} *******")

def compare_dates(dates):
    date1 = date(dates.year, dates.month, dates.day)
    date2 = get_todays_date()
    date2 = date(date2.year, date2.month, date2.day)
    delta = date2 - date1
    if delta.days > days_until_delete:
        return True
    else:
        return False

def delete_file(file):
    try:
        if inBackground:
            shutil.rmtree(file, ignore_errors= False)
            files_deleted += 1
            print(f"-> DELETED {file}")
        else:
            confirmation = input(f"Confirm Deletion of {file}")
            confirmation = confirmation.lower()
            if confirmation == "yes" or "y":
                shutil.rmtree(file, ignore_errors= False)
                files_deleted += 1
                print(f"-> DELETED {file}")
            elif confirmation == "no" or "n":
                print(f"Skipped {file}")
    except Exception as e:
        print(f"ERROR DELETING {file} - {e}")

def main():
    files_deleted = 0
    load_folder(folder_root)
    if len(files_in_folder) == 0:
        print("-> FOLDER IS EMPTY")
        return
    else:
        print(f"-> FOUND {len(files_in_folder)} FILES")
    read_files()

if __name__ == "__main__":
    main()
