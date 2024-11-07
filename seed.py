from app import create_app, db
from app.models.goal import Goal
from app.models.task import Task

my_app = create_app()
with my_app.app_context():
    
    goal1 = Goal(title="Build productive habits")
    goal2 = Goal(title="Develop coding skills")
    goal3 = Goal(title="Become a better ally")

    db.session.add_all([goal1, goal2, goal3])
    db.session.commit()

    task1 = Task(title="Complete Python exercise", description="Practice loops and conditionals", goal=goal2)
    task2 = Task(title="Build portfolio project", description="Set up initial HTML, CSS files", goal=goal2)
    task3 = Task(title="Read up on RESTful APIs", description="Go over RESTful API documentation", goal=goal2)

    task4 = Task(title="Morning walk", description="Take a short walk for a break", goal=goal1)
    task5 = Task(title="Journal for 5 minutes", description="Reflect on daily goals and progress", goal=goal1)
    task6 = Task(title="Get 8 hours of sleep", description="Focus on rest for better productivity", goal=goal1)

    task7 = Task(title="Attend allyship workshop", description="Participate in LGBTQIA+ ally training", goal=goal3)
    task8 = Task(title="Read educational resources", description="Learn about POC and gender-expansive experiences", goal=goal3)
    task9 = Task(title="Support LGBTQIA+ creators", description="Purchase or share content from LGBTQIA+ creators", goal=goal3)
    task10 = Task(title="Volunteer with advocacy groups", description="Offer support to LGBTQIA+ and POC organizations", goal=goal3)

    db.session.add_all([task1, task2, task3, task4, task5, task6, task7, task8, task9, task10])
    db.session.commit()