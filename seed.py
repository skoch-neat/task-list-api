from app import create_app, db
from app.models.task import Task

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="Complete Python exercise", description="Practice loops and conditionals"))
    db.session.add(Task(title="Build portfolio project", description="Set up initial HTML, CSS files"))
    db.session.add(Task(title="Read up on REST APIs", description="Go over REST API documentation"))
    db.session.add(Task(title="Morning walk", description="Take a short walk for a break"))
    db.session.add(Task(title="Review Flask routing", description="Look at Flask app routing examples"))
    db.session.add(Task(title="Journal for 5 minutes", description="Reflect on daily goals and progress"))
    db.session.add(Task(title="Code review session", description="Participate in a peer code review"))
    db.session.add(Task(title="Build a CRUD app", description="Create a CRUD app with Flask and SQLAlchemy"))
    db.session.add(Task(title="Plan next sprint", description="Outline objectives for upcoming sprint"))
    db.session.add(Task(title="Get 8 hours of sleep", description="Focus on rest for better productivity"))
    db.session.add(Task(title="Watch tutorial on Git", description="Review branching and merging in Git"))
    db.session.add(Task(title="Stretch break", description="Take a stretch break every hour"))
    db.session.add(Task(title="Implement feature tests", description="Write and run tests for app features"))
    db.session.add(Task(title="Research CSS frameworks", description="Compare Bootstrap, Tailwind, etc."))
    db.session.add(Task(title="Organize code repo", description="Clean up folders and files in repo"))
    db.session.add(Task(title="Experiment with APIs", description="Make API calls to a public API"))
    db.session.add(Task(title="Set up Trello board", description="Organize projects on Trello for tracking"))
    db.session.add(Task(title="Daily meditation", description="Spend 10 minutes on meditation practice"))
    db.session.add(Task(title="Debug JavaScript code", description="Use console to debug JS app"))
    db.session.add(Task(title="Write a blog post", description="Document your progress and challenges"))
    db.session.commit()