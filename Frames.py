import tkinter as tk
from tkinter import *
from tkinter import ttk 
from PIL import Image, ImageTk
import ttkbootstrap as ttkbootstrap
from ttkbootstrap.constants import *
import emoji
from datetime import datetime, timedelta
import json
import os
from tkinter import messagebox
from .classes import Job, Worker, Service

workers = []
services = []
jobs = []

root = tk.Tk()
root.geometry("%dx%d" % (root.winfo_screenwidth()/2.3, root.winfo_screenheight()))
root.config(background="white")
root.title("Carwash")
root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))

app = tk.Frame(root, padx=20, pady=20, bg="white")
app.pack(fill=tk.BOTH, expand=True)

# ========================================= FRAME 1 ==============================================
workers_frame = tk.Frame(app, padx=10, pady=10, bg="white")
workers_frame.grid(row=0, column=0, sticky="news")

workers_label_image = resize_image("workers-list-label.png", 250, 50)
worker_label = tk.Label(workers_frame, image=workers_label_image, borderwidth=0, highlightthickness=0, highlightbackground="white")
worker_label.grid(row=0, column=0, columnspan=2)

workers_listbox_scrollbar = tk.Scrollbar(workers_frame, orient=tk.VERTICAL)
workers_listbox = Listbox(workers_frame, background="white", fg="gray", width=25, yscrollcommand=workers_listbox_scrollbar.set, borderwidth=0, highlightthickness=0)

workers_listbox_scrollbar.config(command=workers_listbox.yview)
workers_listbox.grid(row=1, column=0, sticky=tk.NSEW)
workers_listbox_scrollbar.grid(row=1, column=1, sticky=tk.NS)

add_worker_btn = ttk.Button(workers_frame, text=f'{emoji.emojize(":sparkles:")} Add New Worker', command=add_worker)
add_worker_btn.grid(row=2, column=0, sticky="ew", columnspan=2, pady=(0, 5))

edit_worker_btn = ttk.Button(workers_frame, text=f'{emoji.emojize(":pencil:")} Edit Worker', bootstyle="warning", command=edit_worker)
edit_worker_btn.grid(row=3, column=0, sticky="ew", columnspan=2, pady=(0, 5))

delete_worker_btn = ttk.Button(workers_frame, text=f'{emoji.emojize(":wastebasket:")} Delete Worker', bootstyle="danger", command=delete_worker)
delete_worker_btn.grid(row=4, column=0, sticky="ew", columnspan=2, pady=(0, 5))
# ================================================================================================
# ========================================= FRAME 2 ==============================================
services_frame = tk.Frame(app, padx=10, pady=10, bg="white")
services_frame.grid(row=0, column=1, sticky="news")

services_label_image = resize_image("services-label.png", 250, 50)
services_label = tk.Label(services_frame, image=services_label_image, borderwidth=0, highlightthickness=0, highlightbackground="white")
services_label.grid(row=0, column=0, columnspan=2)

services_listbox_scrollbar = tk.Scrollbar(services_frame, orient=tk.VERTICAL)
services_listbox = Listbox(services_frame, background="white", fg="gray", width=25, yscrollcommand=services_listbox_scrollbar.set, borderwidth=0, highlightthickness=0)

services_listbox_scrollbar.config(command=services_listbox.yview)
services_listbox.grid(row=1, column=0, sticky=tk.NSEW)
services_listbox_scrollbar.grid(row=1, column=1, sticky=tk.NS)

add_service_btn = ttk.Button(services_frame, text=f'{emoji.emojize(":sparkles:")} Add New Service', command=add_service)
add_service_btn.grid(row=2, column=0, sticky="ew", columnspan=2, pady=(0, 5))

edit_service_btn = ttk.Button(services_frame, text=f'{emoji.emojize(":pencil:")} Edit Service', bootstyle="warning", command=edit_service)
edit_service_btn.grid(row=3, column=0, sticky="ew", columnspan=2, pady=(0, 5))

delete_service_btn = ttk.Button(services_frame, text=f'{emoji.emojize(":wastebasket:")} Delete Service', bootstyle="danger", command=delete_service)
delete_service_btn.grid(row=4, column=0, sticky="ew", columnspan=2, pady=(0, 5))
# ================================================= ==============================================
# ========================================= FRAME 3 ==============================================
jobs_frame = tk.Frame(app, padx=10, pady=10, bg="white")
jobs_frame.grid(row=1, column=0, sticky="news", columnspan=2)

jobs_label_image = resize_image("jobs-label.png", 565, 220)
jobs_label = tk.Label(jobs_frame, image=jobs_label_image, borderwidth=0, highlightthickness=0, highlightbackground="white")
jobs_label.grid(row=0, column=0, columnspan=2)

ttk.Style().configure("Treeview", background="white", foreground="black", fieldbackground="white")
ttk.Style().configure("Treeview.Heading", foreground="black")

jobs_tree = ttk.Treeview(jobs_frame, columns=('Time', 'Jobs', 'Workers'), show='headings')
jobs_tree_scrollbar = ttk.Scrollbar(jobs_frame, orient=tk.VERTICAL, command=jobs_tree.yview, bootstyle="default-round")

jobs_tree.heading('Time', text='Time')
jobs_tree.heading('Jobs', text='Jobs')
jobs_tree.heading('Workers', text='Workers')

jobs_tree.column('Time', width=170)
jobs_tree.column('Jobs', width=180)
jobs_tree.column('Workers', width=170)

jobs_tree.configure(yscrollcommand=jobs_tree_scrollbar.set)
jobs_tree.grid(row=1, column=0, sticky=tk.NSEW)
jobs_tree_scrollbar.grid(row=1, column=1, sticky=tk.NS)

btn_frame = tk.Frame(jobs_frame, bg="white", pady=5)
btn_frame.grid(row=2, column=0, columnspan=2)

add_job_btn = ttk.Button(btn_frame, text=f'{emoji.emojize(":sparkles:")} Add New Job', width=20, command=add_job)
add_job_btn.grid(row=0, column=0, sticky="news", padx=(0, 5))

edit_job_btn = ttk.Button(btn_frame, text=f'{emoji.emojize(":pencil:")} Edit Job', bootstyle="warning", width=18, command=edit_job)
edit_job_btn.grid(row=0, column=1, sticky="ew", padx=(0, 5))

delete_job_btn = ttk.Button(btn_frame, text=f'{emoji.emojize(":wastebasket:")} Delete Job', bootstyle="danger", width=15, command=delete_job)
delete_job_btn.grid(row=0, column=2, sticky="ew", padx=(0, 5))
load_data()
# ================================================================================================
# ========================================= FRAME 4 ==============================================
btn_frame = tk.Frame(app, bg="white", pady=20)
btn_frame.grid(row=2, column=0, columnspan=2)

get_salaries_btn = ttk.Button(btn_frame, text=f'{emoji.emojize("🤑")} Get Salaries', width=20, padding=5, bootstyle="success", command=get_salaries)
get_salaries_btn.grid(row=0, column=0, sticky="news", padx=(0, 10))

start_new_day_btn = ttk.Button(btn_frame, text=f'{emoji.emojize(":sun:")} Start New day', bootstyle="warning-outline", width=18, command=start_new_day)
start_new_day_btn.grid(row=0, column=1, sticky="ew", padx=(10, 0))
# ================================================================================================
app.mainloop()
