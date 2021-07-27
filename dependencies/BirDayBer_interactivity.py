import dependencies.BirDayBer_interfaceStructure as BirDayber_structure
import tkinter.messagebox as messagebox
import tkinter as tk
import webbrowser


class BirDayBer_interactivity(BirDayber_structure.Interface_structure):
    """
    Class that manages the interactivity of the BirDayBer's client.
    """
    def __init__(self):
        """
        It assign all events to buttons and it loads all
        people from the database in the 'people_viewer' method.
        """
        super().__init__()

        self.settings_state = False
        self.button_commands()
        self.model_people()
        # self.refresh_people_viewer()
        # self.refresh_today_birthdays()

    def button_commands(self):
        """
        This method assigns commands to each button of the client.
        """
        self.minimize_button.config(command=self.title_bar_minimize)
        # self.maximize_button.config(command=self.title_bar_maximize) Later...
        self.close_button.config(command=self.close_client)
        self.license_icon.config(command=self.show_license)
        self.about_icon.config(command=self.open_about)
        self.github_icon.config(command=self.open_github)
        self.twitter_icon.config(command=self.open_twitter)
        self.nut_icon.config(command=self.open_settings)

    def show_license(self):
        return messagebox.showinfo(
            "BirDayBer License",
            f"{self.get_license()[0]}\n{self.get_license()[1]}")

    def open_about(self):
        return messagebox.showinfo("About BirDayBer", self.get_version())

    def open_github(self):
        self.github_icon.config(command=self.open_github)
        webbrowser.open("https://github.com/LucioFex")

    def open_twitter(self):
        self.twitter_icon.config(command=self.open_twitter)
        webbrowser.open("https://twitter.com/LucioFex")

    def model_people(self):  # Just a test method (delete later)
        self.row_person_border = tk.Frame(self.people_finder, bg="#79c1db")
        self.row_person = tk.Frame(self.row_person_border, bg="#8fd0e7")
        self.row_person_img = tk.Button(
            self.row_person, image=self.person_default_src)

        self.row_person_border.grid(row=0, column=0)
        self.row_person.pack()
        self.row_person_img.pack()
