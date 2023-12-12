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


def resize_image(path, desired_width, desired_height):
    workers_label_image = Image.open(path)  

    width, height = workers_label_image.size
    aspect_ratio = width / height

    if width > height:
        new_width = desired_width
        new_height = int(desired_width / aspect_ratio)
    else:
        new_height = desired_height
        new_width = int(desired_height * aspect_ratio)

    resized_image = workers_label_image.resize((new_width, new_height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)

    return photo
def is_valid_time_format(input_time):
    try:
        # Parse the input string with the specified format
        datetime.strptime(input_time, '%I:%M %p')
        return True
    except ValueError:
        return False
def is_earlier_time(time1, time2):
    # Convert time strings to datetime objects
    time_format = '%I:%M %p'
    datetime1 = datetime.strptime(time1, time_format)
    datetime2 = datetime.strptime(time2, time_format)

    return datetime1 < datetime2
def is_worker_available(worker, time):
    time_format = '%I:%M %p'
    input_time = datetime.strptime(time, time_format)

    for job in jobs:
        for workerr in job.workers:
            if str(workerr) == str(worker):
                if datetime.strptime(job.start_time, '%I:%M %p') <= input_time <= datetime.strptime(job.end_time, '%I:%M %p'):
                    return False  # Worker found in a job within the specified time
    return True


def add_worker():
    add_worker_window_root = tk.Toplevel(root)
    add_worker_window_root.title("Add Worker")
    
    add_worker_window = tk.Frame(add_worker_window_root, padx=10, pady=10, bg="white")
    add_worker_window.pack(fill=tk.BOTH, expand=True)

    first_name_label = ttk.Label(add_worker_window, text="First Name:")
    first_name_label.grid(row=0, column=0)
    first_name_entry = ttk.Entry(add_worker_window)
    first_name_entry.grid(row=0, column=1, pady=(0,10))

    last_name_label = ttk.Label(add_worker_window, text="Last Name:")
    last_name_label.grid(row=1, column=0)
    last_name_entry = ttk.Entry(add_worker_window)
    last_name_entry.grid(row=1, column=1, pady=(0,10))

    def add_button_click():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        if not first_name or not last_name:  
            messagebox.showwarning("Warning", "Fill in all fields!")
            return 
        workers_listbox.insert(tk.END, f'{first_name} {last_name}')
        workers.append(Worker(first_name, last_name))
        add_worker_window_root.destroy()  

    add_btn = ttk.Button(add_worker_window, text="Add", command=add_button_click, width=10)
    add_btn.grid(row=6, column=0, columnspan=2, sticky="e")
def add_service():
    add_service_window_root = tk.Toplevel(root)
    add_service_window_root.title("Add Service")
    
    add_service_window = tk.Frame(add_service_window_root, padx=10, pady=10, bg="white")
    add_service_window.pack(fill=tk.BOTH, expand=True)

    service_name_label = ttk.Label(add_service_window, text="Service Name:")
    service_name_label.grid(row=0, column=0)
    service_name_entry = ttk.Entry(add_service_window)
    service_name_entry.grid(row=0, column=1, pady=(0,10))

    service_price_label = ttk.Label(add_service_window, text="Price:")
    service_price_label.grid(row=1, column=0)
    service_price_entry = ttk.Entry(add_service_window)
    service_price_entry.grid(row=1, column=1, pady=(0,10))

    def add_button_click():
        service_name = service_name_entry.get()
        service_price = service_price_entry.get()
        if not service_name or not service_price:  
            messagebox.showwarning("Warning", "Fill in all fields!")
            return 
        if not isinstance(service_price, float) and not isinstance(service_price, int):
            messagebox.showinfo("Error", "Price should be a number.")
            return
        services_listbox.insert(tk.END, f"{service_name:<20} {service_price:<3} UAH")
        services.append(Service(service_name, service_price))
        add_service_window_root.destroy()  

    add_btn = ttk.Button(add_service_window, text="Add", command=add_button_click, width=10)
    add_btn.grid(row=6, column=0, columnspan=2, sticky="e")
def add_job():
    add_job_window_root = tk.Toplevel(root)
    add_job_window_root.title("Add Job")
    
    add_job_window = tk.Frame(add_job_window_root, padx=10, pady=10, bg="white")
    add_job_window.pack(fill=tk.BOTH, expand=True)

    current_time = datetime.now().strftime("%I:%M %p")
    job_time_label = ttk.Label(add_job_window, text="Job Start Time:")
    job_time_label.grid(row=0, column=0)
    job_time_entry = ttk.Entry(add_job_window)
    job_time_entry.insert(tk.END, current_time)
    job_time_entry.grid(row=0, column=1, pady=(0,10))

    job_end_time_label = ttk.Label(add_job_window, text="Job End Time:")
    job_end_time_label.grid(row=1, column=0)
    job_end_time_entry = ttk.Entry(add_job_window)
    job_end_time_entry.insert(tk.END, (datetime.strptime(current_time, "%I:%M %p")+ timedelta(minutes=30)).strftime("%I:%M %p"))
    job_end_time_entry.grid(row=1, column=1, pady=(0,10))

    services_label = ttk.Label(add_job_window, text="Services:")
    services_label.grid(row=2, column=0, sticky="w")
    services_checkboxes = []
    for i in range(len(services)):
        services_checkboxes.append(tk.IntVar())
        check_button = tk.Checkbutton(add_job_window, text=(services[i].name), variable=services_checkboxes[i])
        check_button.grid(row=i+2, column=1, pady=(0,10), sticky="w")

    workers_label = ttk.Label(add_job_window, text="Workers:")
    workers_label.grid(row=len(services) + 2, column=0, sticky="w")
    workers_checkboxes = []
    for i in range(len(workers)):
        workers_checkboxes.append(tk.IntVar())
        check_button = tk.Checkbutton(add_job_window, text=str(workers[i]), variable=workers_checkboxes[i])
        check_button.grid(row=len(services)+i+2, column=1, pady=(0,10), sticky="w")

    def add_button_click():
        if not job_time_entry.get() or not job_end_time_entry.get():  
            messagebox.showwarning("Warning", "Fill in all fields!")
            return 
        if not is_valid_time_format(job_time_entry.get()) or not is_valid_time_format(job_end_time_entry.get()):
            messagebox.showwarning("Warning", "Wrong time format!")
            return 
        if is_earlier_time(job_end_time_entry.get(), job_time_entry.get()):
            messagebox.showwarning("Warning", "Job end time can't be before its start time:)")
            return 
        
        for i in range(len(workers)):
            if workers_checkboxes[i].get() == 1:
                if not is_worker_available(workers[i], job_time_entry.get()):
                    messagebox.showwarning("Warning", f"The worker {workers[i]} isn't available at the moment")
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

        job = Job(datetime.now(), datetime.now() + timedelta(minutes=30), [], [])
        job.start_time = job_time_entry.get()
        job.end_time = job_end_time_entry.get()
       
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
        jobs_tree.insert("", "end", values=(f"{datetime.strptime(job.start_time, '%I:%M %p').strftime('%I:%M %p')} - {datetime.strptime(job.end_time, '%I:%M %p').strftime('%I:%M %p')}", job_services_str, job_workers_str))
        jobs.append(job)
        add_job_window_root.destroy()  

    add_btn = ttk.Button(add_job_window, text="Add", command=add_button_click, width=10)
    add_btn.grid(row=len(workers) + len(services) + 2, column=0, columnspan=2, sticky="e")

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

def delete_worker():
    if not workers_listbox.curselection():
        return
    selected_index = [int(index) for index in workers_listbox.curselection()][0]
    workers_listbox.delete(selected_index)
    workers.pop(selected_index)
def delete_service():
    if not services_listbox.curselection():
        return
    selected_index = [int(index) for index in services_listbox.curselection()][0]
    services_listbox.delete(selected_index)
    services.pop(selected_index)
def delete_job():
    if not jobs_tree.selection():
        return
    selected_row = jobs_tree.selection()
    selected_index = jobs_tree.index(jobs_tree.selection()[0])
    jobs_tree.delete(selected_row)
    jobs.pop(selected_index)

def get_jobs_for_worker(worker):
    worker_jobs = []

    for job in jobs:
        for workerr in job.workers:
            if worker.first_name == workerr.first_name and worker.last_name == workerr.last_name:
                worker_jobs.append(job)
    return worker_jobs
def save_data(): # зберігає дані у файл
    worker_dicts = [worker.to_dict() for worker in workers]
    workers_json = json.dumps(worker_dicts, indent=2)

    file_name = 'workers.json'  
    with open(file_name, 'w') as file:
        file.write(workers_json)

    service_dicts = [service.to_dict() for service in services]
    services_json = json.dumps(service_dicts, indent=2)

    file_name = 'services.json'  
    with open(file_name, 'w') as file:
        file.write(services_json)

    job_dicts = [job.to_dict() for job in jobs]
    jobs_json = json.dumps(job_dicts, indent=2)

    file_name = 'jobs.json'  
    with open(file_name, 'w') as file:
        file.write(jobs_json)
def on_close(root): # при закриванні вікна потрібно зберегти дані
    save_data()
    root.destroy()
def load_data(): # при відкриванні потрібно відобразити дані з файлу
    current_directory = os.getcwd()
    with open(f"{current_directory}/workers.json", "r") as json_file:
        serialized_workers = json.load(json_file)
        for serialized_worker in serialized_workers:
            worker = Worker(
                first_name=serialized_worker["first_name"],
                last_name=serialized_worker["last_name"],
            )
            workers.append(worker)
            workers_listbox.insert(tk.END, f'{worker.first_name} {worker.last_name}')

    with open(f"{current_directory}/services.json", "r") as json_file:
        serialized_services = json.load(json_file)
        for serialized_service in serialized_services:
            service = Service(
                name=serialized_service["name"],
                price=serialized_service["price"],
            )
            services.append(service)
            services_listbox.insert(tk.END, f"{service.name:<20} {service.price:<3} UAH")

    with open(f"{current_directory}/jobs.json", "r") as json_file:
        try:
            serialized_jobs = json.load(json_file)
            for item in serialized_jobs:
                job_workers = [Worker(worker['first_name'], worker['last_name']) for worker in item['workers']]
                job_services = [Service(service['name'], service['price']) for service in item['services']]
                job = Job(item['start_time'], item['end_time'],job_workers, job_services)
                jobs.append(job)

                job_services_str = ""
                for item in job.services:
                    job_services_str += f'{item.name}; '

                job_workers_str = ""
                for item in job.workers:
                    job_workers_str += f'{item.first_name} {item.last_name}; '
                jobs_tree.insert("", "end", values=(f"{job.start_time} - {job.end_time}", job_services_str, job_workers_str))
        except json.JSONDecodeError as e:
            pass
def start_new_day():  # коли розпочинається новий робочий день, список робіт очишається
    global jobs
    jobs = []
    jobs_tree.delete(*jobs_tree.get_children())
    with open(f"{os.getcwd()}/jobs.json", 'w') as file:
        pass 
def calculate_salary(): # розрахунок зарплат
    for job in jobs:
        for worker in job.workers:
            worker.salary = 0
    for w in workers:
        w.salary = 0
    
    total = 0

    for job in jobs:
        for worker in job.workers:
            for w in workers:
                if str(w) == str(worker):
                    w.salary += worker.salary

    for job in jobs:
        money = 0
        for service in job.services:
            money += int(service.price)
        for worker in job.workers:
            worker.salary = (money/2)/len(job.workers)
    for job in jobs:
        for worker in job.workers:
            for w in workers:
                if str(w) == str(worker):
                    w.salary += worker.salary

    for job in jobs:
        for service in job.services:
            total += int(service.price)

    return float(float(total)/2)        
def get_salaries(): # обробник кнопки для розрахунку зарплат
    salary = calculate_salary()
    get_salaries_window_root = tk.Toplevel(root)
    get_salaries_window_root.title("Salaries")
    
    get_salaries_window = tk.Frame(get_salaries_window_root, padx=60, pady=60, bg="white")
    get_salaries_window.pack(fill=tk.BOTH, expand=True)

    total_label = ttk.Label(get_salaries_window, text=f'💰 TOTAL TODAY:')
    total_label.grid(row=0, column=0, pady=(0,40), sticky="w")
    total_salary_label = ttk.Label(get_salaries_window, text=f"{salary*2} UAH")
    total_salary_label.grid(row=0, column=1, pady=(0,40), sticky="e")

    def see_worker_jobs_details(worker):
        worker_jobs = get_jobs_for_worker(worker)
        worker_jobs_log_str = ""
        for worker_job in worker_jobs:
            worker_jobs_log_str += worker_job.to_str()
            worker_jobs_log_str += '\n\n'
        
        see_details_window = tk.Toplevel(get_salaries_window_root)
        see_details_window.title(f"{worker.first_name} {worker.last_name} deatails")
        details_header_label = ttk.Label(see_details_window, text=f'💰 {worker.first_name} {worker.last_name} JOBS LOG:')
        details_header_label.grid(row=0, column=0, pady=(0,40), sticky="w")
        detials_label = ttk.Label(see_details_window, text=worker_jobs_log_str)
        detials_label.grid(row=1, column=0, pady=(0,40), sticky="w")

    for i in range(len(workers)):

        worker_label = ttk.Label(get_salaries_window, text=f'{workers[i].first_name} {workers[i].last_name}')
        worker_label.grid(row=i+1, column=0, pady=(0,20), sticky="w", padx=(0,10))
        worker_salary_label = ttk.Label(get_salaries_window, text=f"{workers[i].salary} UAH")
        worker_salary_label.grid(row=i+1, column=1, pady=(0,20), sticky="e")

        see_details_btn = ttk.Button(get_salaries_window, text="See Details", command=lambda w=workers[i]: see_worker_jobs_details(w), width=10)
        see_details_btn.grid(row=i+1, column=2, pady=(0,20),padx=20, sticky="e")

    owner_label = ttk.Label(get_salaries_window, text=f'👨‍💻 Owner:')
    owner_label.grid(row=len(workers)+1, column=0, pady=(40,40), sticky="w")
    owner_salary_label = ttk.Label(get_salaries_window, text=f"{salary} UAH")
    owner_salary_label.grid(row=len(workers)+1, column=1, pady=(40,40), sticky="e")


class Worker:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.salary = 0
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name
        }
class Service:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def __str__(self):
        return f"{self.name:<20} {self.price:<3} UAH"
    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price
        }
class Job:
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=30)
        self.workers = []
        self.services = []
    def __init__(self, start_time, end_time, workers, services):
        self.start_time = start_time
        self.end_time = end_time
        self.workers = workers
        self.services = services
    def __str__(self) -> str:
        string = f'Time: {self.start_time}-{self.end_time}\nWorkers:\n'
        for item in self.workers:
            string += "\t"
            string += str(item)
            string += "\n"
        string += "Services:\n"
        for item in self.services:
            string += "\t"
            string += str(item)
            string += "\n"
        return string
    def to_str(self):
        string = f'Time:\t{self.start_time}-{self.end_time}\nWorkers:\t'
        for item in self.workers:
            string += str(item)
            string += ", "
        string += "\nServices:\t"
        for item in self.services:
            string += f"{item.name} {item.price} ({item.price}/{len(self.workers) * 2} = {(int(item.price)/len(self.workers))/2})"
            string += ", "
        return string
    def to_dict(self):
        workers_list = [worker.to_dict() for worker in self.workers]
        services_list = [service.to_dict() for service in self.services]

        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'workers': workers_list,
            'services': services_list
        }

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
