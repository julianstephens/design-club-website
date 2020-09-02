from flask import Flask, render_template
from flask_assets import Environment, Bundle
import contentful


app = Flask(__name__)

# Configure flask assets for sass
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('_variables.scss', 'main.scss',
              filters='pyscss', output='main.css')
assets.register('scss_all', scss)


# Load custom config
app.config.from_object("config.Config")

# Connect to contentful client
client = contentful.Client(
    app.config["CONTENTFUL_SPACEID"], app.config["CONTENTFUL_ACCESSKEY"])


def getSiteName():
    """Retrieves site name from contentful

    Returns:
        string: Site name
    """
    entry_id = '1EngZagyUcVRislD4wINfw'
    name = client.entry(entry_id)
    return name.text


def getEvents():
    """Retrieves all events from contentful

    Returns:
        list: Events in order from oldest to newest
    """
    events = client.entries(
        {'content_type': 'event', 'order': 'fields.date'})

    eventList = []

    for event in events:
        eventList.append(event.name)

    return eventList


def getOfficers():
    """Retrieves officers from contentful

    Returns:
        dict: Officer info in rank order
    """
    officers = client.entries(
        {'content_type': 'officers', 'order': 'fields.order'})

    officerList = []

    for officer in officers:
        officerInfo = {}

        officerInfo['name'] = officer.name
        officerInfo['bio'] = officer.bio
        officerInfo['photo'] = officer.photo
        officerInfo['position'] = officer.position

        officerList.append(officerInfo)

    return officerList


siteName = getSiteName()
officers = getOfficers()


@app.route("/")
def home():
    events = getEvents()

    return render_template('index.html', name=siteName, events=events)


@app.route("/about")
def about():
    return render_template('about.html', name=siteName, officers=officers)


@app.route("/blog")
def blog():
    return "Blog"
    #  return render_template('blog.html', name=siteName, officers=officers)


@app.route("/resources")
def resources():
    return "Resources"
    #  return render_template('blog.html', name=siteName, officers=officers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
