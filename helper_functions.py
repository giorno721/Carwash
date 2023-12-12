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
