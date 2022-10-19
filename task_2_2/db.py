def get_all_games(user):
    response = user.quizzes.all()
    return response