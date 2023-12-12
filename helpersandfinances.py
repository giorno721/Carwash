
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

