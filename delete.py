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
