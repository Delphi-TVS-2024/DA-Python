
import customtkinter
import json
import glob, os

app = customtkinter.CTk()

height = '1920'
width = '1080'
app.geometry(height + 'x' + width)
app.configure(fg_color='#040D12')

IGNORE_LINE = ['Config', ]
LINES = []
FOLDER_PATH = 'E:/IIOT/'
TABLES = ['RawTable', 'CycleTime', 'Alarm', 'Loss', 'Tool', 'CTIndex','Alert' ]

for i in os.listdir(FOLDER_PATH):
    if len(i.split('.')) == 1 and i not in IGNORE_LINE:
        LINES.append(i)


tabview = customtkinter.CTkTabview(master=app)
tabview.pack(anchor='nw', padx=40, pady=40)
tabview.configure(fg_color='#183D3D', height=1300, width=1200)


def button_event(line):
    json_data = json.loads(open(FOLDER_PATH+line+'/Log_files/'+line + str('_visual.json')).read())
    print(json_data)
    for i in TABLES:
        folder_path = FOLDER_PATH + line + '/' + i

        csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
        globals()[line + '_' + i + str('_time_stamp')].configure(text=json_data[i][0])
        globals()[line + '_' + i + str('_req_count')].configure(text=json_data[i][1])
        globals()[line + '_' + i + str('que')].configure(text=len(csv_files))


def create_ui(line):
    globals()[line + '_update'] = customtkinter.CTkButton(tabview.tab(line), text="Update",
                                                          command=lambda: button_event(line), width=100)
    globals()[line + '_update'].place(x=1000, y=10)

    x = 40
    y = 40
    for i in TABLES:
        globals()[line + '_' + i + str('_table')] = customtkinter.CTkLabel(tabview.tab(line), text=i,
                                                                           fg_color="transparent",
                                                                           font=("Helvetica", 20, "bold"))
        globals()[line + '_' + i + str('_table')].place(x=x, y=y)
        globals()[line + '_' + i + str('_time_stamp')] = customtkinter.CTkLabel(tabview.tab(line),
                                                                                text="-",
                                                                                fg_color="transparent",
                                                                                font=("Helvetica", 20, "bold"))
        globals()[line + '_' + i + str('_time_stamp')].place(x=x + 200, y=y)
        globals()[line + '_' + i + str('_req_count')] = customtkinter.CTkLabel(tabview.tab(line), text="-",
                                                                               fg_color="transparent",
                                                                               font=("Helvetica", 20, "bold"))
        globals()[line + '_' + i + str('_req_count')].place(x=x + 500, y=y)

        globals()[line + '_' + i + str('que')] = customtkinter.CTkLabel(tabview.tab(line), text="-",
                                                                        fg_color="transparent",
                                                                        font=("Helvetica", 20, "bold"))
        globals()[line + '_' + i + str('que')].place(x=x + 650, y=y)
        y = y + 40


for i in LINES:
    tabview.add(i)
    create_ui(i)
app.mainloop()
