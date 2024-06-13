import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from threading import Thread

class IPLMatchResultsDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("IPL Match Results Dashboard")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Apply a theme
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TCombobox", font=("Helvetica", 10))
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # MongoDB connection
        self.client = MongoClient("mongodb+srv://admin:Santosh1210%40@projects.cqzixbp.mongodb.net/")
        self.db = self.client["IPL_Stats"]
        self.collection = self.db["matches_played"]

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(expand=True, fill="both")

        # Title
        title_label = ttk.Label(main_frame, text="IPL Match Results Dashboard", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)

        # Input frame
        input_frame = ttk.Frame(main_frame, padding="10 10 10 10")
        input_frame.pack(pady=10)

        # Team selection
        self.team_names = [
            'Chennai Super Kings', 'Delhi Capitals', 'Delhi Daredevils', 'Kolkata Knight Riders', 'Mumbai Indians',
            'Kings XI Punjab', 'Royal Challengers Bangalore', 'Rajasthan Royals', 'Sunrisers Hyderabad',
            'Deccan Chargers', 'Pune Warriors India', 'Gujarat Lions', 'Rising Pune Supergiant', 'Kochi Tuskers Kerala',
            'Gujarat Titans', 'Lucknow Super Giants'
        ]

        label_team1 = ttk.Label(input_frame, text="Select Team 1:")
        label_team1.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.team1_combobox = ttk.Combobox(input_frame, values=self.team_names, state="readonly")
        self.team1_combobox.grid(row=0, column=1, padx=5, pady=5)

        label_team2 = ttk.Label(input_frame, text="Select Team 2:")
        label_team2.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.team2_combobox = ttk.Combobox(input_frame, values=self.team_names, state="readonly")
        self.team2_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Season selection
        label_season = ttk.Label(input_frame, text="Select Season:")
        label_season.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.season_combobox = ttk.Combobox(input_frame, values=list(range(2008, 2024)), state="readonly")
        self.season_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Search button
        self.search_button = ttk.Button(input_frame, text="Search", command=self.on_search_click)
        self.search_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Loading label
        self.loading_label = ttk.Label(main_frame, text="", foreground="red")
        self.loading_label.pack(pady=5)

        # Treeview for displaying results
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(expand=True, fill="both")

        self.tree = ttk.Treeview(tree_frame, columns=("Team 1", "Team 2", "Winner", "Result Margin", "Ground", "Match Date"))
        self.tree.heading("#0", text="Match ID")
        self.tree.heading("Team 1", text="Team 1")
        self.tree.heading("Team 2", text="Team 2")
        self.tree.heading("Winner", text="Winner")
        self.tree.heading("Result Margin", text="Result Margin")
        self.tree.heading("Ground", text="Ground")
        self.tree.heading("Match Date", text="Match Date")

        self.tree.column("#0", width=100)
        self.tree.column("Team 1", width=150)
        self.tree.column("Team 2", width=150)
        self.tree.column("Winner", width=150)
        self.tree.column("Result Margin", width=100)
        self.tree.column("Ground", width=150)
        self.tree.column("Match Date", width=100)

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

    def on_search_click(self):
        team1 = self.team1_combobox.get()
        team2 = self.team2_combobox.get()
        season = self.season_combobox.get()

        if not team1 or not team2 or not season:
            messagebox.showwarning("Input Error", "Please select both teams and the season.")
            return

        self.loading_label.config(text="Loading data, please wait...")
        self.tree.delete(*self.tree.get_children())

        thread = Thread(target=self.search_matches, args=(team1, team2, season))
        thread.start()

    def search_matches(self, team1, team2, season):
        matches = self.collection.find({
            'Season': int(season),
            '$or': [
                {'Team_1': team1, 'Team_2': team2},
                {'Team_1': team2, 'Team_2': team1}
            ]
        })

        for match in matches:
            self.tree.insert('', 'end', text=match.get('_id'), values=(
                match.get('Team_1', ''),
                match.get('Team_2', ''),
                match.get('Winner', ''),
                f"{match.get('result_margin_value', '')} {match.get('result_margin_type', '')}",
                match.get('Ground', ''),
                match.get('Match_Date', '')
            ))

        self.loading_label.config(text="")

def main():
    root = tk.Tk()
    app = IPLMatchResultsDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
