import json

from flask import Flask, request, render_template
from flask.ext.restful import Api, Resource, reqparse, abort

from lib.resource import user, system, session, beer, spstyp
import conf
from log import applog

spsconf = conf.SpsConf()
app = Flask(__name__)
api = Api(app)


#User Endpoints
api.add_resource(user.User,
                 "/user", "/user/<int:userid>")
api.add_resource(user.UserToken,
                 "/user/login", "/user/logout", "/user/token")
#Session Endpoints
api.add_resource(session.Session,
                 "/session","/session/<int:sessionid>")

api.add_resource(session.SessionUser,
                 "/session/<int:sessionid>/user",
                 "/session/<int:sessionid>/user/<int:userid>")

api.add_resource(session.SessionBeer,
                 "/session/<int:sessionid>/beer",
                 "/session/<int:sessionid>/beer/<int:sessionbeerid>")

api.add_resource(session.SessionBeerRating,
                 "/session/<int:sessionid>/beer/<int:sessionbeerid>/rating",
                 "/session/<int:sessionid>/beer/<int:sessionbeerid>/rating/<int:beerratingid>")

api.add_resource(session.SessionEvent,
                 "/session/<int:sessionid>/event")

#Beer
api.add_resource(beer.Beer,
                 "/beer","/beer/<string:beerid>")

api.add_resource(beer.Brewery,
                 "/brewery","/brewery/<string:breweryid>")

api.add_resource(beer.Search,
                 "/beer/search",
                 "/brewery/search")

#Basic info Endpoints
api.add_resource(system.System, "/system")
api.add_resource(spstyp.RatingVal, "/ratingval")
api.add_resource(spstyp.RatingTyp, "/ratingtyp")
api.add_resource(spstyp.SessionStatusTyp, "/sessionstatustyp")
api.add_resource(spstyp.UserRoleTyp, "/userroletyp")
api.add_resource(spstyp.BeerSessionStatusTyp,
                 "/beersessionstatustyp")

@app.route("/")
def index():
    """
    Indexs
    """
    return render_template('index.html')

@app.route("/shutdown", methods=["POST"])
def shutdown():
    #NOTE: This method should only be enabled
    #when the application is being tested
    if spsconf.testing:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            applog.debug("App is not being hosted by werkzeug. Skipping shutting down.")
            msg = {
                "status": "ERR",
                "message": "Not running with werzkeug server"
            }
        else:
            applog.info("Shuting down app server")
            func()
            msg = { "status": "OK" }
        return json.dumps(msg)
    else:
        applog.debug("App not in testing mode. Skipping shuting down server")
        msg = {
            "status": "ERR",
            "message": "Application not in testing mode"
        }
        return json.dumps(msg)

if __name__ == "__main__":
    applog.info("Starting dev server")
    applog.info("Port: %s" % spsconf.rest_port)
    applog.info("Debug: %s" % spsconf.debug)
    applog.info("Testing: %s" % spsconf.testing)
    applog.info("No Tokens: %s" % spsconf.notokens)
    app.run(debug=spsconf.debug,
            port=spsconf.rest_port)

