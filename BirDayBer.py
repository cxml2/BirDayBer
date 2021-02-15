import db_manager
import tkinter as tk
from PIL import Image
import os


def wrong_input_type(desired, acquired):
    """
    Function that raises a ValueError because of the data type given.
    """
    raise ValueError(
        "add_person method only expects as a parameter a " +
        "%s, but a %s was recieved." % (desired, acquired))


class Birdayber_database:
    """
    This class is specialized in the generation and maintenance
    of the DB and get data of the project's LICENSE.
    """
    def __init__(self, db_connection, mainloop):
        """
        Method that only accepts a sqlite3 database lotaction and Boolean:
        Creation of the database and preparation to generate the interface.
        If the second parameter is 'True' the program will start main-looping.
        """
        #  Db management and generation:
        if os.path.exists(db_connection) is False:  # If there's not db
            self.generate_database(db_connection)
        self.db = db_manager.Db_manager(db_connection)  # If there's a db

    def get_license(self):
        """
        This method returns the type of BirDayBer project's license,
        the duration of this one and the name of its creator.
        """
        license_type = []
        with open("LICENSE", "r", encoding="utf-8") as license_data:
            license_type.append(license_data.readlines()[0][0:-1])
            license_data.seek(0)
            license_type.append(license_data.readlines()[2][0:-1])

        return tuple(license_type)

    def generate_database(self, db_connection):
        """
        Method that only accepts sqlite3 database locations:
        Generation of the database connection and tables.
        The generation of the tables is pre-created.
        """
        self.db = db_manager.Db_manager(db_connection)
        id_type = "INTEGER PRIMARY KEY AUTOINCREMENT"

        self.db.create_table({
            "genders":
                f"""id_gender {id_type},
                gender VARCHAR(6) NOT NULL""",
            "photos":
                f"""id_photo {id_type},
                photo BLOB""",
            "countries":
                f"""id_country {id_type},
                country VARCHAR(40)""",
            "births":
                f"""id_birth {id_type},
                birth DATE NOT NULL,
                age INTEGER""",

            "people":
                f"""id_person {id_type},
                per_first VARCHAR(35) NOT NULL,
                per_last VARCHAR(35),
                id_country1_fk INTEGER NOT NULL,
                id_gender1_fk INTEGER NOT NULL,
                id_birth1_fk INTEGER NOT NULL,
                id_photo1_fk INTEGER NOT NULL,
                FOREIGN KEY (id_country1_fk) REFERENCES country (id_country),
                FOREIGN KEY (id_gender1_fk) REFERENCES gender (id_gender),
                FOREIGN KEY (id_birth1_fk) REFERENCES birth (id_birth),
                FOREIGN KEY (id_photo1_fk) REFERENCES photo (id_photo)"""})

        del id_type
        return db_connection

    def add_person(self, person):
        """
        Method that only accepts dicts:
        Addition of people to the database.
        Every key in the dictionary must be a String, like in the example.

        For example:
            self.add_person({
                "country": {"country": "United States"},
                "gender": {"gender": "Male"},
                "photo": {"photo": None},
                "birth": {"birth": "1919-12-23", "age": None},
                "person": {"per_first": "Randolph", "per_last": "Carter"}})
        """
        if type(person) == dict:  # Data type detector
            for row in person.items():
                if type(row[0]) != str:
                    wrong_input_type(str, type(row))
                elif type(row[1]) != dict:
                    wrong_input_type(dict, type(row))

            return self.db.add_rows(person)  # If all the data type is fine
        return wrong_input_type(dict, type(row))

    def get_people(self, id_person="&None%", binary=True):
        """
        Method that only accepts Str or Int:
        This method brings all the information of the people.
        The parameter "id" is part of a WHERE clause. If there's no WHERE
        given or "&None%" recieved, then all the data will be displayed.
        """
        if id_person != "&None%":
            id_person = "id_person = %s" % id_person

        if binary:
            select = "per_first, per_last, birth, age, photo, country, gender"
        elif binary is False:
            select = "per_first, per_last, birth, age, country, gender"

        people_data = self.db.column_search(
            "people", select,
            """INNER JOIN
                births on births.id_birth = people.id_birth1_fk
            INNER JOIN
                photos on photos.id_photo = people.id_photo1_fk
            INNER JOIN
                countries on countries.id_country = people.id_country1_fk
            INNER JOIN
                genders on genders.id_gender = people.id_gender1_fk""",
            id_person)

        return people_data

    def drop_database(self):
        """
        This method deletes the database file.
        """
        self.db.close_database()
        self.db.drop_database()

    def close_client(self):
        """
        It makes the program stop mainlooping.
        """
        self.db.close_database()
        self.window.destroy()


class Birdayber_client(Birdayber_database):
    """
    This class is specialized in the generation and maintenance of the UI.
    """
    def __init__(self, db_connection, mainloop=False):
        """
        If the 'mainloop' parameter is 'True' the program will main-loop.
        """
        super().__init__(db_connection, mainloop)
        self.window = tk.Tk()
        self.window_init_resolution()  # Set of the window screen resolution
        self.responsive_imgs()  # Generation of new responsive images
        self.titlebar_init()  # Generation of the new title bar
        self.window.mainloop() if mainloop else None

    def window_init_resolution(self):
        """
        This method returns the information of the best
        possible resolution and position for the client's window.
        Then it sets the new values in the root.geometry() function.
        """
        real_screen_width = self.window.winfo_screenwidth()
        real_screen_height = self.window.winfo_screenheight()

        self.screen_width = real_screen_width - round(real_screen_width / 4)
        self.screen_height = real_screen_height - round(real_screen_height / 4)

        self.x_position = round(real_screen_width / 7)
        self.y_position = round(real_screen_height / 7)

        self.window.geometry("%sx%s+%s+%s" % (
            self.screen_width, self.screen_height,
            self.x_position, self.y_position))

        self.window.update()
        return str(self.window.geometry)

    def responsive_imgs(self):
        """
        Method that modifies all the sizes of images and clone these in the
        BirDayBer's system to something more visible for the user.
        The new clones will be saved in the 'responsive' folder.
        """
        location = "bin//system_content//visual_content"
        files = next(os.walk(location))[2]

        for img in files:  # Refactor later
            if img in (  # Title bar section
                "close-button.png", "minimize-button.png",
                    "maximize-button.png", "maximized-button.png"):
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail((
                    round(self.screen_width * 4 / 100),
                    round(self.screen_height * 4.5 / 100)))
                responsive_img.save("%s//responsive//%s" % (location, img))

            elif img in ("BirDayBerIcon.png"):
                responsive_img = Image.open("%s//%s" % (location, img))
                responsive_img.thumbnail((
                    round(self.screen_width * 6.5 / 100),
                    round(self.screen_height * 6.5 / 100)))
                responsive_img.save("%s//responsive//%s" % (location, img))

    def titlebar_init(self):
        """
        Generation of the new Title Bar and elimination of the previous one.
        """
        self.window.overrideredirect(1)  # Deletion of the original Title Bar
        location = "bin//system_content//visual_content//responsive//"

        self.title_bar = tk.Frame(
            self.window, bg="#316477", height=round(self.screen_height / 20))
        self.title_bar.pack(fill="x")

        self.images = []
        for img in ("close-button.png", "maximize-button.png",
                    "minimize-button.png", "BirDayBerIcon.png"):
            self.images.append(tk.PhotoImage(file=location + img))

        buttons = ["x", "+", "-"]
        for index, button in enumerate(buttons):  # Generation of buttons
            buttons[index] = tk.Button(
                self.title_bar, image=self.images[index],
                bg="#2c5c6d", relief=tk.FLAT, bd=0, activebackground="#1e5061")
            buttons[index].pack(side=tk.RIGHT, ipadx=14, ipady=7)
        buttons[0].config(activebackground="#911722")

        self.icon = tk.Label(
            self.title_bar, image=self.images[3], bg="#316477")
        self.icon.pack(side=tk.LEFT)


if __name__ == '__main__':
    BirDayBer = Birdayber_client("bin//BirDayBer.db", True)
