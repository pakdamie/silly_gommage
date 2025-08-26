import pandas as pd
import numpy as np


def wrangle_demography_df(dem_df):
   
    """This cleans up the demographic data file downloaded to be in the 
    format that I wanted for a gommage
    """
    #Ensure that commas are removed so that the values can be
    #made numeric
    dem_df = dem_df.apply(lambda x: x.str.replace(',', ''))

    #Extract ages from the Age Group 
    dem_df[["start", "end"]] = dem_df["Age Group"].str.extract(r"(\d+)\s*to\s*(\d+)")
    dem_df.loc[dem_df["Age Group"] == "Under 5 years", ["start", "end"]] = [0, 4]
    dem_df.loc[dem_df["Age Group"] == "85 years and over", ["start", "end"]] = [85, 100]

    #Make numeric columns of the population size, start, end
    dem_df["Population"] = pd.to_numeric(dem_df["Population"], errors="coerce").fillna(0).astype(int)
    dem_df["start"] = pd.to_numeric(dem_df["start"], errors="coerce").fillna(0).astype(int)
    dem_df["end"] = pd.to_numeric(dem_df["end"], errors="coerce").fillna(0).astype(int)

    #Make a list for each group 
    age_list = []

    for index, row in dem_df.iterrows():
        start = row["start"]
        end = row["end"]
        total_pop_size = row["Population"]
        full_age = pd.DataFrame({"numbers": range(start, end + 1)})

        # Compute repeated population size
        pop_size_value = np.floor(total_pop_size / len(full_age))
        full_age["pop_size"] = [pop_size_value] * len(full_age)
        age_list.append(full_age)

        combined_age_df = pd.concat(age_list, ignore_index=True)

    #Beacuse we're going 100 to 0, it's a bit easier to order it by descending 
    combined_age_df  = combined_age_df.sort_values(by="numbers", ascending=False)
    #The cumulative population as it decreases
    combined_age_df["Cumulative"] = combined_age_df["pop_size"].sum() - np.cumsum(combined_age_df["pop_size"])

    new_row = pd.DataFrame({"numbers": [101], "pop_size": [ combined_age_df["pop_size"].sum()],
    "Cumulative": [ combined_age_df["pop_size"].sum()]})
    combined_age_df = pd.concat([new_row, combined_age_df ], ignore_index=True)


    return combined_age_df
