# -*- coding: utf-8 -*-
"""
EV mods 3, started Mar 10, 2023 (fixed to allow for non-integer district names)

TR mods 3, started Oct 25, 2021 (minor screen output tweaks)

EV mods 2, started Sept 14, 2021

TR Mods 2, started May 28, 2021

EV Mods, started May 26, 2021

TR Mods, started May 10, 2021

Created by SS on Mon Mar  1 19:07:45 2021


This code runs on a pair of csv files.
One file has an election outcome for each district in a districting map.
The second file has the edges for the dual graph of that map.
The output is a set of csv files. For each party, two files are written:
    One giving the GEO score, newly competitive, contributing won, and contributing lost districts
    A second auxillary file giving information about each newly competitive district:
        original vote share, average neighbor vote share, district transferring votes, whether the transfering district was winning or losing

@authors: Tommy Ratliff, Stephanie Somersille, Ellen Veomett

This code enacts the algorithm for the GEO metric.
That is, it
    1) Orders the districts by decreasing value of average neighbor vote share A_i
    2) Then adds vote shares to losing districts (if possible) from neighboring districts
        2a) Vote shares are transferred proportional to shareable votes
        2b) No district's vote share can drop below either 55% (if winning) or average neighbor vote share minus one standard deviation of average neighborhood vote share
    3) Shareable vote shares are re-calculated, and the next losing district (in decreasing A_i order) is considered

"""

#import needed libaries 
import pandas as pd 
from collections import OrderedDict


#Define input files



election_file = './PA_Senate2016_ElectionOutcome.csv'
edges_file = './PA_2011map_edges.csv'



#Set parameters for GEO metric
min_cvs = 0.5 #Vote share losing districts must reach to become competitive
max_cvs = 0.55 #Vote share that winning districts cannot drop below

#Specify columns in election data files to use 
#Column 0 should contain district labels, other columns contain party vote totals
input_cols_to_use = [0,1,2] 

#Define output file name
output_file_prefix = 'PASenate16'

output_file_suffix = '_GEO_'+str(max_cvs)+'_'+str(min_cvs)+'.csv'
output_file = output_file_prefix + output_file_suffix


#-------------Should not need to make any modifications beyond this point-----------------------

    
#Read election data, use district names in first column as index, uses parties in input_cols_to_use variable 
#build dataframe with vote share
election_df = pd.read_csv(election_file,  header=None, index_col=0, usecols=input_cols_to_use)
    
num_parties = len(election_df.columns)            
total_votes =  election_df.iloc[:,0:num_parties+1].sum(axis=1)

vote_share_df = pd.DataFrame(index=election_df.index,columns=election_df.columns)
for i in range(1,num_parties+1):                    #range(1,k) loops through 1, 2, . . . ,k-1
    vote_share_df[i] = election_df[i]/total_votes
    
    
#Build sorted list of all edges
#Deal with duplicates (d1,d2) or (d1,d2) listed but not (d2,d1) in edges_file
#Last lines drop duplicates and reindex 
edges_df = pd.read_csv(edges_file, header=None, index_col=False)
tmp_df = edges_df.rename(columns={0:1,1:0},copy=False)
all_edges_df = pd.concat([edges_df,tmp_df])
all_edges_df.drop_duplicates( keep='first', inplace=True)
all_edges_df.reset_index(drop=True, inplace=True)  
    
#Build lists of neighbors
#neighbors[i] will contain list of neighbors of district i
districts=election_df.index.tolist()  #Get list of districts from election_df
neighbors = dict()  #Initiate empty dictionary of neighbors
for district in districts:
    n_index = all_edges_df[(all_edges_df[0] == district)][1].tolist()   #Get index in all_edges_df of neighbors of i
    neighbors[district] = n_index  #Add values to neighbors list
    
    

    
screen = '{:<10} {:<30}' #Output format for screen

#Loop through all parties
for party in range(1,num_parties+1):
    print("\n\nParty ",party," GEO calculations\n") #just to make screen output more readable
    print(screen.format('District', 'Made competitive by'))
    
    geo_score = 0
    newly_competitive = []
    contributing_won= []
    contributing_lost = []

    
    geo_df = pd.DataFrame(index=election_df.index, columns=['Original Vote Share', 'Vote Share','Avg Neighbor Vote Share','Votes to Share','Made Competitive','Total Votes Shared','Is Competitive'])
    geo_df['Original Vote Share'] = vote_share_df[party]
    geo_df['Vote Share'] = vote_share_df[party]
    geo_df['Made Competitive'].values[:] = 0
    geo_df['Is Competitive'].values[:] = False          
    geo_df['Total Votes Shared'].values[:] = 0          
    
    
    #Dataframe to hold details of districts made competitive
    aux_df = pd.DataFrame(columns=['Newly Competitive District', 'Original Vote Share','Avg Neighbor Vote Share','District Transferring Votes', 'Vote Shares Transferred', 'Transferring District Winning/Losing'])
        
    
    #Compute Avg Neighbor Vote Share 
    for district in districts:
        total_neighborhood_votes = geo_df.loc[neighbors[district],'Vote Share'].sum() + geo_df.at[district,'Vote Share']
        geo_df.at[district,'Avg Neighbor Vote Share'] = total_neighborhood_votes / (len(neighbors[district])+1)
        
    #Use standard deviation of A_i to adjust votes to share, allow possibility of different adjustments for winning and losing districts 
    stdev = geo_df['Avg Neighbor Vote Share'].std()
    win_adj = stdev     #A_i - win_adj for winning districts
    loss_adj = stdev    #A_i - loss_adj for losing districts
    
        
    for district in districts:
        avg_neigh_vs = geo_df.at[district,'Avg Neighbor Vote Share']
        if geo_df.at[district,'Vote Share'] > max_cvs:   #Winning district that we potentially allow to share votes
            geo_df.at[district,'Votes to Share'] = max(0, geo_df.at[district,'Vote Share'] - max(max_cvs,avg_neigh_vs-win_adj))
        elif geo_df.at[district,'Vote Share'] >= min_cvs:  #Winning district we do not allow to share votes
            geo_df.at[district,'Votes to Share'] = 0
            geo_df.at[district,'Is Competitive'] = True            
        else:                                   #Losing district
            geo_df.at[district,'Votes to Share'] = max(0, geo_df.at[district,'Vote Share']-(avg_neigh_vs-loss_adj))
        
      
        
    #Sort by 'Avg Neighbor Vote Share', then get stable_wins and losses in this order
    geo_df.sort_values(by='Avg Neighbor Vote Share', axis=0, ascending=False, inplace=True)    
    stable_win = geo_df.index[(geo_df['Vote Share']>max_cvs)].tolist()
    loss =  geo_df.index[(geo_df['Vote Share']<min_cvs)].tolist()
        
    #All the districts to consider for shifting votes
    stable_win_loss = stable_win + loss
    
        
    #Run through loss districts to see if can make competitive
    for j in loss:
        needs_to_be_competitive = min_cvs - geo_df.at[j,'Vote Share'] 
            
        #Find vote shares that can be transferred in from neighbors
        shareable_neighbors = list( set.intersection( set(neighbors[j]), set(stable_win_loss)))
        neighbors_votes_to_share = geo_df.loc[shareable_neighbors,'Votes to Share'].sum()
        
        if needs_to_be_competitive <= neighbors_votes_to_share:  #If there's enough vote shares from neighbors to change district to competitive
                # Adjust j to be competitive and remove j from stable_win_loss list
                geo_df.at[j,'Vote Share'] = min_cvs
                geo_df.at[j,'Votes to Share'] = 0          
                geo_df.at[j,'Is Competitive'] = True
                geo_df.at[j,'Made Competitive'] = True
                newly_competitive.append(j)
                stable_win_loss.remove(j)
                
                # Loop through shareable_neighbors, reducing votes to share
                #  Reduce by proportion of votes neighbors have to share
                sharing_neighbors = []
                for k in shareable_neighbors:
                    if geo_df.at[k, 'Votes to Share'] == 0:    #It didn't end up sharing anything, so we don't want to note it
                        continue
                    sharing_neighbors.append(k)
                    votes_shared = (geo_df.at[k,'Votes to Share']/neighbors_votes_to_share) * needs_to_be_competitive
                    geo_df.at[k,'Vote Share'] -=  votes_shared
                    geo_df.at[k,'Votes to Share'] -=  votes_shared 
                    geo_df.at[k,'Total Votes Shared'] += votes_shared
                    
                    aux_df.loc[len(aux_df.index)]=[j,geo_df.at[j,'Original Vote Share'],geo_df.at[j,'Avg Neighbor Vote Share'],k, votes_shared,'']
                    if geo_df.at[k,'Original Vote Share'] >= 1/2:    #Creating list of contributing won
                        contributing_won.append(k)
                        aux_df.at[len(aux_df.index)-1,'Transferring District Winning/Losing']='W'
                    else:
                        contributing_lost.append(k)    #Creating list of contributing losses
                        aux_df.at[len(aux_df.index)-1,'Transferring District Winning/Losing']='L'
                        
                        
                
                print(screen.format(j, ' '.join(map(str,sharing_neighbors))))
                
    
    
    
    #Count number of non-zero values in 'Made Competitive'        
    geo_score = geo_df['Made Competitive'].astype(bool).sum()
 
    #Get rid of duplicates
    contributing_won = list(OrderedDict.fromkeys(contributing_won))
    contributing_lost = list(OrderedDict.fromkeys(contributing_lost))
    
    #more screen output
    print("\n")
    print(f"Geo score for party {party} is: {geo_score}")
    print(f"Newly Competitive Districts for party {party}: {newly_competitive}")
    
    print("\n")
    
    
    #Note:  The following changes the ordering in the dataframe, but does not impact ordering of output files.
    geo_df.sort_values(by='Total Votes Shared', axis=0, ascending=False, inplace=True)
    indices_sorted_by_TotalVotesShared = geo_df.index.tolist()
  
    # We print the Contributins won districts first, in order of total votes shared
    print("Contributing won districts:")
    print(screen.format('District','Total vote shares contributed'))
    for d in indices_sorted_by_TotalVotesShared:
        if d in contributing_won:
            print(screen.format(d,geo_df.at[d, 'Total Votes Shared']))
    
    #Now print Contributing lost districts, in order of total votes shared
    print("\n")
    print("Contributing lost districts:")    
    print(screen.format('District','Total vote shares contributed'))
    for d in indices_sorted_by_TotalVotesShared:
        if d in contributing_lost:
            print(screen.format(d,geo_df.at[d, 'Total Votes Shared']))
    
    
    
    """The remaining code just outputs the information in to the two files,
    with steps taken to make it format nicely """
    
    #Adjusting the data so it prints nicely to the csv file
    longestLength = max(1, len(newly_competitive),len(contributing_won), len(contributing_lost))
    newly_competitive.extend(['']*(longestLength-len(newly_competitive)))
    contributing_won.extend(['']*(longestLength-len(contributing_won)))
    contributing_lost.extend(['']*(longestLength-len(contributing_lost)))
    geo_array = [geo_score]
    geo_array.extend(['']*(longestLength-len(geo_array)))
    
    
    #Convert our list of lists to a dataframe and save   
    #In main csv file, newly competitive districts are listed in order of becoming newly competitive (in decreasing A_i order), districts transferring votes listed in order in which they contributed.    
    geo_scores_df = pd.DataFrame({"GEO score": geo_array,  "Newly Competitive": newly_competitive,  "Contributing Wins": contributing_won, "Contributing Losses": contributing_lost})        
    geo_scores_df.to_csv(str(party)+output_file, header=True)  
    #In aux csv file, newly competitive districts are again listed in order of becoming newly competitive (in decreasing A_i order), districts transferring votes listed in increasing numerical order.
    aux_df.to_csv(str(party)+'_aux_'+output_file, header=True, float_format='%.5f')  
 
    
 
 



