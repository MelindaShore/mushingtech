#
#  The BSD License, because it's the 21st century and we have to
#  worry about this sort of nonsense
#
#  
#  Copyright (c) 2014, Melinda Shore
#  All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without 
#  modification, are permitted provided that the following conditions are met:
#  
#  1. Redistributions of source code must retain the above copyright notice, 
#     this list of conditions and the following disclaimer.
#  
#  2. Redistributions in binary form must reproduce the above copyright 
#     notice, this list of conditions and the following disclaimer in the 
#     documentation and/or other materials provided with the distribution.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
#  CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# TODO : add run calculations

import sys
import argparse
from bs4 import BeautifulSoup
import re
import urllib2

def cleanup(datum):
    return float(datum.rstrip(','))

def pull_data(script):
    data = []

    for item in script.split(';'):
        scanned = re.search('d2.push\(\[(.+?)\]\)', item)
        if scanned:
            data.append(map(cleanup, scanned.group(1).split()))
    return data


def main():
    soup = ""
    speed_list = []             # extracted times/speeds tuples
    nrests = 0                  # how many times this team has rested
    nruns = 0                   # how many runs

    speed_thresh = .5           # the speed below which we assume we're not really moving
    time_thresh = 1.0           # have to be stopped at least this long to be
                                # assumed to be resting
    start_time = 0.0            # holds the start hour for the rest
    in_rest = True              # state variable
    run_start = 0.0             # track the time a "run" starts
    duration = 0.0
    total_rest = 0.0
    total_run = 0.0
    default_rest_format = 'Rest at race time: {0} hours, duration: {1} hours'
    default_run_format = 'Run at race time: {0} hours, duration: {1} hours'
    csv_run_format = 'R,{0},{1}'
    csv_rest_format = 'T,{0},{1}'
    out_rest_format = default_rest_format
    out_run_format = default_run_format
    csv = False                 # state variable for whether or not we're writing csv

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='speed', type=float,
                       help='Speed below which the team will be considered at rest')
    parser.add_argument('-t', dest='time', type=float,
                        help='Minimum stopped time for which the time will be considered at rest')
    parser.add_argument('-c', help='Format output as csv', action='store_true')
    parser.add_argument('times_uri')
    args = parser.parse_args()
    if args.speed:
        speed_thresh = args.speed
    if args.time:
        time_thresh = args.time
    if args.c:
        csv = True
        out_rest_format = csv_rest_format
        out_run_format = csv_run_format
    
    try:
        soup = BeautifulSoup(open(args.times_uri), "lxml")
    except Exception as e:
        try:
            soup = BeautifulSoup(urllib2.urlopen(args.times_uri), "lxml")
        except Exception as e:
            print '{0}: {1}'.format(sys.argv[0], e)
            sys.exit(1)
    for script in soup.find_all(id='source'):
        if 'd2' in str(script):
            speed_list = pull_data(str(script))
            for point in speed_list:
                if point[1] < speed_thresh: # point[0] holds hours since start, point[1] holds speed
                    if not in_rest:
                        in_rest = True
                        duration = point[0] - run_start
                        print out_run_format.format(run_start, duration)
                        total_run += duration
                        nruns += 1
                        start_time = point[0]
                else:
                    if in_rest:
                        duration = point[0] - start_time
                        if duration > time_thresh:
                            print out_rest_format.format(start_time, duration)
                            total_rest = total_rest + duration
                            nrests = nrests + 1
                            run_start = point[0]
                        in_rest = False
                        start_time = 0.0
            if not csv:
                print 'Number of rests: {0}'.format(nrests)
                print 'Total rest: {0}'.format(total_rest)
                print 'Number of runs: {0}'.format(nruns)
                print 'Total run time: {0}'.format(total_run)

if __name__ == '__main__':
    main()
