import tkinter as tk
from tkinter import font, IntVar, Radiobutton, ttk, BOTH, Menu, StringVar
import sys
sys.path.append('./')
from Algorithm_final_Adjust_test_una import run
import tkinter.messagebox as messagebox
import numpy as np


def submit():
    # 獲取用戶輸入的數值和選項
    try:
        days_queens = int(day_queens_var.get())
        days_bronx = int(day_bronx_var.get())
        days_manhattan = int(day_manhattan_var.get())
        days_brooklyn = int(day_brooklyn_var.get())
        days_staten_island = int(day_staten_island_var.get())

        day_lst = [days_queens, days_bronx, days_manhattan, days_brooklyn, days_staten_island]
        # 計算總天數
        total_days = days_queens + days_bronx + days_manhattan + days_brooklyn + days_staten_island

        budget_total = int(total_budget_var.get())
        budget_attractions = int(budget_attractions_var.get())
        budget_restaurants = int(budget_restaurants_var.get())
        budget_accommodation = int(budget_accommodation_var.get())

        preference = preference_combobox.get()

        result = run(budget_total, budget_attractions, budget_restaurants, budget_accommodation, day_lst, preference, total_days)
        
        if len(result) > 1:
            fare, Queenshoteloutput, Bronxhoteloutput, Manhattanhoteloutput, Brooklynhoteloutput, StatenIslandhoteloutput, schedule = result
            # 在此處執行提交操作，可以調用後端的函數或進行其他處理
            return total_days, fare, Queenshoteloutput, Bronxhoteloutput, Manhattanhoteloutput, Brooklynhoteloutput, StatenIslandhoteloutput, schedule
    
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter valid values <3")


root = tk.Tk()
root.title("Welcome to T.A.I.N.")

style = ttk.Style()
# root = ThemedTk(theme="clearlooks")
style.theme_use("aqua")  # 應用主題
# style.configure('FLORA', background='floralwhite')

root.configure(bg="floralwhite")


# 創建標籤
title_font = font.Font(family='Times', size=20, weight="bold")
title_label = tk.Label(root, text="Your Tourist Assistant in NYC!", font=title_font, background='floralwhite')
title_label.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")

#停留天數
budget_font = font.Font(family='Georgia', size=14, weight="bold")
budget_label = tk.Label(root, text="Budget", font=budget_font, background='floralwhite')
budget_label.grid(row=1, column=0, columnspan=5, pady=0)

# 預算輸入格式說明
description_font = font.Font(family='Times', size=12, weight="normal", slant="italic")
description_label = tk.Label(root, text="*Please enter your budget and allocate it. \n*The percentages should add up to one hundred.", font=description_font, justify='left', background='floralwhite')
description_label.grid(row=2, column=0, padx=10)


# 總預算輸入
total_budget_label = tk.Label(root, text="Total Budget (in NTD):", font=("Georgia", 12), background='floralwhite')
total_budget_label.grid(row=3, column=0, padx=10)
total_budget_var = tk.Entry(root, width=5)
total_budget_var.insert(0, "0")
total_budget_var.grid(row=3, column=1, padx=10)
total_budget_var.configure(highlightbackground='floralwhite')

# 景點預算
budget_attractions_label = tk.Label(root, text="Attractions:", font=("Georgia", 12), background='floralwhite')
budget_attractions_label.grid(row=4, column=0, padx=10)

budget_attractions_var = tk.StringVar()
budget_attractions_entry = tk.Entry(root, textvariable=budget_attractions_var, width=5)
budget_attractions_entry.grid(row=4, column=1, padx=10)
budget_attractions_entry.configure(highlightbackground='floralwhite')

percentage_label = tk.Label(root, text="%", font=("Georgia", 12), background='floralwhite')
percentage_label.grid(row=4, column=2)

# 餐廳預算
budget_restaurants_label = tk.Label(root, text="Restaurants:", font=("Georgia", 12), background='floralwhite')
budget_restaurants_label.grid(row=5, column=0, padx=10)

budget_restaurants_var = tk.StringVar()
budget_restaurants_entry = tk.Entry(root,textvariable=budget_restaurants_var, width=5)
budget_restaurants_entry.grid(row=5, column=1, padx=10)
budget_restaurants_entry.configure(highlightbackground='floralwhite')

percentage_label = tk.Label(root, text="%", font=("Georgia", 12), background='floralwhite')
percentage_label.grid(row=5, column=2)

# 住宿預算
budget_accommodation_label = tk.Label(root, text="Accommodation:", font=("Georgia", 12), background='floralwhite')
budget_accommodation_label.grid(row=6, column=0, padx=10)

budget_accommodation_var = tk.StringVar()
budget_accommodation_entry = tk.Entry(root, textvariable=budget_accommodation_var, width=5)
budget_accommodation_entry.grid(row=6, column=1, padx=10)
budget_accommodation_entry.configure(highlightbackground='floralwhite')

percentage_label = tk.Label(root, text="%", font=("Georgia", 12), background='floralwhite')
percentage_label.grid(row=6, column=2)

#停留天數
stay_label = tk.Label(root, text="Duration of Stay", font=budget_font, background='floralwhite')
stay_label.grid(row=7, column=0, columnspan=5, pady=10)

# 停留天數的輸入格式說明
description_label = tk.Label(root, text="*Adjust days per region using the arrows below.\n*The maximum value is three days.", font=description_font, justify='left', background='floralwhite')
description_label.grid(row=8, column=0, padx=10)

# 皇后區
day_queens_label = tk.Label(root, text="Queens:", font=("Georgia", 12), background='floralwhite')
day_queens_label.grid(row=9, column=0, padx=0)
day_queens_var = tk.IntVar(root, value=0)
day_queens_entry = tk.Spinbox(root, from_=0, to=3, textvariable=day_queens_var, width=5)
day_queens_entry.grid(row=9, column=1, padx=10)
day_queens_entry.configure(highlightbackground='floralwhite')

# 布朗克斯區
day_bronx_label = tk.Label(root, text="Bronx:", font=("Georgia", 12), background='floralwhite')
day_bronx_label.grid(row=10, column=0, padx=10)
day_bronx_var = tk.IntVar(root, value=0)
day_bronx_entry = tk.Spinbox(root, from_=0, to=3, textvariable=day_bronx_var, width=5)
day_bronx_entry.grid(row=10, column=1, padx=10)
day_bronx_entry.configure(highlightbackground='floralwhite')

# 曼哈頓區
day_manhattan_label = tk.Label(root, text="Manhattan:", font=("Georgia", 12), background='floralwhite')
day_manhattan_label.grid(row=11, column=0, padx=10)
day_manhattan_var = tk.IntVar(root, value=0)
day_manhattan_entry = tk.Spinbox(root, from_=0, to=3, textvariable=day_manhattan_var, width=5)
day_manhattan_entry.grid(row=11, column=1, padx=10)
day_manhattan_entry.configure(highlightbackground='floralwhite')

# 布魯克林區
day_brooklyn_label = tk.Label(root, text="Brooklyn:", font=("Georgia", 12), background='floralwhite')
day_brooklyn_label.grid(row=12, column=0, padx=10)
day_brooklyn_var = tk.IntVar(root, value=0)
day_brooklyn_entry = tk.Spinbox(root, from_=0, to=3, textvariable=day_brooklyn_var, width=5)
day_brooklyn_entry.grid(row=12, column=1, padx=10)
day_brooklyn_entry.configure(highlightbackground='floralwhite')

# 史丹頓島區
day_staten_island_label = tk.Label(root, text="Staten Island:", font=("Georgia", 12), background='floralwhite')
day_staten_island_label.grid(row=13, column=0, padx=10)
day_staten_island_var = tk.IntVar(root, value=0)
day_staten_island_entry = tk.Spinbox(root, from_=0, to=3, textvariable=day_staten_island_var, width=5)
day_staten_island_entry.grid(row=13, column=1, padx=10)
day_staten_island_entry.configure(highlightbackground='floralwhite')

# 創建偏好標籤
preference_label = tk.Label(root, text="Preference", font=budget_font, background='floralwhite')
preference_label.grid(row=14, column=0, columnspan=5, pady=10)
preference_label.configure(highlightbackground='floralwhite')

# 偏好選擇的說明
description_label = tk.Label(root, text="*Please enter your sorting preference.", font=description_font, justify='left', anchor='w', background='floralwhite')
description_label.grid(row=15, column=0, padx=10)
description_label.configure(highlightbackground='floralwhite')

# 創建偏好選項變量
preference_var = IntVar()

# 創建Radiobuttons
preference_combobox = ttk.Combobox(root, textvariable=preference_var, state="readonly")
preference_combobox["values"] = ("分數", "評論數", "人氣指數")
preference_combobox.grid(row=18, column=0, columnspan=5)
preference_combobox.configure(background="floralwhite")
preference_combobox.current(0)  # 設置默認選擇項

# result 接住輸入結果
def on_submit():
    result = submit()
    schedule = result[-1]
    fare = result[1]
    total_days = result[0]
    Queenshoteloutput = result[2]
    Bronxhoteloutput = result[3]
    Manhattanhoteloutput = result[4]
    Brooklynhoteloutput = result[5]
    StatenIslandhoteloutput = result[6]
    print(schedule)

    # 創建"Schedule"窗口
    schedule_window = tk.Toplevel(root)
    schedule_window.title("Schedule")
    schedule_window.configure(bg="floralwhite")

    def get_list_by_day():
        selected_option = schedule_combobox.get()
        def clear_schedule_window():
            # Clear the schedule window
            for widget in schedule_window.grid_slaves():
                if widget != schedule_combobox and widget != fare_label and widget != fare_value_label:
                    widget.grid_forget()

        if selected_option == "Recommended Accomodations":
            clear_schedule_window()
            
            region_title = ['Queens', 'Bronx', 'Manhattan', 'Brooklyn', 'Staten Island']
            hotel_recs = [Queenshoteloutput, Bronxhoteloutput, Manhattanhoteloutput, Brooklynhoteloutput, StatenIslandhoteloutput]

            for i in range(5):
                region_subtitle = tk.Label(schedule_window, text=region_title[i], font=("Georgia", 16, "bold"), background='floralwhite')
                region_subtitle.grid(row=i*4+3, column=0, sticky="w")

                # if hotel_recs[i] == None or hotel_recs[i] == 'None' or hotel_recs[i] == []:
                #     no_match_label = tk.Label(schedule_window, text="No Matched Accommodation!", font=("Arial", 12))
                #     no_match_label.grid(row=i*4+4, column=0, sticky="w")
                row_counter = 0
                if hotel_recs[i] == []:
                    not_scheduled_label = tk.Label(schedule_window, text="Not in your schedule!", font=("Georgia", 12, "italic"), background='floralwhite')
                    not_scheduled_label.grid(row=i*4+4, column=0, sticky="w")
                elif hotel_recs[i][0] == None:
                    no_match_label = tk.Label(schedule_window, text="No Matched Accommodation! Please increase your accommodation budget!\nFor accommodation in New York, a recommended budget range starts from at least $4000-7000 per night.", font=("Georgia", 12, "italic"), background='floralwhite', anchor='w')
                    no_match_label.grid(row=i*4+4, column=0, sticky="w")
                    blank_label = tk.Label(schedule_window, text="")
                    blank_label.grid_forget()
                else:
                    
                    for j in range(0, len(hotel_recs[i]), 2):
                        hotel_name = tk.Label(schedule_window, text=hotel_recs[i][j], font=("Georgia", 12), background='floralwhite')
                        hotel_name.grid(row=i*4+4+row_counter, column=0, sticky="w")

                        hotel_price_text = str(hotel_recs[i][j + 1])
                        if j in [0, 2, 4]:
                            hotel_price_text = "$" + hotel_price_text

                        hotel_price = tk.Label(schedule_window, text=hotel_price_text, font=("Georgia", 12), background='floralwhite')
                        hotel_price.grid(row=i*4+4+row_counter, column=3, sticky="w")

                        row_counter += 1

        # 空出一列
                blank_label = tk.Label(schedule_window, text="")
                blank_label.grid(row=i*4+4+row_counter, column=0)



        else:
            subtitle_lable = tk.Label(schedule_window, text='Attractions/Restaurants', font=("Georgia", 12, "bold"), background='floralwhite')
            subtitle_lable.grid(row=2, column=0, columnspan=5, pady=10, sticky="w")

            subtitle_lable2 = tk.Label(schedule_window, text='Estimate Price', font=("Georgia", 12, "bold"), background='floralwhite')
            subtitle_lable2.grid(row=2, column=1, columnspan=5, pady=10, sticky="w")

            schedule_label = tk.Label(schedule_window, text="")
            schedule_label.grid(row=1, column=0)
            selected_option = schedule_combobox.get()
            index = int(selected_option[3:]) - 1  # Extract the number part from the index and subtract 1 to match the list index
            if 0 <= index < len(schedule):

                day_schedule = schedule[index]
                # 清空先前的行程
                for widget in schedule_window.grid_slaves():
                    if widget != schedule_combobox and widget != fare_label and widget != fare_value_label and widget != subtitle_lable and widget != subtitle_lable2:
                        widget.grid_forget()
                        
                schedule_window.columnconfigure(0, weight=1)
                schedule_window.columnconfigure(1, weight=1)
                # 顯示選定的行程
                for i, schedule_item in enumerate(day_schedule):
                    if i % 2 == 0:
                        # 雙數項目向左對齊
                        if schedule_item == None and i in (2, 6, 10):
                            schedule_label = tk.Label(schedule_window, text="No matched restsurant! Please increase your food budget!", anchor='w', font=('Georgia', 12, 'italic'))
                            schedule_label.grid(row=i + 3, column=0, sticky='w')
                            schedule_label.configure(background='floralwhite')
                        elif schedule_item == None and i in (0, 4, 8):
                            schedule_label = tk.Label(schedule_window, text="No matched attraction! Please increase your attraction budget!", anchor='w', font=('Georgia', 12, 'italic'))
                            schedule_label.grid(row=i + 3, column=0, sticky='w')
                            schedule_label.configure(background='floralwhite')
                        else:
                            schedule_label = tk.Label(schedule_window, text=schedule_item, anchor='w', font='Georgia')
                            schedule_label.grid(row=i + 3, column=0, sticky='w')
                            schedule_label.configure(background='floralwhite')
                    else:
                        if schedule_item == None:
                            schedule_label = tk.Label(schedule_window, text="", anchor='e')
                            schedule_label.grid(row=i + 2, column=1,sticky='w')
                            schedule_label.configure(background='floralwhite')
                        else:
                        # 單數項目向右對齊
                            schedule_label = tk.Label(schedule_window, text="$" + str(schedule_item), anchor='e', font='Georgia')
                            schedule_label.grid(row=i + 2, column=1,sticky='w')
                            schedule_label.configure(background='floralwhite')
            else:
                schedule_label = tk.Label(schedule_window, text="Invalid day.", font='Georgia')
                schedule_label.grid(row=i + 1, column=0)
                schedule_label.configure(background='floralwhite')

    fare_label = tk.Label(schedule_window, text="Transportation expenses in total:", font='Georgia')
    fare_label.grid(row=0, column=0, sticky="w")
    fare_label.configure(background='floralwhite')

    fare_value_label = tk.Label(schedule_window, text="$" + str(fare), font='Georgia') # add a $ sign
    fare_value_label.grid(row=0, column=1, sticky="w")
    fare_value_label.configure(background='floralwhite')




    schedule_combobox = ttk.Combobox(schedule_window, state="readonly")
    schedule_combobox.grid(row=1, column=0, columnspan=8)

    schedule_combobox["values"] = ["Recommended Accomodations"] + [f"Day{i}" for i in range(1, total_days + 1)]
    schedule_combobox.bind("<<ComboboxSelected>>", lambda event: get_list_by_day())

# 創建提交按鈕
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=19, column=0, columnspan=5, pady=10)
submit_button.configure(highlightbackground='floralwhite')


root.mainloop()
