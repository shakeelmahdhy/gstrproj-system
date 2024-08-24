import matplotlib.pyplot as plt
from datetime import datetime
import pickle


class GreenStarProject:
    def __init__(self, name, location, registered_date, certified_date, rating_tool, rating):
        self.name = name
        self.location = location
        self.registered_date = registered_date
        self.certified_date = certified_date
        self.rating_tool = rating_tool
        self.rating = rating


class Visualization:
    def __init__(self, data, title=None, save_path=None):
        self.data = data
        self.title = title
        self.save_path = save_path

    def visualize(self):
        raise NotImplementedError("Subclasses should implement this!")

    def apply_title(self):
        if self.title:
            plt.title(self.title)

    def save_plot(self):
        if self.save_path:
            plt.savefig(self.save_path)
            print(f"Chart saved as {self.save_path}")

class BarChart(Visualization):
    def visualize(self):
        names = [project.name for project in self.data]
        ratings = [int(project.rating) if project.rating != 'NA' else 0 for project in self.data]
        plt.barh(names, ratings, height=0.5)
        plt.xlabel('Project')
        plt.ylabel('Rating')
        plt.title('Project - Green Star Ratings')
        self.save_plot()
        plt.show()

class ScatterPlot(Visualization):
    def visualize(self):
        certified_dates = [datetime.strptime(project.certified_date, '%d/%m/%Y') for project in self.data]
        names = [project.name for project in self.data]

        plt.scatter(certified_dates, names)
        plt.xlabel('Certified Date')
        plt.ylabel('Project')
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.save_plot()
        plt.show()

class LineChart(Visualization):
    def visualize(self):
        names = [project.name for project in self.data]
        registered_dates = [datetime.strptime(project.registered_date, '%d/%m/%Y') for project in self.data]
        certified_dates = [datetime.strptime(project.certified_date, '%d/%m/%Y') for project in self.data]

        plt.plot(registered_dates, names, color='g', marker='*', label='Registered Date')
        plt.plot(certified_dates, names, color='c', marker='o', label='Certified Date')
        plt.xlabel('Date')
        plt.ylabel('Company')
        plt.title('Registered and Certified Dates of Green Star Projects')
        plt.legend()
        self.save_plot()
        plt.show()


class PieChart(Visualization):
    def visualize(self):
        rating_tools = [project.rating_tool for project in self.data]
        tool_counts = {tool: rating_tools.count(tool) for tool in set(rating_tools)}
        labels = list(tool_counts.keys())
        counts = list(tool_counts.values())
        plt.pie(counts, labels=labels, autopct='%1.1f%%')
        plt.title('Distribution of Rating Tools Used')
        self.save_plot()
        plt.show()


class DataHandler:
    def __init__(self):
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def serialize(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.projects, f)

    def deserialize(self, file_path):
        if not self.checkLoad(file_path):
            print("Error: Please provide a valid .pkl file path.")
            return
        try:
            with open(file_path, 'rb') as f:
                self.projects = pickle.load(f)
                print("Project loaded successfully!")
        except EOFError:
            print("Error: Unable to deserialize data from file. The file might be corrupted or empty.")
            self.projects = []

    @staticmethod
    def checkLoad(file_path):
        if not file_path.endswith(".pkl"):
            return False

        try:
            with open(file_path, 'rb'):
                pass
        except FileNotFoundError:
            return False
        return True

    def get_projects(self):
        return self.projects


if __name__ == "__main__":
    handler = DataHandler()

    while True:
        print("1. Add new project")
        print("2. Visualize projects")
        print("3. Save projects to file")
        print("4. Load projects from file")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
                name = input("Enter project name: ")
                location = input("Enter project location: ")

                while True:
                    registered_date = input("Enter registered date (dd/mm/yyyy): ")
                    try:
                        datetime.strptime(registered_date, '%d/%m/%Y')
                        break  # Break out of the loop if no ValueError occurs
                    except ValueError:
                        print("Please enter date in the valid format dd/mm/yyyy:")

                while True:
                    certified_date = input("Enter certified date (dd/mm/yyyy): ")
                    try:
                        datetime.strptime(certified_date, '%d/%m/%Y')
                        break  # Break out of the loop if no ValueError occurs
                    except ValueError:
                        print("Please enter date in the valid format dd/mm/yyyy:")

                rating_tool = input("Enter rating tool: ")
                while True:
                    rating = input("Enter rating (or 'NA' if not available): ")
                    if rating != 'NA':
                        if rating.isdigit():
                            rating = int(rating)
                            break
                        else:
                            print("Please enter a valid integer as rating! ")

                new_project = GreenStarProject(name, location, registered_date, certified_date, rating_tool, rating)
                handler.add_project(new_project)
                print("Project added successfully!")
        elif choice == '2':
            print("""
            Select visualization type: 
            1. Bar Chart 
            2. Line Chart 
            3. Pie Chart
            4. Scatter Plot
            5. Exit""")
            vis_type = int(input("Enter the number corresponding to your choice: "))
            if vis_type == 1:
                title = "Project - Green Star Ratings"
                save_path = "barChart.jpg"
                visualization = BarChart(handler.get_projects(), title=title, save_path=save_path)
            elif vis_type == 2:
                title = "Registered and Certified Dates of Green Star Projects"
                save_path = "lineChart.jpg"
                visualization = LineChart(handler.get_projects(), title=title, save_path=save_path)
            elif vis_type == 3:
                title = "Distribution of Rating Tools Used"
                save_path = "pieChart.jpg"
                visualization = PieChart(handler.get_projects(), title=title, save_path=save_path)
            elif vis_type == 4:
                title = "Certified Date vs Project"
                save_path = "scatterPlot.jpg"
                visualization = ScatterPlot(handler.get_projects(), title=title, save_path=save_path)
            elif vis_type == 5:
                print("Exiting...")
                break
            else:
                print("Invalid choice")
                continue
            visualization.visualize()
        elif choice == '3':
            file_path = input("Enter file path to save projects: ")
            handler.serialize(file_path)
            print("Projects saved successfully!")
        elif choice == '4':
            print("Use 'projects.pkl' to test, I've uploaded it to test the functionality.")
            file_path = input("Enter file path to load projects [USE 'projects.pkl' to test]: ")
            handler.deserialize(file_path)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
