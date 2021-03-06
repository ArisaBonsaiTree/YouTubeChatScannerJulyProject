import threading
from itertools import islice

from moviepy.editor import VideoFileClip, concatenate_videoclips

from ComputeData.ComputeHelperFunctions import \
    convert_string_timestamps_into_seconds, create_dict_with_timestamps, convert_raw_time_data_to_dictionary_FILTERED, \
    get_last_timestamp_from_from

from Utilities.HelperFunctions import RawChatDataDir, string_time_to_seconds, ROUND_DOWN_VALUE, \
    ClippedVideo, VideoDownloadedDir, getContents


# NUMBER_OF_LINES = -abs(2)
# SPLIT_DICT_BY_SECONDS = 10 # Added this to the upperbound, since we only start at the beginning of a timestamp group
# ADDED_SECONDS_TO_CLIPS = 0


def subclip_prerequisite():

    file, list_of_contents, selected_file_index = files_displayed_to_user_and_user_selects_file(RawChatDataDir, "_CLEANED.txt")
    last_line = get_last_timestamp_from_from(file.name)

    START = 0
    END = convert_string_timestamps_into_seconds(last_line)
    END_ROUND_DOWN = END - (END % ROUND_DOWN_VALUE)


    dict_with_all_timestamps = create_dict_with_timestamps(START, END_ROUND_DOWN)
    data = convert_raw_time_data_to_dictionary_FILTERED(dict_with_all_timestamps, open(file.name, 'r'))

    SPLIT_DICT_BY_SECONDS = int(input("How many seconds do you want to break the dictionary in[SPLITTER]? "))

    splt_dict = group_dict_values_by_splitter(data, SPLIT_DICT_BY_SECONDS)
    splt_dict = sorted(splt_dict.items(), key=lambda x: x[1])

    sort_dict = dict(splt_dict)

    seconds_timestamp = []

    NUMBER_OF_LINES = int(input("How many lines of data do you want to use[HOW MANY TIMESTAMPS]? "))
    NUMBER_OF_LINES = -abs(NUMBER_OF_LINES)

    for i in range(-1, NUMBER_OF_LINES - 1, -1):
        try:
            seconds_timestamp.append(string_time_to_seconds(list(sort_dict)[i]))
        except:
            pass

    seconds_timestamp.sort()

    clip, RawVideoFile, name = user_selects_video_to_clip()


    if (not clip):
        print("ERROR")
        return


    #ADDED_SECONDS_TO_CLIPS = int(input("How many seconds do you want to add to each clip [ALSO ADDED 'SPLIT_DICT_BY_SECONDS' into the upperbound? "))
    LOWER_BOUND_SECS = int(input("How many seconds do we want to add BEFORE the timestamp? "))
    UPPER_BOUND_SECS = int(input("How many seconds do you want to add AFTER the timestamp? "))
    Thread = threading.Thread(target=createClip, args=(seconds_timestamp, clip, name, LOWER_BOUND_SECS, UPPER_BOUND_SECS,))
    Thread.start()


def createClip(seconds_timestamp, clip, name, LOWER_BOUND_SECS, UPPER_BOUND_SECS,):
    START_VIDEO = clip.start
    END_VIDEO = clip.end
    list_of_clips = []

    for i in seconds_timestamp:
        try:
            lower_bound = (i - LOWER_BOUND_SECS) if (i - LOWER_BOUND_SECS) > START_VIDEO else START_VIDEO
            upper_bound = (i + UPPER_BOUND_SECS) if (i + UPPER_BOUND_SECS) < END_VIDEO else END_VIDEO
            list_of_clips.append(clip.subclip(lower_bound, upper_bound))
        except: pass


    combined_clips = concatenate_videoclips(list_of_clips)
    name = name.split(".")[0]
    combined_clips.write_videofile(ClippedVideo + "/" + name + "_COMBINED.mp4")


def files_displayed_to_user_and_user_selects_file(file_directory, extension):
    print(file_directory)

    list_of_contents = getContents(file_directory, extension)

    for index, value in enumerate(list_of_contents):  # Display the files in the directory with a choice number
        print("\t[{}]: {}".format(index, value))

    try:
        i = input("Please select the text-file you want to compute: ")
    except:
        print("An exception was found!")
        return False


    try:  # Attempt to open the file the user selected
        File = open(file_directory + "\\" + list_of_contents[int(i)], "r")
    except:
        print("{} isn't a valid choice".format(i))
        return False

    name = list_of_contents[int(i)].split(".")[0]

    return File, list_of_contents, i


def user_selects_video_to_clip():
    RawVideoFile, listofcontent, i = files_displayed_to_user_and_user_selects_file(VideoDownloadedDir, "mp4")
    if (not RawVideoFile):
        return False

    clip = VideoFileClip(RawVideoFile.name)

    return clip, RawVideoFile, listofcontent[int(i)]

# We get splitter amount of values --> add them up --> place it
def group_dict_values_by_splitter(dict, splitter):
    new_dict = {}

    for item in chunks(dict, splitter):
        new_dict[list(item.keys())[0]] = sum(item.values())
    return new_dict

def chunks(data, SIZE=1000000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k: data[k] for k in islice(it, SIZE)}
