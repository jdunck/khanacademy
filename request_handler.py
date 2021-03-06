import os
import logging
import datetime
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

import util
from app import App
from models import UserData

class RequestHandler(webapp.RequestHandler):

    def request_string(self, key, default = ''):
        return self.request.get(key, default_value=default)

    def request_int(self, key, default = None):
        try:
            return int(self.request_string(key))
        except ValueError:
            if default is not None:
                return default
            else:
                raise # No value available and no default supplied, raise error

    def request_date(self, key, format_string, default = None):
        try:
            return datetime.datetime.strptime(self.request_string(key), format_string)
        except ValueError:
            if default is not None:
                return default
            else:
                raise # No value available and no default supplied, raise error

    def request_float(self, key, default = None):
        try:        
            return float(self.request_string(key))
        except ValueError:
            if default is not None:
                return default
            else:
                raise # No value available and no default supplied, raise error

    def request_bool(self, key, default = None):
        if default is None:
            return self.request_int(key) == 1
        else:
            return self.request_int(key, 1 if default else 0) == 1

    def is_ajax_request(self):
        # jQuery sets X-Requested-With header for this detection.
        if self.request.headers.has_key("x-requested-with"):
            s_requested_with = self.request.headers["x-requested-with"]
            if s_requested_with and s_requested_with.lower() == "xmlhttprequest":
                return True
        return self.request_bool("is_ajax_override", default=False)

    def request_url_with_additional_query_params(self, params):
        url = self.request.url
        if url.find("?") > -1:
            url += "&"
        else:
            url += "?"
        return url + params

    def handle_exception(self, e, *args):

        message = "We ran into a problem. It's our fault, and we're working on it."
        if type(e) is CapabilityDisabledError:
            message = "We're temporarily down for maintenance. Try again in about an hour. We're sorry for the inconvenience."

        webapp.RequestHandler.handle_exception(self, e, args)

        # Never show stack traces on production machines
        if not App.is_dev_server:
            self.response.clear()

        self.render_template('viewerror.html', {"message": message})

    def user_agent(self):
        return str(self.request.headers['User-Agent'])

    def redirect_via_refresh_if_webkit(self, location):
        if self.user_agent().lower().find("webkit") > -1:
            # When WebKit issues a 302 redirect after a POST request,
            # all previously cached static content (images, scripts, the whole kit'n'kaboodle)
            # is cleared from cache and re-retrieved. Until it's fixed, we'll avoid this WebKit-only 
            # bug by using a Refresh header.
            #
            # https://bugs.webkit.org/show_bug.cgi?id=38690
            # http://stackoverflow.com/questions/4301405/webkit-image-reload-on-post-redirect-get
            # http://www.google.com/support/forum/p/Chrome/thread?tid=72bf3773f7e66d68&hl=en
            #
            self.response.headers.add_header("Refresh", "0; URL=%s" % location)
        else:
            self.redirect(location)

    def render_template(self, template_name, template_values):
        template_values['App'] = App
        template_values['None'] = None
        template_values['points'] = None
        template_values['username'] = ""
        user = util.get_current_user()
        if user is not None:
            template_values['username'] = user.nickname()            
        user_data = UserData.get_for(user)

        template_values['user_data'] = user_data
        template_values['points'] = user_data.points if user_data else 0

        template_values['login_url'] = util.create_login_url(self.request.uri)
        template_values['logout_url'] = users.create_logout_url(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), template_name)
        self.response.out.write(template.render(path, template_values))
 
