# GEOmetric
Calculate the Geography and Election Outcome metric
The Python program GEOMetricCalculatorForSharingFINAL.py will calculate the Geography and Election Outcome (GEO) metric as described in the preprint “The Geography and Election Outcome (GEO) Metric: An Introduction” by Campisi, Ratliff, Somersille, and Veomett available at https://arxiv.org/abs/2103.12856. 

The files in this directory demonstrate how to use the program to calculate the GEO metric for the enacted 2011 Congressional districting plan for Pennsylvania. 
Input files
There are two csv files required for input to GEOMetricCalculator.py:

PA_Senate2016_ElectionOutcome.csv

This file contains the Democratic and Republican election results of the 2016 election for the U.S. Senate broken down by Congressional district. 

The first column contains the district number, the second contains the votes for the Democratic candidate, and the third contains the votes for the Republican candidate. 



PA_2011map_edges.csv

This file contains adjacency information for the 2011 Congressional districts.  

Each row contains two district numbers, indicating that these districts are adjacent in the districting plan. 

Note: The districts may appear in either order. For example, if District 1 is adjacent to District 5, then the program will recognize 1,5 or 5,1 or even both. 

Parameters to set in GEOMetricCalculator.py
The user can input different files to evaluate a different map and/or different election outcome.

election_file = './PA_Senate2016_ElectionOutcome.csv'
edges_file = './PA_2011map_edges.csv'


These specify the input files described above. 

output_file_prefix = 'PASenate16'

This specifies the output file prefix, if you’d like to run the code on many different maps/election outcomes.


Output files
There will be two output files written for each party (thus, four output files total). The file names include the vote share parameters and columns from election_file used in calculating the GEO metric. 

1PASenate16_GEO_0.55_0.5.csv

This file contains four columns related to the party whose results are given in column 1 of election_file.  
The first gives the GEO score.
The second lists losing districts are made Newly Competitive when applying the GEO metric algorithm.
The third lists Contributing Won districts, i.e. those won by the party and transferred votes to a newly competitive district.
The fourth lists Contributing Lost districts, i.e. those lost by the party and transferred votes to a newly competitive district.

Note: The order of the districts in each column correspond to the order that they were encountered in the algorithm.  For newly competitive districts, this is by decreasing value of average neighbor vote share A_i.  For contributing districts, this is just by increasing numerical label of the district. 

1_aux_PASenate16_GEO_0.55_0.5.csv

This file contains additional information about the computations. It lists the Newly Competitive districts in the order in which the GEO metric algorithm transferred votes to them. For each Newly Competitive district, the file lists its original vote share, its average neighbor vote share, the district which transferred votes, the vote shares that district transferred, and whether the transferring district was winning or losing. 


Screen Output
The Python terminal screen will also output results.  It starts with party 1, and lists which districts were made competitive in order of decreasing neighborhood vote share A_i, and the contributing districts in increasing numerical order.

It then outputs the GEO score for that party, and a list of newly competitive districts (again in order of decreasing A_i).

It then outputs the contributing won districts, in decreasing order of the total votes they shared with all districts during the algorithm, along with that total votes shared.

Finally, it outputs the contributing lost districts, in decreasing order of the total votes they shared with all districts during the algorithm, along with that total votes shared.

All of the above is also printed for party 2.

For questions
Contact: 
Marion Campisi marion.campisi@sjsu.edu 
Tommy Ratliff ratliff_thomas@wheatoncollege.edu 
Stephanie Somersille ssomersille@gmail.com 
Ellen Veomett erv2@stmarys-ca.edu 
