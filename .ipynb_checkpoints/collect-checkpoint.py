import pickle
import phub

from pyats.async_.synchronize import Lockable

class SemaMethods(Lockable):

    def __init__(self):
        super().__init__()

    @Lockable.locked
    def atualize_and_get(self, n_pool, n_videos, n_videos_participants, searched_star):
        with open("videos_file", "rb") as videos_file:
            videos = pickle.load(videos_file)
        with open("videos_file", "wb") as videos_file:
            pickle.dump(videos + n_videos, videos_file)
            
        with open("searched_file", "rb") as searched_file:
            searched_stars = pickle.load(searched_file)
        for p in n_pool:
            if p in searched_stars:
                n_pool.remove(p)
        searched_stars.append(searched_star)
        with open("searched_file", "wb") as searched_file:
            pickle.dump(searched_stars, searched_file)
            
        with open("pool_file", "rb") as pool_file:
            pool = pickle.load(pool_file)
        with open("pool_file", "wb") as pool_file:
            pickle.dump(pool, pool + list(set(n_pool) - set(pool)))
            
        with open("videos_participants_file", "rb") as videos_participants_file:
            videos_participants = pickle.load(videos_participants_file)
        with open("videos_participants_file", "wb") as videos_participants_file:
            pickle.dump(videos_participants + n_videos_participants, videos_participants_file)

        return videos_participants, videos, searched_stars, pool
        
    @Lockable.locked
    def get_initials(self):
        with open("videos_participants_file", "rb") as videos_participants_file:
            videos_participants = pickle.load(videos_participants_file)
        with open("videos_file", "rb") as videos_file:
            videos = pickle.load(videos_file)
        
        with open("searched_file", "rb") as searched_file:
            searched_stars = pickle.load(searched_file)
        with open("pool_file", "rb") as pool_file:
            pool = pickle.load(pool_file)
        return videos_participants, videos, searched_stars, pool

    @Lockable.locked
    def remove_p(self, p):
        with open("pool_file", "rb") as pool_file:
            pool = pickle.load(pool_file)
        pool.remove(p)
        with open("pool_file", "wb") as pool_file:
            pickle.dump(pool, pool_file)

client = phub.Client(language = 'br')

SM = SemaMethods()

SM.acquire()
videos_participants, videos, searched_stars, pool = SM.get_initials()

while len(pool) != 0:
    p = pool[0]
    search = client.search(p.replace('-',' '))
    SM.remove_p(p)
    SM.release()
    
    n_pool = []
    n_videos = []
    n_videos_participants = []
    
    for v in range(20):
        try:
            video = search.get(v)
            pornstars = video.pornstars
            n_videos_participants.append(pornstars)
            n_videos.append(video)
            for participant in pornstars:
                name = participant.name
                n_pool.append(name)
        except phub.errors.NoResult:
            pass

    SM.acquire()
    videos_participants, videos, searched_stars, pool = SM.atualize_and_get(n_pool, n_videos, n_videos_participants, p)