from tkinter import *
from tkinter import ttk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv_tools as ct

import account_tools as at
import transactions_tools as tt

root = Tk()
root.title("ARBITRAGE God")
root.minsize(300, 300)


def destroy_app_frame():
    if var.get() == "":
        Label(app, text=" ( `_` ) Choose... ", fg="red").pack(padx=30)
        return 0
    app.destroy()
    account_balance_input()


app = Frame(root)
app.grid()
Label(app, text="ARBITRAGE God", fg="#00b2a9", font=("Arial", 26), padx=20).pack(fill='x', pady=(20, 0))
button_img = PhotoImage(file="logo100.png")
Button(app, image=button_img, fg="white", bg="#00b2a9", command=destroy_app_frame).pack(pady=30)
Label(app, text="Choose the currency to work with...", fg="#00b2a9", font=("Arial", 12)).pack()

var = StringVar()
combobox = ttk.Combobox(app, textvariable=var)
combobox['values'] = at.coins
combobox['state'] = 'readonly'
combobox.pack(fill='x', padx=5, pady=5)


def account_balance_input():
    balance_input = Frame(root)
    balance_input.grid()
    at.coin_symbol = var.get()

    Label(balance_input, text="ARBITRAGE God", fg="#00b2a9", font=("Arial", 26), padx=20, pady=20).grid(column=0, row=0,
                                                                                                        columnspan=3)
    Label(balance_input, text="Please fill your estimated accounts balances:", fg="#00b2a9", font=("Arial", 10)).grid(
        column=0, row=1, columnspan=3)
    Label(balance_input, text="$", fg="#00b2a9", font=("Arial", 10)).grid(column=1, row=2)
    Label(balance_input, text=at.coin_symbol, fg="#00b2a9", font=("Arial", 10)).grid(column=2, row=2)

    b_label = ttk.Label(balance_input, text="Binance:")
    b_label.grid(column=0, row=3, sticky=W, padx=5, pady=5)
    b_entry_f = ttk.Entry(balance_input)
    b_entry_f.grid(column=1, row=3, sticky=E, padx=5, pady=5)
    b_entry_c = ttk.Entry(balance_input)
    b_entry_c.grid(column=2, row=3, sticky=E, padx=5, pady=5)

    h_label = ttk.Label(balance_input, text="Huobi:")
    h_label.grid(column=0, row=4, sticky=W, padx=5, pady=5)
    h_entry_f = ttk.Entry(balance_input)
    h_entry_f.grid(column=1, row=4, sticky=E, padx=5, pady=5)
    h_entry_c = ttk.Entry(balance_input)
    h_entry_c.grid(column=2, row=4, sticky=E, padx=5, pady=5)

    k_label = ttk.Label(balance_input, text="kuCoin:")
    k_label.grid(column=0, row=5, sticky=W, padx=5, pady=5)
    k_entry_f = ttk.Entry(balance_input)
    k_entry_f.grid(column=1, row=5, sticky=E, padx=5, pady=5)
    k_entry_c = ttk.Entry(balance_input)
    k_entry_c.grid(column=2, row=5, sticky=E, padx=5, pady=5)

    def create_balance():
        Label(balance_input, text="I need all & correct values!", fg="red").grid(column=1, row=6)
        at.collect_input(b_entry_f, b_entry_c, h_entry_f, h_entry_c, k_entry_f, k_entry_c)
        balance_input.destroy()
        main_menu()

    create_button = ttk.Button(balance_input, text="Create", command=create_balance)
    create_button.grid(column=2, row=6, sticky=E, padx=5, pady=5)


def main_menu():
    frm_main_menu = Frame(root)
    frm_main_menu.grid()

    def history_window_launch():
        frm_main_menu.destroy()
        history_frame_create()

    def arbitrage_window_launch():
        frm_main_menu.destroy()
        arbitrage_live()

    def currency_input_window_launch():
        frm_main_menu.destroy()
        account_balance_input()

    Label(frm_main_menu, text="ARBITRAGE God", fg="#00b2a9", font=("Arial", 26), padx=20, pady=20).grid(column=0, row=0)
    ttk.Button(frm_main_menu, text="Arbitrage Live", width=20, command=arbitrage_window_launch).grid(column=0, row=1,
                                                                                                     pady=(20, 2))
    ttk.Button(frm_main_menu, text="Wallet settings", width=20, command=currency_input_window_launch).grid(column=0,
                                                                                                           row=2,
                                                                                                           pady=2)
    ttk.Button(frm_main_menu, text="History", width=20, command=history_window_launch).grid(column=0, row=3, pady=2)
    ttk.Button(frm_main_menu, text="Exit", width=20, command=exit).grid(column=0, row=4, pady=2)


def arbitrage_live():
    def back_to_main_menu():
        frm_arbitrage_live.destroy()
        main_menu()

    frm_arbitrage_live = Frame(root)
    frm_arbitrage_live.grid()
    Label(frm_arbitrage_live, text="Arbitrage is live", fg="#00b2a9", font=("Arial", 26), padx=20, pady=20).grid(
        column=0, row=0)
    ttk.Button(frm_arbitrage_live, text="Start", command=tt.start_transactions).grid()
    ttk.Button(frm_arbitrage_live, text="Back", command=back_to_main_menu).grid()


def history_frame_create():
    frm_history = Frame(root)
    frm_history.grid()

    def back_to_main_menu():
        frm_history.destroy()
        main_menu()

    def build_graph():
        def back():
            frm_graph.destroy()
            main_menu()

        frm_history.destroy()
        frm_graph = Frame(root)
        frm_graph.pack()

        fig = ct.create_graph()
        canvas = FigureCanvasTkAgg(fig, master=frm_graph)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, frm_graph)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        ttk.Button(frm_graph, text="Back", command=back).pack(side=BOTTOM)

    def show_log():
        for i in reversed(at.history[-6:]):
            Label(frm_history, text=i, font=("Arial", 7)).grid(pady=2)
        ttk.Button(frm_history, text="Back", command=back_to_main_menu).grid(padx=100, pady=10)

    Label(frm_history, text="History", fg="#00b2a9", font=("Arial", 26), padx=75, pady=10).grid()
    Label(frm_history, text=f"Congrats! Your session income: {at.session_income}", padx=40).grid(pady=(0, 10))
    show_log_btn = ttk.Button(frm_history, text="Show log", command=show_log)
    show_log_btn.grid(pady=2)
    build_graph_btn = ttk.Button(frm_history, text="Build graph", command=build_graph)
    build_graph_btn.grid(pady=2)


root.mainloop()
