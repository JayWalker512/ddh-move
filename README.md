# ddh-move

Consumes the output list of duplicate files from [ddh](https://github.com/darakian/ddh) and lets you 
do something with the duplicates. **ddh** 
is a great tool for finding duplicate files in your directories, but it doesn't do anything with them.
**ddh-move** allows you move the duplicates to another location (or delete them)
according to some criteria.

This is a work in progress, I'll be adding tests and more options in the future.

Usage:
------
    ddh <Directory> --output no --format json -v duplicates | tail -n 1 | python3 ddh-move.py <Destination> [OPTIONS]

When run with no options, the file names are sorted and the first file is kept while the rest are moved to
the provided destination. For example, if files **a.txt**, **b.txt**, **c.txt** were identical, files
**b.txt** and **c.txt** will be moved to the provided destination and **a.txt** will be left in the original
location.

Options:
--------
    --dry-run    Print the files to be moved without moving them.

Testing:
--------
The tests assume that you have **ddh** installed on your system, in my case I just copied the binary to **/usr/bin**.
This is to ensure continued compatibility with future versions of **ddh** and my script, as well as
possibly varied output from **ddh** which would not be captured by a static text copy of **ddh** output. 
    
Requirements:
-------------
**ddh-move** and its tests require Python 3.5 or above.  
  
License
-------
Copyright 2019 Brandon Foltz

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
