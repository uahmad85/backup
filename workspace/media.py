import webbrowser
class Movie():
    def __init__(self, movie_title='Toy Story', movie_storyline='Toys Come to Life', poster_image='https://en.wikipedia.org/wiki/File:Toy_Story.jpg', trailer_youtube='https://www.youtube.com/watch?v=J6i9_i5bL5Q&list=PL1F03876BA92D4647'):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def open_image(self):
        webbrowser.open(self.poster_image_url)

    def play_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
