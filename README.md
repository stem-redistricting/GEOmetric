# GEOmetric

GEOMetricCalculatorForSharingFINAL.py will calculate the Geography and Election Outcome (GEO) metric as described in “The Geography and Election Outcome (GEO) Metric: An Introduction” by Campisi, Ratliff, Somersille, and Veomett, available at [https://www.liebertpub.com/doi/full/10.1089/elj.2021.0054](https://www.liebertpub.com/doi/full/10.1089/elj.2021.0054). 

## Input Data

Two csv files are required: the Election Outcome data and the Geography data.  

The Election outcome data has three columns: the first column contains the district number, the second contains the votes for the Democratic candidate, and the third contains the votes for the Republican candidate.  

The Geography data contains adjacency information for the districting map: each row contains two district numbers, indicating that these districts are adjacent in the districting plan. The districts may appear in either order. For example, if District 1 is adjacent to District 5, then the program will recognize 1,5 or 5,1 or even both. 

To start out, you may find it useful to try out these sample data:

[PA_Senate2016_ElectionOutcome.csv](https://github.com/stem-redistricting/GEOmetric/blob/0cbbda53d721c06cca85a7a09f88ba265d81363e/PA_Senate2016_ElectionOutcome.csv) contains the Democratic and Republican election results of the 2016 election for the U.S. Senate broken down by Congressional district.  



[PA_2011map_edges.csv](https://github.com/stem-redistricting/GEOmetric/blob/0cbbda53d721c06cca85a7a09f88ba265d81363e/PA_2011map_edges.csv) contains adjacency information for the 2011 Congressional districts.  


## Parameters
The user can input different files to evaluate a different map and/or different election outcome.

```
election_file = './PA_Senate2016_ElectionOutcome.csv'
edges_file = './PA_2011map_edges.csv'
```

These specify the input files described above. 

```
output_file_prefix = 'PASenate16'
```

This specifies the output file prefix, if you’d like to run the code on many different maps/election outcomes.


## Output files
There will be two output files written for each party (thus, four output files total). The file names include the vote share parameters used in calculating the GEO metric. 

```
1PASenate16_GEO_0.55_0.5.csv
```

This file contains four columns related to the party whose results are given in column 1 of election_file.  

1. The first gives the GEO score.
2. The second lists losing districts are made Newly Competitive when applying the GEO metric algorithm.
3. The third lists Contributing Won districts, i.e. those won by the party and transferred votes to a newly competitive district.
4. The fourth lists Contributing Lost districts, i.e. those lost by the party and transferred votes to a newly competitive district.

Note: The order of the districts in each column correspond to the order that they were encountered in the algorithm.  For newly competitive districts, this is by decreasing value of average neighbor vote share A_i.  For contributing districts, this is just by increasing numerical label of the district. 

```
1_aux_PASenate16_GEO_0.55_0.5.csv
```

This file contains additional information about the computations. It lists the Newly Competitive districts in the order in which the GEO metric algorithm transferred votes to them. For each Newly Competitive district, the file lists its original vote share, its average neighbor vote share, the district which transferred votes, the vote shares that district transferred, and whether the transferring district was winning or losing. 


## Screen Output
The Python terminal screen will also output results.  It starts with party 1, and lists which districts were made competitive in order of decreasing neighborhood vote share A_i, and the contributing districts in increasing numerical order.

It then outputs the GEO score for that party, and a list of newly competitive districts (again in order of decreasing A_i).

It then outputs the contributing won districts, in decreasing order of the total votes they shared with all districts during the algorithm, along with that total votes shared.

Finally, it outputs the contributing lost districts, in decreasing order of the total votes they shared with all districts during the algorithm, along with that total votes shared.

All of the above is also printed for party 2.

For questions, contact 
Ellen Veomett eveomett@usfca.edu 
Tommy Ratliff ratliff_thomas@wheatoncollege.edu 
