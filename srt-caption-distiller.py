#!/usr/bin/env python
# -*- coding: utf-8 -*-


# SRT Caption Distiller
#
# Copyright © 2022, Trevor Masinelli (aka tmaaz)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.


# import modules

import sys
import os
import pathlib
import shutil
from datetime import datetime, timedelta
import textwrap
import math
import re


# define variables

ask_path = ''                                    # path to original .srt file
raw_check = ''                                   # make sure we were given an .srt file
raw_split = []                                   # list to split the path and file name
raw_path = ''                                    # path to files
raw_name = ''                                    # raw file name
dis_path = ''                                    # full path to our temp .txt file
fin_path = ''                                    # full path to our final .srt file
fin_name = ''                                    # final distilled file name
batch_num = 0                                    # sequential batch number used in new file (will increase with every batch / split)
batch_work = []                                  # list of text lines from temp file to parse
batch_time = '00:00:00,000 --> 00:00:00,000'     # string we will break into ms integers for maths
batch_time_open = '00:00:00.000'                 # batch open time, timedelta format
batch_time_close = '00:00:00.000'                # batch close time, timedelta format
batch_open = 0                                   # batch total open time, in ms
batch_close = 0                                  # batch total close time, in ms
batch_clock = 0                                  # actual batch time (batch open to close)
this_payload = ''                                # text from current batch
payload_length = 0                               # number of characters in current batch
one_line_max = 37                                # per FCC guidelines, the optimum max line length for a caption
two_line_max = (2 * one_line_max)                # per FCC guidelines, the optimum total length per closed caption (2 lines @ max length)
batch_shift = []                                 # manageable slices from oversized batch
slice_count = 0                                  # number of slices
sorted_set = ''                                  # final chronological set of distilled and formatted batches, to be written to file
evenflow = 0                                     # even split of batch time into slice time
oddflow = 0                                      # odd split of batch time into slice time
slice_cent = 0                                   # even percent of the whole batch time each slice is
odd_big = 0                                      # offset for odd slice, full slice
odd_small = 0                                    # offset for odd slice, remainder

# define functions

def wind_clock(adj_time):
    h, m, s = map(float, adj_time.split(':'))
    adj_time = timedelta(hours=h, minutes=m, seconds=s).total_seconds() * 1000
    adj_time = int(adj_time)
    return adj_time

def clock_even(time):
    hh = str(int(time/(1000*60*60))%24).zfill(2)
    mm = str(int(time/(1000*60))%60).zfill(2)
    ss = round((time/1000)%60, 3)
    ss = format(ss, '.3f').zfill(6).replace('.', ',')
    return (hh + ":" + mm + ":" + ss)


# main code

def main():

    # define globals
    global batch_num
    global sorted_set

    # ask for the .srt file, and fault gracefully if not found, or if not .srt
    ask_path = input('*** SRT Caption Distiller *** \n \n Please type the full path of your .srt file, or drag-and-drop your .srt file into this window, then press "Enter": ')
    if os.path.exists(ask_path) is False:
        print('I was unable to find the .srt file at ' + str(ask_path))
        quit()
    raw_check = os.path.splitext(ask_path)[-1]
    if raw_check != '.srt':
        print('The file provided is not a valid .srt file. Please only submit a valid .srt file')
        quit()

    # set up all the necessary pathing and naming conventions now
    raw_split = os.path.split(ask_path)
    raw_path  = raw_split[0]
    raw_name  = raw_split[1]
    dis_path  = (raw_path + '/srt_dist_temp.txt')
    fin_name  = ((os.path.splitext(raw_name)[0]) + '_distilled.srt')
    fin_path  = (raw_path + '/' + fin_name)

    # we have to wrap the process in a try, because it gets confused and faults when we run out of batches
    try:
        # copy the chosen .srt file and rename as our temp.txt file
        shutil.copy(ask_path, dis_path)

        # line-by-line inbound process loop
        with open(dis_path, 'r') as fin:                             # open our temp.txt for READ
            batch_work = fin.read().splitlines(True)                 # pull content into list, broken into individual lines

        # parse all batch sections into main variables
        while batch_work:                                            # iterate through list, until empty
            if batch_work[0] == '\n':                                # delete errant returns that sometimes get stuck at the top
                batch_work.pop(0)
            batch_time = batch_work[1].strip()                       # pull timing string, remove newline from result
            x = 2                                                    # reset our counter variable just in case
            this_payload = ''                                        # reset our payload variable just in case
            try:
                while batch_work[x] != '\n':                         # stubbornly throws unnecessary exceptions - embedded in 'try' to quash them
                    batch_work[x].split('\n')                        # pull the line, and remove the hard return
                    this_payload += (batch_work[x].strip() + ' ')    # add this line plus a space to the payload
                    if x < len(batch_work):                          # exception check for when we reach the end of the file
                        x += 1                                       # increase counter to keep checking lines
                    else:
                        break
            except (IndexError):                                     # finally break free from the 'while' exception
                pass
            del batch_work[0:x]                                      # remove batch from list that we're about to process
            payload_length = len(this_payload)                       # get the length of the payload (character count)

            # process the payload -- verious methods depending on size and content of playload

            # correct a common srt glitch where a space will dissappear between the end of a sentence and the following capital letter
            this_payload = re.sub(r"(\w)([A-Z])", r"\1 \2", this_payload)

            # one line batch - no extra processing, just increase the batch number, insert to sorted_set, and move on to next batch
            if payload_length <= one_line_max:
                batch_num += 1
                sorted_set += (str(batch_num) + '\n' + batch_time + '\n' + this_payload + '\n' + '\n')

            # two line batch - increase the batch number, format strings properly, insert to sorted_set, and move on to next batch
            elif payload_length > one_line_max and payload_length < two_line_max:
                batch_num += 1
                this_payload = textwrap.fill(this_payload, width=one_line_max)
                sorted_set += (str(batch_num) + '\n' + batch_time + '\n' + this_payload + '\n' + '\n')

            # oversized batches - the whole reason for this script. Let's break the clock, slice the playload into proper-sized batches, then rebuild within the given timeframe
            else:
                # pull timestamps, convert to timedelta format (hh:mm:ss.fff), then to ms integer
                batch_time_open = (batch_time[0:12]).replace(',', '.')
                batch_open = wind_clock(batch_time_open)
                batch_time_close = (batch_time[17:]).replace(',', '.')
                batch_close = wind_clock(batch_time_close)
                batch_clock = (batch_close - batch_open)

                # break the batch into slices and count them
                batch_shift = textwrap.wrap(this_payload, width=two_line_max)
                slice_count = len(batch_shift)

                # slice time evenly to divide given time equally between slices
                evenflow = math.floor(batch_clock / slice_count)

                # if we have uneven slice payloads, modify the timing for the full-size slices, versus the last (small) slice, within the given time parameter
                if (len(batch_shift[-1]) <= one_line_max):                              # if the last slice is only one line or less
                    slice_cent = round((100 / slice_count), 2)                          # figure out our percentage per slice, to sub-split time properly
                    oddflow = round(((evenflow / 100) * slice_cent), 2)                 # divide the total time by the percentage of one slice
                    odd_big = int(evenflow + (oddflow / (slice_count - 1)))             # spread the lion's share of percentage evenly to full size slices
                    odd_small = int(evenflow - oddflow)                                 # subtract an equal total percentage portion from the total for the remainder slice, to get to 100%
                    for z in batch_shift:
                        batch_num += 1                                                  # increase the batch number
                        if z == batch_shift[-1]:                                        # if this is the last loop
                            batch_close = (batch_open + odd_small) -1                   # increase the clock stop position by smaller amount, then reduce by 1 to compensate for drift
                        else:                                                           # otherwise this is a full-sized slice, so
                            batch_close = (batch_open + odd_big)                        # increase the clock stop position by larger amount
                        batch_time_open = clock_even(batch_open)                        # calculate and rebuild the open clock string via function
                        batch_time_close = clock_even(batch_close)                      # calculate and rebuild the close clock string via function
                        batch_time = (batch_time_open + ' --> ' + batch_time_close)     # now we can rebuild the batch_time string for this batch

                        # format the payload and assemble the pieces
                        this_payload = textwrap.fill(z, width=one_line_max)
                        sorted_set += (str(batch_num) + '\n' + batch_time + '\n' + this_payload + '\n' + '\n')

                        # advance the clock's start position, so we pick up where we left off
                        batch_open = (batch_close + 1)

                # we have even slice payloads, so we can evenly split the timing
                else:
                    for z in batch_shift:
                        batch_num += 1                                                  # increase the batch number
                        batch_close = (batch_open + evenflow)                           # increase the clock stop position
                        batch_time_open = clock_even(batch_open)                        # rebuild the open clock via function
                        batch_time_close = clock_even(batch_close)                      # rebuild the close clock via function
                        batch_time = (batch_time_open + ' --> ' + batch_time_close)     # rebuild the batch_time string for this batch

                        # format the payload and assemble the pieces
                        this_payload = textwrap.fill(z, width=one_line_max)
                        sorted_set += (str(batch_num) + '\n' + batch_time + '\n' + this_payload + '\n' + '\n')

                        # advance the clock's start position, so we pick up where we left off
                        batch_open = (batch_close + 1)

    # we've run out of batches, let's wrap things up
    except (IndexError):
        pass

    # all data is processed, overwrite everything back into the temp file
    with open(dis_path, 'w') as fout:
        fout.writelines(sorted_set)

    # once loaded, change the temp file into the final file
    os.rename(dis_path, fin_path)

    # tell the user that the process is done
    print('\n' + 'The file has been processed successfully,' + '\n' + 'and saved in the same location as your original file.' + '\n' + 'Thank you for using SRT Caption Distiller!')

    quit()


if __name__ == '__main__':
    main()
