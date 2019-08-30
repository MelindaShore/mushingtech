#
#  The BSD License, because it's the 21st century and we have to
#  worry about this sort of nonsense
#
#  
#  Copyright (c) 2019, Melinda Shore
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

import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen

def getem():
    
    soup = BeautifulSoup(open("./pastiditarodmushers.html"), "html.parser")
    return { i.string:i['href'] for i in soup.find(class_="stats-table").find_all("a") }

#
#  we know what the data look like - if there's an href in it it's a
#    race, and it's got 5 fields.  This is exceptionally crude code
#

def do_stats(name, musher):
    entries = 0
    scratches = 0
    finishes = 0
    consecutives = 0
    max_c = 0

    try:
        soup = BeautifulSoup(open(musher), "html.parser")
    except Exception as e:
        try:
            soup = BeautifulSoup(urlopen(musher), "html.parser")
        except Exception as e:
            print('{0}: {1}'.format(sys.argv[0], e))
            sys.exit(1)
  
    for row in soup.find_all("tr"):
        if row.a:
            entries += 1
            tmp = list(row.find_all("td"))
            if tmp[1].string == "-":
                scratches += 1
                consecutives += 1
            else:
                finishes += 1
                consecutives = 0
            if consecutives > max_c: 
                max_c = consecutives
    return(list(map(str, [name, entries, finishes, scratches, max_c])))


def main():
    mushers = getem()
    for musher in mushers.keys():
        res = do_stats(musher, mushers[musher])
        print(", ".join(res))

 
if __name__ == "__main__":
    main()
