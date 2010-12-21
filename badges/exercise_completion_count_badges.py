import models
from badges import Badge, BadgeContextType, BadgeCategory

# All badges awarded for completing some specific count of exercises inherit from ExerciseCompletionCountBadge
class ExerciseCompletionCountBadge(Badge):

    def is_satisfied_by(self, *args, **kwargs):
        user_data = kwargs.get("user_data", None)
        if user_data is None:
            return False

        return len(user_data.all_proficient_exercises) >= self.required_exercises

    def extended_description(self):
        return "Achieve proficiency in any %d exercises" % self.required_exercises

class GettingStartedBadge(ExerciseCompletionCountBadge):
    def __init__(self):
        ExerciseCompletionCountBadge.__init__(self)
        self.required_exercises = 3
        self.description = "Just Getting Started"
        self.badge_category = BadgeCategory.BRONZE
        self.points = 100

class MakingProgressBadge(ExerciseCompletionCountBadge):
    def __init__(self):
        ExerciseCompletionCountBadge.__init__(self)
        self.required_exercises = 7
        self.description = "Making Progress"
        self.badge_category = BadgeCategory.BRONZE
        self.points = 1000

class ProductiveBadge(ExerciseCompletionCountBadge):
    def __init__(self):
        ExerciseCompletionCountBadge.__init__(self)
        self.required_exercises = 15
        self.description = "Productive"
        self.badge_category = BadgeCategory.SILVER
        self.points = 2000

class HardAtWorkBadge(ExerciseCompletionCountBadge):
    def __init__(self):
        ExerciseCompletionCountBadge.__init__(self)
        self.required_exercises = 25
        self.description = "Hard at Work"
        self.badge_category = BadgeCategory.SILVER
        self.points = 8000

class WorkHorseBadge(ExerciseCompletionCountBadge):
    def __init__(self):
        ExerciseCompletionCountBadge.__init__(self)
        self.required_exercises = 40
        self.description = "Work Horse"
        self.badge_category = BadgeCategory.GOLD
        self.points = 12000

class MagellanBadge(ExerciseCompletionCountBadge):
    def __init__(self):
        ExerciseCompletionCountBadge.__init__(self)
        self.required_exercises = 80
        self.description = "Magellan"
        self.badge_category = BadgeCategory.PLATINUM
        self.points = 25000

class AtlasBadge(ExerciseCompletionCountBadge):
    def __init__(self):
        ExerciseCompletionCountBadge.__init__(self)
        self.required_exercises = 150
        self.description = "Atlas"
        self.badge_category = BadgeCategory.DIAMOND
        self.points = 50000
        self.is_teaser_if_unknown = True
