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


def getOfficerBio(name):
    bioTags = {
        'Julian': "0kFzv1fjg1CvGGpbgLH8w",
        'MaKenzie': "lGCdEYxRZ2WxD9lVcgtOG",
        'Blanca': "704Yncda3h4nLVwm7TX8p0",
        'Michelle': "1Okz31RuR8ivPBfhFuAA5h",
        'Kimberly': "7622yy2YW1hTI6HA8FEE9d"
    }

    info = client.entry(bioTags[name])

    return info


def getBlogPosts():
    posts = client.entries(
        {'content_type': 'blogPost', 'order': 'fields.date'})

    postList = []

    for post in posts:
        postInfo = {}

        postInfo['title'] = post.title
        postInfo['author'] = post.author
        postInfo['text'] = post.text
        postInfo['type'] = post.type
        postInfo['media'] = post.media.url()

        postList.append(postInfo)

    return postList


siteName = getSiteName()
officers = getOfficers()
posts = getBlogPosts()


@app.route("/")
def index():
    events = getEvents()

    return render_template('index.html', name=siteName, events=events)


@app.route("/about", defaults={'officer_name': None})
@app.route("/about/<officer_name>")
def about(officer_name):
    if not officer_name:
        return render_template('about.html', name=siteName, officers=officers)

    info = getOfficerBio(officer_name)

    return render_template('profile.html', name=siteName, officer_name=officer_name, info=info)


@app.route("/blog")
def blog():
    return render_template('blog.html', name=siteName, posts=posts)


@app.route("/resources")
def resources():
    return "Resources"
    #  return render_template('blog.html', name=siteName, officers=officers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
