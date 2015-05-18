# base_multiply
Python script to multiply non-negative integers in an aribtrary base from 2 to 16 inclusive

Python script to multiply non-negative integers in an aribtrary base from 2 to 16 inclusive

See usage statement, it's pretty straightforward: you specify a base between 2 and 16, inclusive, (default: 10) and any number of non-negative integers in that base to multiply together, and you will get the answer in that base.

The range of accepted bases can be trivially extended.

The simple way to do multiplication in an arbitrary base is to convert the inputs to base-10, do the multiplication, and convert the answer back into the desired base.
This script does not do that.
Instead, it goes back to first principles and uses the basic multiplication algorithm that you learned in grade school ("carry the one", etc.) directly in the desired base (except insofar as your computer's arithmetic unit uses base 10).

As a result, this is not necessarily efficient for what it does. But it was an exercise, and I am happy with the result.

You can use the script directly on the commandline, or you can import it as a module into another script.

The base_addition module that this script imports is similar in spirit and implementation, and can be found in a sibling repo to this one).
