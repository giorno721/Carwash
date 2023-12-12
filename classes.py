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
