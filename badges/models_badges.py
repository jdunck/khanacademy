#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.appengine.ext import db

class UserBadge(db.Model):
    user = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    badge_name = db.StringProperty()
    target_context = db.ReferenceProperty()
    target_context_name = db.StringProperty()

    @staticmethod
    def get_for(user):
        query = UserBadge.all()
        query.filter('user =', user)
        query.order('badge_name')
        query.order('-date')
        return query.fetch(1000)
