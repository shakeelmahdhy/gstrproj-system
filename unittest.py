import unittest
from main import GreenStarProject, BarChart, LineChart, PieChart, ScatterPlot, DataHandler

class TestGreenStarProject(unittest.TestCase):
    def setUp(self):
        self.project = GreenStarProject("Test Project", "Test Location", "01/01/2022", "01/01/2023", "Test Tool", 5)

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.location, "Test Location")
        self.assertEqual(self.project.registered_date, "01/01/2022")
        self.assertEqual(self.project.certified_date, "01/01/2023")
        self.assertEqual(self.project.rating_tool, "Test Tool")
        self.assertEqual(self.project.rating, 5)

class TestDataHandler(unittest.TestCase):
    def setUp(self):
        self.file = 'test_projects.pkl'
        self.handler = DataHandler()

    def test_serialize_deserialize(self):
        projects = [
            GreenStarProject("Test Project 1", "Test Location", "01/01/2022", "01/01/2023", "Test Tool", 5)
        ]
        for project in projects:
            self.handler.add_project(project)

        self.handler.serialize(self.file)
        deserialized_handler = DataHandler()
        deserialized_handler.deserialize(self.file)
        deserialized_projects = deserialized_handler.get_projects()

        self.assertEqual(len(deserialized_projects), 1)
        self.assertEqual(deserialized_projects[0].name, "Test Project 1")

class TestVisualizations(unittest.TestCase):
    def setUp(self):
        self.projects = [
            GreenStarProject("Project 1", "Location 1", "01/01/2022", "01/01/2023", "Tool 1", 5),
            GreenStarProject("Project 2", "Location 2", "01/01/2021", "01/01/2022", "Tool 2", 6)
        ]

    def test_bar_chart(self):
        chart = BarChart(self.projects)
        chart.visualize()

    def test_line_chart(self):
        chart = LineChart(self.projects)
        chart.visualize()

    def test_pie_chart(self):
        chart = PieChart(self.projects)
        chart.visualize()

    def test_scatter_plot(self):
        chart = ScatterPlot(self.projects)
        chart.visualize()

    def test_visualization_title(self):
        chart = BarChart(self.projects, title="Test Title")
        chart.visualize()

    def test_visualization_save_path(self):
        chart = BarChart(self.projects, save_path="test_chart.jpg")
        chart.visualize()

if __name__ == '__main__':
    unittest.main()
