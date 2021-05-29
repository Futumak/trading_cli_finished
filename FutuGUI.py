# Simple UI for trade.py from https://github.com/TraderSamwise/trading_cli_finished

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
import os
import json
from pprint import pprint

import trade

settings_file="gui_settings"
preferences_file="gui_preferences"

### Read Settings 
if os.path.isfile(settings_file+".txt"):
    ### read values from file:
    with open(settings_file+".txt", "r") as fp:
        settings = json.load(fp)
else:
    ### default values
    settings={
        "posx": 100,
        "posy": 100,
        "symbol": "BTC-PERP",
        "markets": {
                    "BTC-PERP": {
                                "start_price" : 15000,
                                "end_price": 25000,
                                "total": 0.5,  
                                "num_orders": 10
                                }
                }
        }
    
list_markets=[]
for markets in settings["markets"]:
    list_markets.append(markets)

### trading functions:
def cancel_all(symbol):
    trade.cancel_all(symbol)
def cancel_buys():
    trade.cancel_buys(symbol)
def cancel_sells():
    trade.cancel_sells(symbol)
def scaled_order(side):
    total=float(total_entry.get())
    symbol=symbol_entry.get()
    start_price=float(start_price_entry.get())
    end_price=float(end_price_entry.get())
    num_orders=int(num_orders_entry.get())
    
    ### send the order
    trade.scaled_order(symbol, side, total, start_price, end_price, num_orders)
    print("{} scaled orders {} {} {} from {} to {}" .format(num_orders, side, total, symbol, start_price, end_price))

def entry_replace(entry, newtext):
    entry.delete(0, END)
    entry.insert(0, newtext)
    return entry

def exchangebutton_click(exchange_clicked):
    return(exchange_clicked)

### changed the symbol combobox
def symbol_changed(event): 
    update_settings_markets(settings["symbol"]) #save current symbol settings before switching
    settings["symbol"] = symbol_entry.get()
    update_entries_UI(settings["symbol"]) # switch to new symbol

### update markets table with values from the UI entries
def update_settings_markets(symbol):
    settings["markets"][symbol]={}
    settings["markets"][symbol]["start_price"]=start_price_entry.get()
    settings["markets"][symbol]["end_price"]=end_price_entry.get()
    settings["markets"][symbol]["total"]=total_entry.get()
    settings["markets"][symbol]["num_orders"]=num_orders_entry.get()

### update all entries texts with the stored values for the symbol                                   
def update_entries_UI(symbol):
    entry_replace(total_entry, str(settings["markets"][symbol]["total"]))
    entry_replace(start_price_entry, str(settings["markets"][symbol]["start_price"]))
    entry_replace(end_price_entry, str(settings["markets"][symbol]["end_price"]))
    entry_replace(num_orders_entry, str(settings["markets"][symbol]["num_orders"]))

### init window
window = tk.Tk()
window.title("Futu GUI")
window.iconbitmap('./logo.ico')
window.configure(background="#111722")
window.geometry("390x350+"+str(settings["posx"])+"+"+ str(settings["posy"]))

### read preferences
if os.path.isfile(preferences_file+".txt"):
    with open(preferences_file+".txt", "r") as fp:
        preferences = json.load(fp)    
else:
    tk.messagebox.showinfo(title="Error", message="Preferences file not found")
    window.destroy()

### UI: BUY SELL buttons
frame_scaled = tk.Frame(window, bg="#111722")
frame_scaled.grid(row=1, column=0, sticky="nsew", padx=20)
BUY_scaled_order_button = tk.Button(frame_scaled, font="verdana 14 bold", text="SCALED BUY", padx=5, pady=5, fg="white", bg="#02C77A", command=lambda: scaled_order("buy"))
BUY_scaled_order_button.grid(row=0, column=0)
SELL_scaled_order_button = tk.Button(frame_scaled, font="verdana 14 bold", text="SCALED SELL", padx=10, pady=5, fg="white", bg="#FF3B69", command=lambda: scaled_order("sell"))
SELL_scaled_order_button.grid(row=0, column=1, pady=20)

### UI: symbol
symbol_label = Label(frame_scaled, text="Symbol:", justify=RIGHT, bg="#111722", fg="#999999", font="none 12")
symbol_label.grid(row=1, column=0, sticky=E)
combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#111722',
                                       'fieldbackground': '#222733',
                                       'arrowcolor ': '#999999',
                                       'foreground': 'white',
                                       'insertcolor': 'white',
                                       'background': '#111722',
                                       'selectbackground': '#0078D7'
                                      }
                                     }
                                    }
                        )
window.option_add("*TCombobox*Listbox*Background", '#222733')
window.option_add("*TCombobox*Listbox*Foreground", 'white')
window.option_add("*TCombobox*Listbox*selectBackground", '#0078D7')
window.option_add("*TCombobox*Listbox*selectForeground", 'white')
combostyle.theme_use('combostyle') 
selected_symbol = tk.StringVar()
symbol_entry = ttk.Combobox(frame_scaled, values = list_markets, textvariable=selected_symbol)
symbol_entry.bind('<<ComboboxSelected>>', symbol_changed)
symbol_entry.grid(row=1, column=1, ipady=3)
symbol_entry.set(settings["symbol"])

### UI: Total Amount
total_label = Label(frame_scaled, text="Total Amount:", justify=RIGHT, bg="#111722", fg="#999999", font="none 12")
total_label.grid(row=3, column=0, sticky=E)
total_entry_var = tk.StringVar()
total_entry = Entry(frame_scaled, font="none "+str(preferences["fontsize"]), width = preferences["entrywidth"], bg="#222733", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF", highlightcolor="#AAAAAA", selectborderwidth=0, insertborderwidth=0, relief=FLAT, textvariable=total_entry_var)
total_entry.insert(0,str(settings["markets"][settings["symbol"]]["total"]))
total_entry.grid(row=3, column=1, pady=10)

### UI: Start price
start_price_label = Label(frame_scaled, text="Start Price:", justify=RIGHT, bg="#111722", fg="#999999", font="none 12")
start_price_label.grid(row=4, column=0, sticky=E)
start_price_entry_var = tk.StringVar()
start_price_entry = Entry(frame_scaled, font="none "+str(preferences["fontsize"]), width = preferences["entrywidth"], bg="#222733", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF", highlightcolor="#AAAAAA", selectborderwidth=0, insertborderwidth=0, relief=FLAT, textvariable=start_price_entry_var)
start_price_entry.insert(0,str(settings["markets"][settings["symbol"]]["start_price"]))
start_price_entry.grid(row=4, column=1)
### UI: End price
end_price_label = Label(frame_scaled, text="End Price:", justify=RIGHT, bg="#111722", fg="#999999", font="none 12")
end_price_label.grid(row=5, column=0, sticky=E)
end_price_entry_var = tk.StringVar()
end_price_entry = Entry(frame_scaled, font="none "+str(preferences["fontsize"]), width = preferences["entrywidth"], bg="#222733", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF", highlightcolor="#AAAAAA", selectborderwidth=0, insertborderwidth=0, relief=FLAT, textvariable=end_price_entry_var)
end_price_entry.insert(0,str(settings["markets"][settings["symbol"]]["end_price"]))
end_price_entry.grid(row=5, column=1)

### UI: Number of orders
num_orders_label = Label(frame_scaled, text="Number of orders:", justify=RIGHT, bg="#111722", fg="#999999", font="none 12")
num_orders_label.grid(row=6, column=0, sticky=E)
num_orders_entry_var = tk.StringVar()
num_orders_entry = Entry(frame_scaled, font="none "+str(preferences["fontsize"]), width = preferences["entrywidth"], bg="#222733", fg="#FFFFFF", bd=0, insertbackground="#FFFFFF", highlightcolor="#AAAAAA", selectborderwidth=0, insertborderwidth=0, relief=FLAT, textvariable=num_orders_entry_var)
num_orders_entry.insert(0,str(settings["markets"][settings["symbol"]]["num_orders"]))
num_orders_entry.grid(row=6, column=1, pady=10)

### cancel orders
frame_cancel = tk.Frame(window, bg="#111722")
frame_cancel.grid(row=2, pady=10)
cancel_all_button = tk.Button(frame_cancel, text="CANCEL ALL "+settings["symbol"] +" ORDERS", padx=16, pady=2, font="none 8", fg="white", bg="#1C2230", command=lambda: cancel_all(settings["symbol"]))
cancel_all_button.grid(row=1, column=0, pady=2)
# cancel_buys_button = tk.Button(frame_cancel, text="CANCEL BUY", padx=2, pady=2, font="none 8", fg="white", bg="#1C2230", command=cancel_buys)
# cancel_buys_button.grid(row=1, column=1, pady=2)
# cancel_sells_button = tk.Button(frame_cancel, text="CANCEL SELL", padx=2, pady=2, font="none 8", fg="white", bg="#1C2230", command=cancel_sells)
# cancel_sells_button.grid(row=1, column=2, pady=2)

### When exiting app, save settings
def on_closing():
    temp_symbol_entry = symbol_entry.get()
    update_settings_markets(temp_symbol_entry)
    
    settings["posx"] = window.winfo_x()
    settings["posy"] = window.winfo_y()
    settings["symbol"] = symbol_entry.get()

    with open(settings_file+".txt", "w") as fp:
        json.dump(settings, fp)

    window.destroy()
    
### start app
if __name__ == "__main__":
    ### set window on top
    window.lift()
    window.call('wm', 'attributes', '.', '-topmost', True) # window.after_idle(window.call, 'wm', 'attributes', '.', '-topmost', False)
    
    window.protocol("WM_DELETE_WINDOW", on_closing)
    
    window.mainloop()
