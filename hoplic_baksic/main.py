import pandas as pd
import chardet
import re
import customtkinter as ctk
#from tkinterdnd2 import DND_FILES, TkinterDnD

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

def clean_list_data(data):
    """
        Converts a nested dictionary of data into a sorted DataFrame.

        This function:
        - Converts the input dictionary (e.g., {name: {date: hours}}) to a pandas DataFrame.
        - Sorts the rows by index (e.g., names) and columns (e.g., dates).
        - Adds a new row labeled "SUM" containing the column-wise sum of numeric values.

        Parameters:
            data (dict): Nested dictionary with structure {key: {subkey: value}}, typically representing
                         {person: {date: hours}}
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

def get_hourly_tip(hour,daily_tip): 
       
        '''
        This script calculates the ratio between daily tips and hourly totals for a specific day.

            Steps:
            1. Select the first row from the `daily_tip` DataFrame and replace missing values with 0.
            2. Select the 23rd row (index 22) from the `hour` DataFrame and also replace missing values with 0.
            3. Remove non-numeric or irrelevant columns ('Bezeichnung', 'Zeitraum') from the tips data.
            4. Ensure all remaining missing values in both Series are replaced with 0.
            5. Identify the common columns (indexes) shared between both Series.
            6. Filter both Series to only include these common columns and convert the data to float.
            7. Compute the ratio (score) of tips to hourly values for each common column.
            8. Print the resulting ratio.

        The final output is a Series showing the relative amount of tips per total hourly sum for each shared category.
        '''
        tips = daily_tip.iloc[0].fillna(0)
        sume = hour.iloc[22].fillna(0)
        tips = tips.drop(['Bezeichnung', 'Zeitraum'])
        sume = sume.fillna(0)
        tips = tips.fillna(0)
        all_together = sume.index.intersection(tips.index)
        sume = sume.loc[all_together].astype(float)
        tips = tips.loc[all_together].astype(float)
        score = tips/sume
        return score


def calculation_merging_two_lists(list_of_worked_hours_and_workers,hourly_tips_on_day):
    '''
        Merges a DataFrame of worked hours with hourly tip values and calculates total earnings per worker.

        Parameters:
        - list_of_worked_hours_and_workers (pd.DataFrame): A DataFrame where rows represent workers and columns represent hours worked. 
          If a "SUM" row is present, it will be excluded before processing.
        - hourly_tips_on_day (list or pd.Series): A list or Series containing tip values per hour for each column.

        Process:
        1. Removes the "SUM" row from the input DataFrame if it exists, to avoid duplicating totals.
        2. Adds a temporary "tips" row with the hourly tip values.
        3. For each column (i.e., hour), multiplies all values greater than 0 (excluding the "tips" row)
           by the tip value from the "tips" row.
        4. Removes the "tips" row after applying the multiplication.
        5. Adds a new "SUM" row that contains the column-wise totals.
        6. Adds a new "TRINKGELD" column (German for "tip") that contains row-wise totals (left to right), rounded to 2 decimals.

        Returns:
        - A new DataFrame with updated earnings per worker and overall summaries.
    '''
    if "SUM" in list_of_worked_hours_and_workers.index:
        new_list = list_of_worked_hours_and_workers.drop("SUM",axis=0)
    else:
        new_list = list_of_worked_hours_and_workers.copy()

    if isinstance(hourly_tips_on_day,list):
        assert len(hourly_tips_on_day) == len(new_list.columns)
        new_list.loc["tips"] = hourly_tips_on_day
    elif isinstance(hourly_tips_on_day,pd.Series):
        new_list.loc["tips"] = hourly_tips_on_day

    new_list = new_list.copy()

    for col in new_list.columns:
        last_value = new_list[col].iloc[-1]

        mask = (new_list[col] > 0) & (new_list.index != new_list.index[-1])

        new_list.loc[mask,col] = new_list.loc[mask,col] * last_value

    if "tips" in new_list.index:
        new_list = new_list.drop("tips",axis=0)
    else:
        new_list = new_list.copy()

    
    new_list.loc["SUM"] = new_list.sum(numeric_only=True).fillna(0)
    new_list["TRINKGELD"] = new_list.sum(axis=1,numeric_only=True).round(2)

    return new_list

df = load_and_clean_csv_data("data/Detailexport.csv") #Reads a CSV file with automatic encoding detection, and cleans the column names.
data = extract_confirmed_work_hours(df)#Extracts and organizes confirmed working hours per person by date.
new_list_perso = clean_list_data(data)#Converts a nested dictionary of data into a sorted DataFrame and adds a summary row.
daily_amount = display_and_clean_daily_tip("data/export.csv")#Reads and cleans a daily tip amount from a tab-delimited file.
hourly_tips = get_hourly_tip(new_list_perso,daily_amount)#This script calculates the ratio between daily tips and hourly totals for a specific day.
calculation = calculation_merging_two_lists(new_list_perso,hourly_tips)#Merges a DataFrame of worked hours with hourly tip values and calculates total earnings per worker


#Customtkinter classes
class App(ctk.CTk):
    def __init__(self,):
        super().__init__()
        self.title("\U0001F601")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)

        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        #main grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        #sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)  # za odvajanje donjih dugmadi

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="App",font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home",command=self.show_home)
        self.home_button.grid(row=1, column=0, padx=20, pady=10)

        self.settings_button = ctk.CTkButton(self.sidebar_frame, text="Settings",command=self.show_settings)
        self.settings_button.grid(row=2, column=0, padx=20, pady=10)
        
        self.settings_button = ctk.CTkButton(self.sidebar_frame, text="Main",command=self.show_main_page)
        self.settings_button.grid(row=4, column=0, padx=20, pady=10)

        #main content
        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        self.main_content.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        #intial page
        self.show_home()
    
    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_main_content()
        label = ctk.CTkLabel(self.main_content, text="Welcome to the Home Page!", font=("Arial", 18))
        label.grid(row=0, column=0, padx=20, pady=20)
    
    def show_settings(self):
        self.clear_main_content()
        label = ctk.CTkLabel(self.main_content, text="Settings Page", font=("Arial", 18))
        label.grid(row=0, column=0, padx=20, pady=20)
    
    def show_main_page(self):
        self.clear_main_content()
        label = ctk.CTkLabel(self.main_content, text="Main Page", font=("Arial", 18))
        label.grid(row=0, column=0, padx=20, pady=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()