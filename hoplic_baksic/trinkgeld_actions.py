from cProfile import label

import pandas as pd
import chardet
import re
import customtkinter as ctk
from tabulate import tabulate
from tkinterdnd2 import DND_FILES, TkinterDnD

class TrinkgeldActions(ctk.CTkFrame,TkinterDnD.DnDWrapper):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
        self.path_csv_lists = []

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)

        #Drag and Drop

        self.file_frame = ctk.CTkScrollableFrame(self, width=int(window_width/4), height=int(window_height/5))
        self.file_frame.pack(pady=10)

        label = ctk.CTkLabel(self, text="Drag file here", font=("Arial", 14))
        label.pack(expand=True)

        drop_frame = ctk.CTkFrame(self,width=int(window_width / 2),height=int(window_height / 4),corner_radius=10)
        drop_frame.pack(pady=60)

        # Text box
        df = self.load_and_clean_csv_data(
            "data/Detailexport.csv")  # Reads a CSV file with automatic encoding detection,and cleans the column names.
        daily_amount = self.display_and_clean_daily_tip(
            "data/export.csv")  # Reads and cleans a daily tip amount from a tab-delimited file.
        textbox = ctk.CTkTextbox(self, width=window_width, height=window_height, font=("Courier New", 10),
                                 wrap="none")
        textbox.pack(side="top", fill="both", expand=True)

        # vertical scroll
        v_scroll = ctk.CTkScrollbar(self, orientation="vertical", command=textbox.yview)
        v_scroll.pack(side="right", fill="y")

        # horizontal scroll
        h_scroll = ctk.CTkScrollbar(self, orientation="horizontal", command=textbox.xview)
        h_scroll.pack(side="bottom", fill="x")

        # connecting them
        textbox.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        data = self.extract_confirmed_work_hours(
            df)  # Extracts and organizes confirmed working hours per person by date.
        new_list_perso = self.clean_list_data(
            data)  # Converts a nested dictionary of data into a sorted DataFrame and adds a summary row.
        hourly_tips = self.get_hourly_tip(new_list_perso,
                                          daily_amount)  # This script calculates the ratio between daily tips and hourly totals for a specific day.
        calculation = self.calculation_merging_two_lists(new_list_perso,
                                                         hourly_tips)  # Merges a DataFrame of worked hours with hourly tip values and calculates total earnings per worker

        c = pd.DataFrame(calculation)
        formatted_df = tabulate(c, headers='keys', tablefmt='grid', showindex=True)  # floatfmt=".2f"
        textbox.insert("0.00", formatted_df)

        drop_frame.drop_target_register(DND_FILES)
        drop_frame.dnd_bind("<<DropEnter>>",self.on_drag_enter)
        drop_frame.dnd_bind("<<DropLeave>>",self.on_drag_leave)
        drop_frame.dnd_bind("<<Drop>>",self.display_file_path)

    def on_drag_enter(self,event):
        self.configure(fg_color="#a6dcef")
        return event.action

    def on_drag_leave(self,event):
        self.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        return event.action

    def handle_drop(self):
        pass

    def display_file_path(self,event):
        dropped_file = event.data.replace("{","").replace("}","")
        #read = pd.read_csv(dropped_file,delimiter=";")
        #l = int(len(read))


        if dropped_file:
            self.path_csv_lists.append(dropped_file)

        for path in self.path_csv_lists:
            ctk.CTkLabel(self.file_frame, text=f"{path}", anchor="w").pack(fill="x", padx=10, pady=1)

        new_list = list(dict.fromkeys(self.path_csv_lists))

        return new_list#Duplikati se pojavljuju

    def load_and_clean_csv_data(self,filepath,delimiter=";"):
        with open(filepath,"rb") as f:
            rawdata = f.read(10000)
            result = chardet.detect(rawdata)
            encoding = result["encoding"]

        df = pd.read_csv(filepath,delimiter=delimiter,encoding=encoding)
  
        def clean_colums(col):
            col = col.strip()                  
            col = re.sub(r'\ufeff', '', col)   
            col = re.sub(r'[\W]', '', col)
            col = col.lower()                  
            return col

        df.columns =  [clean_colums(c) for c in df.columns]

        return df


    def extract_confirmed_work_hours(self,data):
        df_subset = data[["tag","vorname","typ","dauerbruttodezimal","arbeitsbereich"]] #Taking only four needed rows
        hours_liste = df_subset.values.tolist() #Putting all data in the list

        perso = {}

        for row in hours_liste:
            tag = row[0]
            vorname = row[1]
            typ = row[2]
            dauer_brutto = row[3]
            arbeitsbereich = row[4]

            if typ == "Bestätigte Arbeitszeit" and arbeitsbereich == "Barista":
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


    def clean_list_data(self,data):
        new_list = pd.DataFrame.from_dict(data,orient="index").fillna(0)
        new_list = new_list.sort_index()
        new_list = new_list[sorted(new_list.columns)]
        new_list.loc["SUM"] = new_list.sum(numeric_only=True).fillna(0)

        return new_list


    def display_and_clean_daily_tip(self,data):
        with open(data) as tip_amount_list:
            daily_tip_amount = pd.read_csv(tip_amount_list,delimiter="\t",nrows=1)
            daily_tip_amount = daily_tip_amount.map(lambda x:x.replace('â‚¬', '').replace(",",".").strip() if isinstance(x,str) else x)

            def clean_colums(col):
                col = re.sub(r'\ufeff', '', col)

                return col

        daily_tip_amount.columns =  [clean_colums(c) for c in daily_tip_amount.columns]

        return daily_tip_amount


    def get_hourly_tip(self,hour,daily_tip): 
            tips = daily_tip.iloc[0].fillna(0)
            sume = hour.iloc[-1].fillna(0)

            tips = tips.drop(['Bezeichnung', 'Zeitraum'])

            sume = sume.fillna(0)
            tips = tips.fillna(0)

            all_together = sume.index.intersection(tips.index)
            
            sume = sume.loc[all_together].astype(float)
            tips = tips.loc[all_together].astype(float)
        
            score = tips/sume

            return score

    def calculation_merging_two_lists(self,list_of_worked_hours_and_workers,hourly_tips_on_day):
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

            mask = (new_list[col] > 0) & (new_list.index != "tips")
            
            new_list.loc[mask,col] = new_list.loc[mask,col] * last_value

        if "tips" in new_list.index:
            new_list = new_list.drop("tips",axis=0)
        else:
            new_list = new_list.copy()

        new_list["TRINKGELD"] = new_list.sum(axis=1,numeric_only=True).round(2)
        new_list["TRINKGELD"] = new_list.iloc[:,-1]
        cols = ['TRINKGELD'] + [col for col in new_list.columns if col != 'TRINKGELD']
    
        new_list = new_list.sort_index()
        new_list = new_list[sorted(new_list.columns)]
        new_list.loc["SUM"] = new_list.sum(numeric_only=True).fillna(0)

        return new_list[cols]