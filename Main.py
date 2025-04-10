import numpy as np
import pandas as pd
from tkinter import *
from tkinter.filedialog import askopenfilename
import re
from decimal import Decimal

file = 'testing.gcode'

def extract_filament_used(filename):
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("; total filament used [g] = "):
                return float(line.split("=")[1].strip())
            
def extract_printing_time_seconds(filename):
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("; estimated printing time (normal mode) = "):
                time_str = line.split("=")[1].strip()
                
                # Extract hours, minutes, and seconds
                match = re.match(r"(\d+)h (\d+)m (\d+)s", time_str)
                if match:
                    hours, minutes, seconds = map(int, match.groups())
                    return hours * 3600 + minutes * 60 + seconds
                
                match = re.match(r"(\d+)m (\d+)s", time_str)
                if match:
                    minutes, seconds = map(int, match.groups())
                    return minutes * 60 + seconds
                
                match = re.match(r"(\d+)s", time_str)
                if match:
                    return int(match.group(1))
    return None


Filament_used = extract_filament_used(file)
Time_used = extract_printing_time_seconds(file)

print("Filament Used:",Filament_used,"g")
print("Time Used:",Time_used,"Seconds")


"""Config Variable"""
Price_per_Kg = 469
Time_cost = 12
Time_cost_expo = 0.2

Price_per_unit = 7
Power_usage = 100

Maintenance = 0.3

Plastic_cost = round(Filament_used * (Price_per_Kg * 0.001),2)
Time_cost = round(pow((Time_used / 60),Time_cost_expo) * Time_cost,2)
Electricity_Cost = round((Time_used / 3600) * (Power_usage / 1000) * Price_per_unit,2)
Maintenance_Cost = round((Plastic_cost + Time_cost) * Maintenance,2)

Total_Price = round(Plastic_cost + Time_cost + Electricity_Cost + Maintenance_Cost,2)

print("Plastic cost:",Plastic_cost)
print("Time cost:",Time_cost)
print("Electricity cost:",Electricity_Cost)
print("Maintenance cost:",Maintenance_Cost)

print("Total = ",Total_Price)
