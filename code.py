# --------------
import pandas as pd 
import numpy as np
# Read the data using pandas module.
df = pd.read_csv(path)
# Find the list of unique cities where matches were played
matches_city= df['city'].unique()
print("Cities matches were played : {}".format(matches_city))
# Find the columns which contains null values if any ?
print(df.columns[df.isnull().values.any()])
# List down top 5 most played venues
df_unique_matches= df.drop_duplicates('match_code')
venues_top5= df_unique_matches['venue'].value_counts().nlargest(5)
print(venues_top5)
# Make a runs count frequency table
print(df['runs'].value_counts())
# How many seasons were played and in which year they were played 
df_unique_matches['year'] = pd.DatetimeIndex(df_unique_matches['date']).year
print('{}seasons were played'.format(len(df_unique_matches['year'].unique())) )
# No. of matches played per season
print(df_unique_matches['year'].value_counts())
# Total runs across the seasons
df['year']= pd.DatetimeIndex(df['date']).year
print(df.groupby('year').agg({'runs':'sum'}))
# Teams who have scored more than 200+ runs. Show the top 10 results
runs_per_team_per_match=df.groupby(['match_code','batting_team']).agg({'runs':'sum'})
print(runs_per_team_per_match[runs_per_team_per_match['runs']>200])
# What are the chances of chasing 200+ target
high_scores=df.groupby(['match_code', 'inning','team1','team2'])['total'].sum().reset_index() 

high_scores = high_scores[high_scores['total'] >= 200]

high_scores1 = high_scores[high_scores['inning']==1]

high_scores2 = high_scores[high_scores['inning']==2]

high_scores1=high_scores1.merge(high_scores2[['match_code','inning', 'total']], on='match_code')

high_scores1.rename(columns={'inning_x':'inning_1','inning_y':'inning_2','total_x':'inning1_runs','total_y':'inning2_runs'},inplace=True)

high_scores1=high_scores1[high_scores1['inning1_runs']>=200]

high_scores1['is_score_chased']=1

high_scores1['is_score_chased'] = np.where(high_scores1['inning1_runs']<=high_scores1['inning2_runs'], 'yes', 'no')

chances = high_scores1['is_score_chased'].value_counts()

print('The chances of chasing a target of 200+ in 1st innings are : \n' , chances[1]/14*100)



# Which team has the highest win count in their respective seasons ?
print(df_unique_matches.groupby(['year','winner']).agg({'winner':'max'}))


