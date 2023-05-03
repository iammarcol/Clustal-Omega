# Web Development Task
DBW web-site and Clustal Omega web application made in Django (python)

Web application to execute an external program (CLUSTAL-Omega)
The task was to prepare a web application (php or python/flask, running in the course server) to perform multiple sequence alignment using Clustal-Omega (executable can be obtained from http://www.clustal.org). It should have
Input options:
A set of protein sequences (in FASTA)
A set of Uniprot ids (sequences could be obtained from https://www.uniprot.org/uniprot/{id}.fasta)
A File upload as alternative input source
Program options (minimum set):
output format
(Optional) other Clustal-O options
check input for errors (e.g. Unkown format, No sequences available, ...)
format the output (be aware of the possible output formats), and allow to download results.

I also added a simple code written in Java on the error messaging when the wrong input is given. 
The code first checks if the input is in the correct format or not and then prints out a message on the screen.
The page is automatically refreshed and automatically scrolled to the position where the error message is stated.

