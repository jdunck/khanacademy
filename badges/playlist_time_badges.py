import util

from badges import Badge, BadgeContextType, BadgeCategory
from playlist_badges import PlaylistBadge

# All badges awarded for watching a specific amount of playlist time inherit from PlaylistTimeBadge
class PlaylistTimeBadge(PlaylistBadge):

    def is_satisfied_by(self, *args, **kwargs):
        user_playlist = kwargs.get("user_playlist", None)

        if user_playlist is None:
            return False

        return user_playlist.seconds_watched >= self.seconds_required

    def extended_description(self):
        return "Watch %s of video in a single playlist" % util.seconds_to_clock_format(self.seconds_required)

class NicePlaylistTimeBadge(PlaylistTimeBadge):
    def __init__(self):
        self.seconds_required = 60 * 15
        self.description = "Nice Listener"
        self.badge_category = BadgeCategory.BRONZE
        self.points = 100
        PlaylistTimeBadge.__init__(self)

class GreatPlaylistTimeBadge(PlaylistTimeBadge):
    def __init__(self):
        self.seconds_required = 60 * 30
        self.description = "Great Listener"
        self.badge_category = BadgeCategory.BRONZE
        self.points = 1000
        PlaylistTimeBadge.__init__(self)

class AwesomePlaylistTimeBadge(PlaylistTimeBadge):
    def __init__(self):
        self.seconds_required = 60 * 60
        self.description = "Awesome Listener"
        self.badge_category = BadgeCategory.SILVER
        self.points = 4500
        PlaylistTimeBadge.__init__(self)

class RidiculousPlaylistTimeBadge(PlaylistTimeBadge):
    def __init__(self):
        self.seconds_required = 60 * 60 * 4
        self.description = "Ridiculous Listener"
        self.badge_category = BadgeCategory.GOLD
        self.points = 10000
        PlaylistTimeBadge.__init__(self)

class LudicrousPlaylistTimeBadge(PlaylistTimeBadge):
    def __init__(self):
        self.seconds_required = 60 * 60 * 10
        self.description = "Ludicrous Listener"
        self.badge_category = BadgeCategory.PLATINUM
        self.points = 25000
        PlaylistTimeBadge.__init__(self)
