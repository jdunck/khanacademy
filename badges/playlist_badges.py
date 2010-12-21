from models import UserPlaylist
from badges import Badge, BadgeContextType, BadgeCategory

# All badges that may be awarded once-per-Playlist inherit from PlaylistBadge
class PlaylistBadge(Badge):

    def __init__(self):
        Badge.__init__(self)
        self.badge_context_type = BadgeContextType.PLAYLIST

    def is_already_owned_by(self, user_data, *args, **kwargs):
        user_playlist = kwargs.get("user_playlist", None)
        if user_playlist is None:
            return False

        return self.name_with_target_context(UserPlaylist.playlist.get_value_for_datastore(user_playlist)) in user_data.badges

    def award_to(self, user, user_data, *args, **kwargs):
        user_playlist = kwargs.get("user_playlist", None)
        if user_playlist is None:
            return False

        self.complete_award_to(user, user_data, user_playlist.playlist, UserPlaylist.playlist.get_value_for_datastore(user_playlist))

