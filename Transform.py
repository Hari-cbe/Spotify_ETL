import Extract
import pandas as pd 


def DataQuaityCheck(load_df):

    if load_df.empty:
        print("No Data Found")
        return False
    
    if pd.Series(load_df["song"]).is_unique:
        pass 
    else:
        raise Exception("Found Duplicates")

    if load_df.isnull().values.any():
        raise Exception("Found Null Values ")

def TransformData(load_df):

    # Rename columns 
    load_df.rename(columns={"album_name":"Album",
                            "song": "Song",
                            "artists" : "Artists",
                            "duration": "Duration"},inplace=True)
    
    #Tranforming list to string
    load_df["Artists"] = load_df["Artists"].str.join(", ") 

    # Creating Artists DF
    artists_df = pd.DataFrame(load_df["Artists"])

    artists_df = artists_df.explode("Artists").drop_duplicates()
    artists_df['Artist_ID'] = range(len(artists_df))
    
    artists_df = artists_df[["Artist_ID","Artists"]]

    return load_df, artists_df


if __name__ == "__main__":
    load_df = Extract.return_df()
    DataQuaityCheck(load_df)
    TransformData(load_df)