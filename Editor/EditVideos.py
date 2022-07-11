import os
from itertools import islice

from moviepy.editor import VideoFileClip, concatenate_videoclips
from Utilities import HelperFunctions, PrintFunctions
from ComputeData.ComputeRawChatData import dataProcessing

# clip1 = VideoFileClip("yoimiya.mp4").subclip(55, 65)
# clip2 = VideoFileClip("ganyu.mp4").subclip(8000000, 10000000)
# clip3 = VideoFileClip("yoimiya.mp4").subclip(195, 225)

# combined = concatenate_videoclips([clip1, clip2, clip3])


# try:
#     clip2 = VideoFileClip("ganyu.mp4")
#     #print(clip2.end)
#     #clip2.subclip(800000, 10000000) # Breaking it like this prevents IGNORED exceptions from occuring
#     #combined = concatenate_videoclips([clip2])
#     #combined.write_videofile("combinedOUTOFBOUNDS.mp4")
# except:
#     print("Invalid Timestamps!")

# Having this makes us pretend we SELECTED 9 from the main program
#os.chdir("C:/Users/Arisa/PycharmProjects/julyProject")


def subclip_prerequisite():
    RawChatDataFile = files_displayed_to_user_and_user_selects_file(HelperFunctions.RawChatDataDir, "txt")

    # Turn the File into a dictionary
    data_dict = convert_raw_time_data_to_dictionary(RawChatDataFile)


    splitter = 20
    num_of_lines = -abs(5)

    split_dict = group_dict_values_by_splitter(data_dict, splitter)
    seconds_timestamp = []

    split_dict = sorted(split_dict.items(), key=lambda x: x[1])
    sort_dict = dict(split_dict)

    for i in range(-1, num_of_lines, -1):
        try:
            print(list(sort_dict)[i])
            seconds_timestamp.append(HelperFunctions.string_time_to_seconds(list(sort_dict)[i]))
        except:
            pass

    seconds_timestamp.sort()

    print(seconds_timestamp)

    # TODO: Load up video [mp4]
    #RawVideoFile = files_displayed_to_user_and_user_selects_file(HelperFunctions.VideoDownloadedDir, "mp4")

    print(RawChatDataFile)
    #print(RawVideoFile)





def files_displayed_to_user_and_user_selects_file(file_directory, extension):
    print("HELLO WORLD")
    print(file_directory)

    list_of_contents = HelperFunctions.getContents(file_directory, extension)

    for index, value in enumerate(list_of_contents): # Display the files in the directory with a choice number
        print("\t[{}]: {}".format(index, value))

    try:
        i = input("Please select the text-file you want to compute: ")
    except:
        print("An exception was found!")
        return

    try: # Attempt to open the file the user selected
        File = open(file_directory + "\\" + list_of_contents[int(i)], "r")
    except:
        print("{} isn't a valid choice".format(i))
        return

    return File


def convert_raw_time_data_to_dictionary(file):
    dict_with_the_raw_time_data = dict()

    for line in file: # Loop through each line of the file
        line = line.strip() # Remove the leading spaces and newline character
        line = line.lower() # Convert characters to lowercase
        # line = line.translate(line.maketrans("", "", string.punctuation)) # Removes the ':'
        words = line.split(" ") # Split the line into words


        for word in words: # Iterate over each word in line
            if (HelperFunctions.check_negative_sign(word)): pass # Looks for a negative value and skips it

            elif word in dict_with_the_raw_time_data: # Check if the word is already in dictionary
                dict_with_the_raw_time_data[word] = dict_with_the_raw_time_data[word] + 1 # Increment count of word by 1

            else: dict_with_the_raw_time_data[word] = 1 # Add the word to dictionary with count 1

    return dict_with_the_raw_time_data


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
