import pandas as pd
import chardet
import re
import customtkinter as ctk
from tabulate import tabulate
from tkinterdnd2 import DND_FILES, TkinterDnD
from warning_msg import WarningPopup
from config import WINDOW_WIDTH,WINDOW_HEIGHT
import pyautogui
from tkinter import filedialog

class TrinkgeldActions(ctk.CTkFrame,TkinterDnD.DnDWrapper):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
        self.path_csv_lists = []

        main_frame = ctk.CTkFrame(self,corner_radius=0,fg_color="#2e2e2e")
        main_frame.pack(fill="both", expand=True)

        self.file_frame = ctk.CTkScrollableFrame(main_frame, width=int(WINDOW_WIDTH / 5), height=int(WINDOW_HEIGHT / 9),border_width=1,border_color="gray")
        self.file_frame.pack(side="left",padx=(20,0),pady=20,anchor="n")

        right_frame = ctk.CTkFrame(main_frame,fg_color="#2e2e2e")
        right_frame.pack(side="left", fill="both", expand=True)

        drop_frame = ctk.CTkFrame(right_frame, width=int(WINDOW_WIDTH / 2), height=int(WINDOW_HEIGHT / 4),border_width=1,border_color="white",fg_color="#2e2e2e")
        drop_frame.pack(padx=10, pady=20, anchor="n")

        label = ctk.CTkLabel(drop_frame, text="Drop file here", font=("Arial", 14), text_color="white")
        label.place(relx=0.5, rely=0.5, anchor="center")

        self.textbox = ctk.CTkTextbox(self, width=int(WINDOW_WIDTH), height=int(WINDOW_HEIGHT),
                                 font=("Courier New", 10), wrap="none")

        ctk.CTkButton(main_frame, text="Delete list" , command=self.clear_file_list).pack(pady=20, padx=20)
        ctk.CTkButton(main_frame, text="Screenshoot", command=self.screenshot_widget).pack(pady=0, padx=0)

        drop_frame.drop_target_register(DND_FILES)
        drop_frame.dnd_bind("<<DropEnter>>",self.on_drag_enter)
        drop_frame.dnd_bind("<<DropLeave>>",self.on_drag_leave)
        drop_frame.dnd_bind("<<Drop>>",self.display_file_path)

    def screenshot_widget(self):
        self.update_idletasks()

        x = self.textbox.winfo_rootx()
        y = self.textbox.winfo_rooty()

        width = self.textbox.winfo_width()
        height = self.textbox.winfo_height()

        screenshoot = pyautogui.screenshot(region=(x,y,width,height))
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG file","*.png")],
            title="save screenshot",
        )

        if path:
            screenshoot.save(path)

    def clear_file_list(self):
        self.path_csv_lists.clear()

        for widget in self.file_frame.winfo_children():
            widget.destroy()

    def on_drag_enter(self,event):
        self.configure(fg_color="#a6dcef")
        return event.action

    def on_drag_leave(self,event):
        self.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        return event.action

    def handle_drop(self,new_list):
        if len(new_list) < 2:
            WarningPopup(self,message="Need more file...")
        elif len(new_list) > 2:
            WarningPopup(self, message="We have more files then we need.")
        elif len(new_list) == 2:
            for data_in_list in new_list:
                read_data = pd.read_csv(data_in_list,delimiter=";")
                if len(read_data) > 2:
                    df = self.load_and_clean_csv_data(data_in_list)
                elif len(read_data) == 2:
                    daily_amount = self.display_and_clean_daily_tip(data_in_list)

            data = self.extract_confirmed_work_hours(df)
            new_list_perso = self.clean_list_data(data)
            hourly_tips = self.get_hourly_tip(new_list_perso, daily_amount)
            calculation = self.calculation_merging_two_lists(new_list_perso, hourly_tips)

            self.textbox.pack(fill="both", expand=True, padx=15, pady=15)

            # vertical scroll
            v_scroll = ctk.CTkScrollbar(self, orientation="vertical", command=self.textbox.yview)
            v_scroll.pack(side="right", fill="y")

            # horizontal scroll
            h_scroll = ctk.CTkScrollbar(self, orientation="horizontal", command=self.textbox.xview)
            h_scroll.pack(side="bottom", fill="x")

            v_scroll.configure(command= self.textbox.yview) #textbox.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            h_scroll.configure(command= self.textbox.xview)

            # connecting them
            c = pd.DataFrame(calculation)
            formatted_df = tabulate(c, headers='keys', tablefmt='grid', showindex=True)  # floatfmt=".2f"
            self.textbox.insert("0.00", formatted_df)

            # Test panel for the "trinkgeld Tabelle"
            test_panel = pd.DataFrame(daily_amount)
            first_col_test_panel = test_panel.iloc[:, 1]
            formated_first_col_test_panel = pd.DataFrame({"TEST": first_col_test_panel})
            formated_test_panel = tabulate(formated_first_col_test_panel,headers='keys', tablefmt='grid',showindex=False)
            self.textbox.insert("0.00",formated_test_panel)

    def display_file_path(self,event):
        dropped_file = event.data.replace("{","").replace("}","")

        if dropped_file:
            self.path_csv_lists.append(dropped_file)

        new_list = list(dict.fromkeys(self.path_csv_lists))

        for widget in self.file_frame.winfo_children():
            widget.destroy()

        for path in new_list:
            ctk.CTkLabel(self.file_frame, text=f"{path}", anchor="w").pack(fill="x",padx=10, pady=1)

        new_list = list(dict.fromkeys(self.path_csv_lists))

        self.handle_drop(new_list)

        return new_list

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
        df_subset = data[["tag","vorname","typ","dauerbruttodezimal","arbeitsbereich"]]
        hours_liste = df_subset.values.tolist()

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