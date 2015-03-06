Function scripts
================

-- makeBratAnnotation.py

Converts .chem (chemspot) files, stripping down to just <unique_id, span_start, span_end, Compound, entity>

Move this python script into the directory of .chem files or you will be asked to supply the directory path after
running.

If not present, a directory called "output" will be created in the directory where the .chem files are found, this
will contain the formatted files.
--

-- evaluateAnnotations.py

Given two directories of files, this will compare files in order. Inside each file it will try and find all
matches between the two files.

Sean Holloway, NTNU 2015