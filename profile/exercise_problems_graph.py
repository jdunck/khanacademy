import models
import util
import logging

class ProblemPoint:
    def __init__(self, problem_log):
        self.time_taken = problem_log.time_taken_capped_for_reporting()
        self.correct = problem_log.correct
        self.exercise_non_summative = problem_log.exercise_non_summative
        self.exercise_non_summative_display_name = models.Exercise.to_display_name(problem_log.exercise_non_summative)
        self.dt = problem_log.time_done
        self.video_point = None

    def video_titles_html(self):
        if not self.video_point:
            return ""
        else:
            return "<br/>".join(self.video_point.dict_titles.keys())

    def video_time(self):
        if not self.video_point:
            return 0
        else:
            return util.seconds_to_time_string(self.video_point.seconds_watched, False)

class VideoPoint:
    def __init__(self, video_log):
        self.seconds_watched = video_log.seconds_watched
        self.dt = video_log.time_watched
        self.first_video_title = video_log.video_title
        self.dict_titles = {video_log.video_title: True}

def exercise_problems_graph_context(user, exid):
    if not user:
        return {}

    if not exid:
        exid = "addition_1"

    user_data = models.UserData.get_for(user)
    user_exercise = user_data.get_or_insert_exercise(exid)
    exercise = user_exercise.get_exercise()

    if not exercise:
        return {}

    related_videos = exercise.related_videos()
    video_list = []

    for exercise_video in related_videos:
        video_logs = models.VideoLog.get_for_user_and_video(user, exercise_video.key_for_video())
        for video_log in video_logs:
            video_list.append(VideoPoint(video_log))

    problem_list = []
    problem_logs = models.ProblemLog.all().filter('user =', user).filter('exercise =', exid).order("time_done")
    for problem_log in problem_logs:
        problem_list.append(ProblemPoint(problem_log))

    max_problems_in_graph = 35
    x_offset = 0
    if len(problem_list) > max_problems_in_graph:
        x_offset = len(problem_list) - max_problems_in_graph
        problem_list = problem_list[-1 * max_problems_in_graph:]

    video_and_problem_list = [point for sublist in [video_list, problem_list] for point in sublist]
    video_and_problem_list = sorted(video_and_problem_list, lambda a,b: cmp(a.dt, b.dt))

    video_point_last = None
    for video_or_problem in video_and_problem_list:
        if ProblemPoint.__name__ == video_or_problem.__class__.__name__:
            if video_point_last:
                video_or_problem.video_point = video_point_last
            video_point_last = None
        else:
            if video_point_last:
                video_point_last.seconds_watched += video_or_problem.seconds_watched
                video_point_last.dict_titles[video_or_problem.first_video_title] = True
            else:
                video_point_last = video_or_problem

    list_last_ten = problem_list[-10:]
    c_last_ten = len(list_last_ten)
    percent_last_ten_correct = 0

    if c_last_ten:
        c_last_ten_correct = reduce(lambda a, b: a + b, map(lambda problem_point: 1 if problem_point.correct else 0, list_last_ten))
        percent_last_ten_correct = int((float(c_last_ten_correct) / float(c_last_ten)) * 100)

    # Purposefully not showing any videos dangling after the last problem is done.
    # If video_point_last exists here, doing another problem will place it on the graph.

    x_axis_label = "Problem #"
    if x_offset:
        x_axis_label += " (Last %d problems)" % max_problems_in_graph

    return {
        'exercise_display_name': models.Exercise.to_display_name(exid),
        'exid': exid,
        'problem_list': problem_list,
        'streak': user_exercise.streak,
        'longest_streak': user_exercise.longest_streak,
        'percent_last_ten_correct': percent_last_ten_correct,
        'student_nickname': util.get_nickname_for(user),
        'x_offset': x_offset,
        'x_axis_label': x_axis_label,
    }

