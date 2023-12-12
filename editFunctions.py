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
def edit_worker():
    if not workers_listbox.curselection():
        return
    selected_index = [int(index) for index in workers_listbox.curselection()][0]
    worker = workers[selected_index]

    edit_worker_window_root = tk.Toplevel(root)
    edit_worker_window_root.title("Edit Worker")
    
    edit_worker_window = tk.Frame(edit_worker_window_root, padx=10, pady=10, bg="white")
    edit_worker_window.pack(fill=tk.BOTH, expand=True)

    first_name_label = ttk.Label(edit_worker_window, text="First Name:")
    first_name_label.grid(row=0, column=0)
    first_name_entry = ttk.Entry(edit_worker_window)
    first_name_entry.grid(row=0, column=1, pady=(0,10))
    first_name_entry.insert(tk.END, worker.first_name)

    last_name_label = ttk.Label(edit_worker_window, text="Last Name:")
    last_name_label.grid(row=1, column=0)
    last_name_entry = ttk.Entry(edit_worker_window)
    last_name_entry.grid(row=1, column=1, pady=(0,10))
    last_name_entry.insert(tk.END, worker.last_name)

    def edit_button_click():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        if not first_name or not last_name:  
            messagebox.showwarning("Warning", "Fill in all fields!")
            return 
        workers_listbox.delete(selected_index)
        workers_listbox.insert(selected_index, f'{first_name} {last_name}')

        workers[selected_index] = Worker(first_name, last_name)
        edit_worker_window_root.destroy()  

    edit_btn = ttk.Button(edit_worker_window, text="Edit", command=edit_button_click, width=10)
    edit_btn.grid(row=6, column=0, columnspan=2, sticky="e") 
def edit_service():
    if not services_listbox.curselection():
        return
    selected_index = [int(index) for index in services_listbox.curselection()][0]
    service = services[selected_index]

    edit_service_window_root = tk.Toplevel(root)
    edit_service_window_root.title("Edit Worker")
    
    edit_service_window = tk.Frame(edit_service_window_root, padx=10, pady=10, bg="white")
    edit_service_window.pack(fill=tk.BOTH, expand=True)

    service_name_label = ttk.Label(edit_service_window, text="Service Name:")
    service_name_label.grid(row=0, column=0)
    service_name_entry = ttk.Entry(edit_service_window)
    service_name_entry.grid(row=0, column=1, pady=(0,10))
    service_name_entry.insert(tk.END, service.name)

    serice_price_label = ttk.Label(edit_service_window, text="Price:")
    serice_price_label.grid(row=1, column=0)
    service_price_entry = ttk.Entry(edit_service_window)
    service_price_entry.grid(row=1, column=1, pady=(0,10))
    service_price_entry.insert(tk.END, service.price)

    def edit_button_click():
        service_name = service_name_entry.get()
        service_price = service_price_entry.get()

        if not service_name or not service_price:  
            messagebox.showwarning("Warning", "Fill in all fields!")
            return 
        if not isinstance(service_price, float) and not isinstance(service_price, int):
            messagebox.showinfo("Error", "Price should be a number.")
            return

        services_listbox.delete(selected_index)
        services_listbox.insert(selected_index, f"{service_name:<20} {service_price:<3} UAH")

        services[selected_index] = Service(service_name, service_price)
        edit_service_window_root.destroy()  

    edit_btn = ttk.Button(edit_service_window, text="Edit", command=edit_button_click, width=10)
    edit_btn.grid(row=6, column=0, columnspan=2, sticky="e")
def edit_job():
    if not jobs_tree.selection():
        return 
    selected_index = jobs_tree.index(jobs_tree.selection()[0])
    job = jobs[selected_index]

    edit_job_window_root = tk.Toplevel(root)
    edit_job_window_root.title("Add Job")
    
    edit_job_window = tk.Frame(edit_job_window_root, padx=10, pady=10, bg="white")
    edit_job_window.pack(fill=tk.BOTH, expand=True)

    job_time_label = ttk.Label(edit_job_window, text="Job Start Time:")
    job_time_label.grid(row=0, column=0)
    job_time_entry = ttk.Entry(edit_job_window)
    job_time_entry.insert(tk.END, job.start_time)
    job_time_entry.grid(row=0, column=1, pady=(0,10))

    job_end_time_label = ttk.Label(edit_job_window, text="Job End Time:")
    job_end_time_label.grid(row=1, column=0)
    job_end_time_entry = ttk.Entry(edit_job_window)
    job_end_time_entry.insert(tk.END, job.end_time)
    job_end_time_entry.grid(row=1, column=1, pady=(0,10))

    services_label = ttk.Label(edit_job_window, text="Services:")
    services_label.grid(row=2, column=0, sticky="w")
    services_checkboxes = []
    for i in range(len(services)):
        var = tk.IntVar()
        for service in job.services:
            if str(services[i]) == str(service):
                var.set(1)
                break
        services_checkboxes.append(var)
        check_button = tk.Checkbutton(edit_job_window, text=(services[i].name), variable=services_checkboxes[i])
        check_button.grid(row=i+2, column=1, pady=(0,10), sticky="w")

    workers_label = ttk.Label(edit_job_window, text="Workers:")
    workers_label.grid(row=len(services) + 2, column=0, sticky="w")
    workers_checkboxes = []
    for i in range(len(workers)):
        var = tk.IntVar()
        for worker in job.workers:
            if str(workers[i]) == str(worker):
                var.set(1)
                break
        workers_checkboxes.append(var)
        check_button = tk.Checkbutton(edit_job_window, text=str(workers[i]), variable=workers_checkboxes[i])
        check_button.grid(row=len(services)+i+2, column=1, pady=(0,10), sticky="w")

    def edit_button_click():
        if not job_time_entry.get() or not job_end_time_entry.get():  
            messagebox.showwarning("Warning", "Fill in all fields!")
            return 
        if not is_valid_time_format(job_time_entry.get()) or not is_valid_time_format(job_end_time_entry.get()):
            messagebox.showwarning("Warning", "Wrong time format!")
            return 
        if is_earlier_time(job_end_time_entry.get(), job_time_entry.get()):
            messagebox.showwarning("Warning", "Job end time can't be before its start time:)")
            return 
        at_least_one_worker_checked = FALSE
        at_least_one_service_checked = FALSE

        for i in range(len(workers)):
            if workers_checkboxes[i].get() == 1:
                at_least_one_worker_checked = TRUE

        for i in range(len(services)):
            if services_checkboxes[i].get() == 1:
                at_least_one_service_checked = TRUE

        if at_least_one_service_checked == FALSE or at_least_one_worker_checked == FALSE:
            messagebox.showwarning("Warning", "You must pick at least one worker and at least one service")
            return 
        
        for i in range(len(workers)):
            if workers_checkboxes[i].get() == 1:
                if not is_worker_available(workers[i], job_time_entry.get()):
                    messagebox.showwarning("Warning", f"The worker {workers[i]} isn't available at the moment")
                    return 

        job.start_time = job_time_entry.get()
        job.end_time = job_end_time_entry.get()
        job.workers = []
        job.services = []
        for i in range(len(workers)):
            if workers_checkboxes[i].get() == 1:
                job.workers.append(workers[i])


        for i in range(len(services)):
            if services_checkboxes[i].get() == 1:
                job.services.append(services[i])

        job_services_str = ""
        for item in job.services:
            job_services_str += f'{item.name}; '

        job_workers_str = ""
        for item in job.workers:
            job_workers_str += f'{item.first_name} {item.last_name}; '

        jobs_tree.item(jobs_tree.selection(), values=(f"{job.start_time} - {job.end_time}", job_services_str, job_workers_str))
        jobs[selected_index] = job
        edit_job_window_root.destroy()  

    edit_btn = ttk.Button(edit_job_window, text="Edit", command=edit_button_click, width=10)
    edit_btn.grid(row=len(workers) + len(services) + 2, column=0, columnspan=2, sticky="e")
