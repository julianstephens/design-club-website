from flask import Flask, render_template
#  from flask.ext.scss import Scss
import contentful


app = Flask(__name__)
app.config.from_object("config.Config")
client = contentful.Client(
    app.config["CONTENTFUL_SPACEID"], app.config["CONTENTFUL_ACCESSKEY"])


def getSiteName():
    entry_id = '1EngZagyUcVRislD4wINfw'
    name = client.entry(entry_id)
    return name.text


def getEvents():
    events = client.entries(
        {'content_type': 'event', 'order': 'fields.date'})

    eventList = []

    for event in events:
        eventList.append(event.name)

    return eventList


def getNav():
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
