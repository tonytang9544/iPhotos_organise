import os, datetime, sys
import tkinter.filedialog as tkfd

def trial():
    filename = "/Users/tony/Documents/E/照片/20240127婚礼/originals/JYF_4662.CR2"
    supported_formats = (".png", ".jpeg", ".jpg", ".cr2", ".heic", ".mov", ".mp4")
    folder = "/Users/tony/Documents/E/照片/Photos Library.photoslibrary/originals"

    datetime_obj = datetime.datetime.fromtimestamp(os.path.getmtime(filename), tz=datetime.timezone.utc)
    formatted_date = datetime_obj.date().strftime("%Y%m%d")
    print(formatted_date)
    print(os.path.dirname(filename))

    print(datetime.datetime.strptime(formatted_date, "%Y%m%d").isoformat())

    all_photos = get_all_media(folder, supported_formats)
    selected_photos = all_files_to_copy("20240127", 5, all_photos)

    print(os.path.basename(filename))


def get_all_media(media_folder, supported_formats):

    if not os.path.isdir(media_folder):
        sys.exit("get_all_media error: " + media_folder + " is not a folder!")

    file_date_dict = {}
    for root, dirs, files in os.walk(media_folder):
        for each_file in files:
            filename = os.path.join(root, each_file)
            if os.path.isfile(filename):

                if filename.lower().endswith(supported_formats):
                    file_date = datetime.datetime.fromtimestamp(os.path.getmtime(filename),
                                                                tz=datetime.timezone.utc).date().strftime("%Y%m%d")
                    if file_date in file_date_dict.keys():
                        file_date_dict[file_date].append(filename)
                    else:
                        file_date_dict[file_date] = [filename]
    print("Media list generated.")
    return file_date_dict


def all_files_to_copy(start_date, num_days, file_date_dict):

    curr_day = datetime.datetime.strptime(start_date, "%Y%m%d")
    filelist = []
    for i in range(num_days):
        dict_key = curr_day.date().strftime("%Y%m%d")
        if dict_key in file_date_dict.keys():
            filelist.extend(file_date_dict[dict_key])
        curr_day += datetime.timedelta(days=1)

    print("File list generated.")
    return filelist


def copy_files(root_folder, files_list):
    for each_file in files_list:
        cmd = each_file + " " + root_folder
        if os.name == 'nt':  # Windows
            cmd = "copy " + cmd
        else:  # Unix/Linux
            cmd = "cp " + cmd
        os.system(cmd)
    print("Files copied.")


def check_input(photo_folder, start, end, copy_to_folder):
    if photo_folder == "":
        sys.exit("Error: No Photo Library chosen.")
    if copy_to_folder == "":
        sys.exit("Error: No copy_to folder chosen.")
    try:
        start_date = datetime.datetime.strptime(start, "%Y%m%d")
        end_date = datetime.datetime.strptime(end, "%Y%m%d")
        if start_date > end_date:
            sys.exit("Error: Start date later than end date!")
        else:
            return (end_date - start_date).days
    except:
        sys.exit("Error: Illegal date time format.")


def organise(photo_folder, media_formats, start, duration, copy_to_folder):
    all_media = get_all_media(photo_folder, media_formats)
    file_list = all_files_to_copy(start, duration, all_media)
    copy_files(copy_to_folder, file_list)


def main():


    if len(sys.argv) == 1:
        # UI mode
        media_formats = (".png", ".jpeg", ".jpg", ".cr2", ".heic", ".mov", ".mp4")
        photo_folder = input("Please input the Photos library directory:\n")

        start = input("Please input the start date in the format yyyymmdd:\n")
        end = input("Please input the end date in the format yyyymmdd:\n")
        copy_to_folder = input("Please input the folder to copy to:\n")

        duration = check_input(photo_folder, start, end, copy_to_folder) + 1

        organise(photo_folder, media_formats, start, duration, copy_to_folder)


    else:
        # headless mode
        print(sys.argv)

if __name__ == "__main__":
    main()