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


def getNav():
    """Retrieves nav items from contentful

    Returns:
        list: Nav items in display order
    """
    navItems = client.entries(
        {'content_type': 'navBar', 'order': 'fields.order'})

    navList = []

    for nav in navItems:
        navList.append(nav.item)

    return navList


@app.route("/")
def home():
    siteName = getSiteName()
    events = getEvents()
    nav = getNav()

    return render_template('index.html', name=siteName, events=events, navItems=nav)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
