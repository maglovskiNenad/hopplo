import pandas as pd
import chardet
import re


def load_and_clean_csv_data(filepath,delimiter=";"):
    """""
    Reads a CSV file with automatic encoding detection, and cleans the column names.

        This function:
        - Detects the file's character encoding using the `chardet` library.
        - Reads the CSV file into a pandas DataFrame using the detected encoding.
        - Cleans column names by:
            - Removing leading and trailing whitespace.
            - Removing any non-alphanumeric characters (including BOM markers).
            - Converting all column names to lowercase.

        Parameters:
            filepath (str): Path to the CSV file.
            delimiter (str, optional): Delimiter used in the CSV file. Default is ';'.

        Returns:
            pandas.DataFrame: A DataFrame with cleaned column names and loaded data.
    """
    with open(filepath,"rb") as f:
        rawdata = f.read(10000)
        result = chardet.detect(rawdata)
        encoding = result["encoding"]

    df = pd.read_csv(filepath,delimiter=delimiter,encoding=encoding)
    
    def clean_colums(col):
        col = col.strip()                  
        col = re.sub(r'\ufeff', '', col)   
        col = re.sub(r'[^\w]', '', col)    
        col = col.lower()                  
        return col
    
    df.columns =  [clean_colums(c) for c in df.columns]

    return df


def extract_confirmed_work_hours(data):
    """
       Extracts and organizes confirmed working hours per person by date.

        This function:
        - Selects relevant columns from the input DataFrame: "tag", "vorname", "typ", and "dauerbruttodezimal".
        - Filters rows where the work type ("typ") is "Bestätigte Arbeitszeit" (confirmed working time).
        - Converts the "dauerbruttodezimal" column to float, handling comma decimal separators.
        - Organizes the data into a nested dictionary structure: {person: {date: hours}}.

        Parameters:
            data (pandas.DataFrame): A DataFrame containing at least the required columns.

        Returns:
            dict: A dictionary mapping each person's name to their working hours per date.
    """
    df_subset = data[["tag","vorname","typ","dauerbruttodezimal"]] #Taking only four needed rows
    hours_liste = df_subset.values.tolist() #Putting all data in the list
    
    perso = {}

    for row in hours_liste:
        tag = row[0]
        vorname = row[1]
        typ = row[2]
        dauer_brutto = row[3]

        if typ == "Bestätigte Arbeitszeit":
            try:
                dauer_brutto = float(str(dauer_brutto).replace(",", "."))
            except:
                dauer_brutto = 0.0

            try:
                tag_dt = pd.to_datetime(tag, dayfirst=True, errors='coerce')
                tag_short = tag_dt.strftime('%d.%m.')
            except:
                tag_short = str(tag)[:6] + "."

            if vorname not in perso:
                perso[vorname] = {}
            perso[vorname][tag_short] = dauer_brutto
    return perso


def adding_new_sum_row(data):
    """
        Converts a nested dictionary of data into a sorted DataFrame and adds a summary row.

        This function:
        - Converts the input dictionary (e.g., {name: {date: hours}}) to a pandas DataFrame.
        - Sorts the rows by index (e.g., names) and columns (e.g., dates).
        - Adds a new row labeled "SUM" containing the column-wise sum of numeric values.

        Parameters:
            data (dict): Nested dictionary with structure {key: {subkey: value}}, typically representing
                         {person: {date: hours}}.

        Returns:
            pandas.DataFrame: A sorted DataFrame with a new summary row at the bottom.
    """
    new_list = pd.DataFrame.from_dict(data,orient="index").fillna(0)
    new_list = new_list.sort_index()
    new_list = new_list[sorted(new_list.columns)]
    new_list.loc["SUM"] = new_list.sum(numeric_only=True).fillna(0)
    
    return new_list

def display_and_clean_daily_tip(data):
    """
    Reads and cleans a daily tip amount from a tab-delimited file.

        This function:
        - Opens a tab-delimited text or CSV file containing daily tip data.
        - Reads only the first row using pandas (assuming the tip amount is in that row).
        - Cleans string values by:
            - Removing the '€' symbol (or its encoding artifact 'â‚¬').
            - Replacing commas with periods to standardize decimal notation.
            - Stripping any leading/trailing whitespace.
        - Cleans column names by removing special BOM characters.

        Parameters:
            data (str): Path to the tab-delimited file containing tip data.

        Returns:
            pandas.DataFrame: A one-row DataFrame with cleaned numeric values and column names.
    """
    with open(data) as tip_amount_list:
        daily_tip_amount = pd.read_csv(tip_amount_list,delimiter="\t",nrows=1)
        daily_tip_amount = daily_tip_amount.map(lambda x:x.replace('â‚¬', '').replace(",",".").strip() if isinstance(x,str) else x)


        def clean_colums(col):
            col = re.sub(r'\ufeff', '', col)
            return col

    daily_tip_amount.columns =  [clean_colums(c) for c in daily_tip_amount.columns]
    return daily_tip_amount

def meargin_two_lists(hour,daily_tip): 
        '''
        This function takes two inputs, hour and daily_tip, which appear to be pandas DataFrames.
            It extracts the first row from the daily_tip DataFrame and fills any missing values (NaN) with 0, storing this in tips.

            It extracts the 23rd row (index 22) from the hour DataFrame and also fills missing values with 0, storing this in suma.

            From the tips data, it drops the columns named 'Bezeichnung' and 'Zeitraum'.

            It ensures that both suma and the modified tips (stored in t) have no missing values by filling any remaining NaNs with 0.

            It finds the common indices (columns) between suma and t and keeps only those common indices for both.

            Both filtered series are converted to floats.

            Finally, it calculates the element-wise division of t by suma and prints the resulting series.

        '''       
        tips = daily_tip.iloc[0].fillna(0)
        suma = hour.iloc[22].fillna(0)
        tips = tips.drop(['Bezeichnung', 'Zeitraum'])

        suma = suma.fillna(0)
        tips = tips.fillna(0)

        zajednocko = suma.index.intersection(tips.index)

        suma = suma.loc[zajednocko].astype(float)
        tips = tips.loc[zajednocko].astype(float)

        rez = tips/suma
        print(rez)



       
    














df = load_and_clean_csv_data("data/Detailexport.csv") #Reads a CSV file with automatic encoding detection, and cleans the column names.
data = extract_confirmed_work_hours(df)#Extracts and organizes confirmed working hours per person by date.
new_list_perso = adding_new_sum_row(data)#Converts a nested dictionary of data into a sorted DataFrame and adds a summary row.
daily_amoutn = display_and_clean_daily_tip("data/export.csv")#Reads and cleans a daily tip amount from a tab-delimited file.



merged = meargin_two_lists(new_list_perso,daily_amoutn)

merged