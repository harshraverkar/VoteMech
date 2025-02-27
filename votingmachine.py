import os
from passlib.hash import grub_pbkdf2_sha512
import tkinter as tk
from tkinter import messagebox, simpledialog


MAX_CANDIDATES = 5
electionEnded = False
votedUsers = [""] * MAX_CANDIDATES

# Define candidates
candidates = ["GAUTAM", "HARSH", "ANIKET", "ANISH", "NONE OF THESE"]

root = tk.Tk()
root.title("Election Voting System")

# Define custom colorsw
bg_color = "white"
button_color = "lightgrey"
exit_button_color = "yellow"

# Configure the root window
root.configure(bg=bg_color)

# Set the window size
root.geometry("1500x1300")  # Adjusted window size

# Load background and logo images
background_image = tk.PhotoImage(file="C:/Users/harsh/OneDrive/Desktop/vs code/voting/voting.png")  # Replace with your background image path
logo_image = tk.PhotoImage(file="C:/Users/harsh/OneDrive/Desktop/vs code/voting/logo.png")  # Replace with your logo image path

def display_background():
    background_label = tk.Label(root, image=background_image, bg=bg_color)
    background_label.place(x=0, y=80, relwidth=1, relheight=1)

def display_logo():
    logo_label = tk.Label(root, image=logo_image, bg=bg_color)
    logo_label.place(x=355, y=10)  # Adjust logo position

def display_decorative_patterns():
    decorative_frame = tk.Frame(root, bg=bg_color)
    decorative_frame.pack()
    tk.Label(decorative_frame, text="********************************************", bg=bg_color, font=("Helvetica", 10)).pack()
    tk.Label(decorative_frame, text="*     ELECTION FOR CLASS REPRESENTATIVE   *", bg=bg_color, font=("Helvetica", 12, "bold")).pack()
    tk.Label(decorative_frame, text="*          SECOND YEAR D DIVISION         *", bg=bg_color, font=("Helvetica", 10)).pack()
    tk.Label(decorative_frame, text="*                                         *", bg=bg_color, font=("Helvetica", 10)).pack()
    tk.Label(decorative_frame, text="********************************************", bg=bg_color, font=("Helvetica", 10)).pack()

def display_motivational_quotes():
    # You can customize the quotes or load them from a file
    quotes = [
        "Your vote is your voice!",
        "Make your choice count.",
    ]

    quotes_frame = tk.Frame(root, bg=bg_color)
    quotes_frame.pack()

    for quote in quotes:
        tk.Label(quotes_frame, text=quote, bg=bg_color, font=("Bold", 12)).pack()

logged_in_users = {}

def authenticate_user():
    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

        # Check if the user has already voted or is logged in
        if username in logged_in_users:
            if logged_in_users[username]:
                messagebox.showerror("Error", "You have already voted.")
                login_window.destroy()
                return

        with open("database.txt", "r") as db:
            user_credentials = [line.split(",") for line in db]

        for user, stored_password in user_credentials:
            if username == user:
                stored_password = stored_password.strip().strip("b'").strip("'")

                if grub_pbkdf2_sha512.verify(password, stored_password):
                    messagebox.showinfo("Success", "Login successful!")
                    logged_in_users[username] = True  # Mark user as logged in
                    login_window.destroy()
                    user_functions(username)
                    return

        messagebox.showerror("Error", "Invalid username or password. Access denied!")

    login_window = tk.Toplevel(root)
    login_window.title("User Login")
    login_window.configure(bg=bg_color)

    tk.Label(login_window, text="Enter your username:", bg=bg_color).pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Enter your Password:", bg=bg_color).pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=submit_login, bg=button_color)
    login_button.pack(pady=5)  # Add some space between the buttons

def authenticate_admin():
    def submit_admin_login():
        admin_username = admin_username_entry.get()
        admin_password = admin_password_entry.get()

        with open("admin_credentials.txt", "r") as admin_file:
            for line in admin_file:
                file_username, file_password = line.strip().split(":")
                if admin_username == file_username and admin_password == file_password:
                    messagebox.showinfo("Success", "Admin login successful!")
                    admin_login_window.destroy()
                    admin_functions()
                    return

        messagebox.showerror("Error", "Invalid admin username or password. Access denied!")

    admin_login_window = tk.Toplevel(root)
    admin_login_window.title("Admin Login")
    admin_login_window.configure(bg=bg_color)

    tk.Label(admin_login_window, text="Enter your username:", bg=bg_color).pack()
    admin_username_entry = tk.Entry(admin_login_window)
    admin_username_entry.pack()

    tk.Label(admin_login_window, text="Enter your password:", bg=bg_color).pack()
    admin_password_entry = tk.Entry(admin_login_window, show="*")
    admin_password_entry.pack()

    admin_login_button = tk.Button(admin_login_window, text="Login", command=submit_admin_login, bg=button_color)
    admin_login_button.pack(pady=5)  # Add some space between the buttons

def read_candidate_qualities():
    qualities = []
    with open("candidate_qualities.txt", "r") as file:
        for line in file:
            quality = line.strip()
            qualities.append(quality)
    return qualities

def user_functions(username):
    global electionEnded
    if electionEnded:
        messagebox.showerror("Error", "The election has ended. You cannot cast a vote at this time.")
        return

    user_voting_window = tk.Toplevel(root)
    user_voting_window.title("User Voting Page")
    user_voting_window.configure(bg=bg_color)

    tk.Label(user_voting_window, text="Welcome, " + username, bg=bg_color).pack()

    while True:
        user_identifier = simpledialog.askinteger("User Identifier", "Enter your Roll no:")
        if user_identifier is None:
            # The user canceled the input dialog
            return

        if user_identifier > 75:
            messagebox.showerror("Error", "Roll no should not exceed 75.")
        else:
            break

    if user_identifier in votedUsers:
        messagebox.showerror("Error", "You have already voted.")
        return

    def vote(candidate):
        candidate_index = candidates.index(candidate)
        votes[candidate_index] += 1
        votedUsers[votedUsers.index("")] = user_identifier
        messagebox.showinfo("Success", f"Vote for {candidate} cast successfully!")

    qualities = read_candidate_qualities()

    for candidate, quality in zip(candidates, qualities):
        tk.Label(user_voting_window, text=f"{candidate}: {quality}", bg=bg_color).pack()
        vote_button = tk.Button(user_voting_window, text=f"Vote for {candidate}", command=lambda c=candidate: vote(c), bg=button_color)
        vote_button.pack()


def admin_functions():
    global electionEnded
    if electionEnded:
        messagebox.showerror("Error", "The election has ended. You cannot access the admin dashboard at this time.")
        return

    admin_dashboard_window = tk.Toplevel(root)
    admin_dashboard_window.title("Admin Dashboard")
    admin_dashboard_window.configure(bg=bg_color)

    tk.Label(admin_dashboard_window, text="Election Results:", bg=bg_color, font=("Helvetica", 12, "bold")).pack()
    for i, candidate in enumerate(candidates):
        tk.Label(admin_dashboard_window, text=f"{candidate}: {votes[i]} votes", bg=bg_color).pack()

    leading_candidate = candidates[votes.index(max(votes))]
    tk.Label(admin_dashboard_window, text=f"Leading Candidate: {leading_candidate}", bg=bg_color).pack()

    end_election_button = tk.Button(admin_dashboard_window, text="End Election", command=update_election_status, bg=button_color)
    end_election_button.pack(pady=5)

# Function to update election status
def update_election_status():
    global electionEnded
    electionEnded = not electionEnded

    if electionEnded:
        winner = candidates[votes.index(max(votes))]
        messagebox.showinfo("Election Ended", f"The election has ended. The winner is {winner}.")
    else:
        messagebox.showinfo("Success", "The election is still in progress.")

# Load the logo and display decorative patterns
display_background()
display_logo()
display_decorative_patterns()
display_motivational_quotes()

# Create a list of votes
votes = [0] * MAX_CANDIDATES

# Create a frame for options
options_frame = tk.Frame(root, bg=bg_color)
options_frame.pack()

# Create buttons for various functions
tk.Label(options_frame, text="Select an option:", bg=bg_color, font=("Helvetica", 12, "bold")).pack()
login_button = tk.Button(options_frame, text="User Login and Vote", command=authenticate_user, bg=button_color)
admin_login_button = tk.Button(options_frame, text="Admin Login and Access Dashboard", command=authenticate_admin, bg=button_color)
exit_button = tk.Button(options_frame, text="Exit", command=root.destroy, bg=exit_button_color)

# Pack buttons and add space
login_button.pack(pady=10)
admin_login_button.pack(pady=10)
exit_button.pack(pady=10)

root.mainloop()
