import pickle
import phub
from time import sleep

def atualize_and_get(n_pool, n_videos, n_videos_participants):
    with open("videos_file", "rb") as videos_file:
        videos = pickle.load(videos_file)
    with open("videos_file", "wb") as videos_file:
        pickle.dump(videos + n_videos, videos_file)
        
    with open("searched_file", "rb") as searched_file:
        searched_stars = pickle.load(searched_file)

    n_pool = [p for p in n_pool if p not in searched_stars]
    
    print(f'n pool{n_pool}')
    print(f'searched{searched_stars}')
        
    with open("pool_file", "rb") as pool_file:
        pool = pickle.load(pool_file)
    with open("pool_file", "wb") as pool_file:
        pickle.dump(pool + list(set(n_pool) - set(pool)),pool_file)
        
    with open("videos_participants_file", "rb") as videos_participants_file:
        videos_participants = pickle.load(videos_participants_file)
    with open("videos_participants_file", "wb") as videos_participants_file:
        pickle.dump(videos_participants + n_videos_participants, videos_participants_file)

    return videos_participants, videos, searched_stars, pool
    
def get_initials():
    with open("videos_participants_file", "rb") as videos_participants_file:
        videos_participants = pickle.load(videos_participants_file)
        
    with open("videos_file", "rb") as videos_file:
        videos = pickle.load(videos_file)
    
    with open("searched_file", "rb") as searched_file:
        searched_stars = pickle.load(searched_file)
        
    with open("pool_file", "rb") as pool_file:
        pool = pickle.load(pool_file)
        
    return videos_participants, videos, searched_stars, pool

def remove_p(p):
    with open("pool_file", "rb") as pool_file:
        pool = pickle.load(pool_file)
    print(pool, p)
    pool.remove(p)
    with open("pool_file", "wb") as pool_file:
        pickle.dump(pool, pool_file)
        
    with open("searched_file", "rb") as searched_file:
        searched_stars = pickle.load(searched_file)
    searched_stars.append(p)
    print(searched_stars)
    with open("searched_file", "wb") as searched_file:
        pickle.dump(searched_stars, searched_file)

def main(argv):
    id = int(argv[1])
    num = int(argv[2])
    
    client = phub.Client(language = 'br')

    id_atual = id+1
    while id_atual != id:
        with open("id_file.txt", 'r') as id_file:
            id_atual = int(id_file.read())
        sleep(1)
            
    videos_participants, videos, searched_stars, pool = get_initials()

    count = 0
    while len(pool) != 0 and count < 2:
        count += 1
        p = pool[0]
        search = client.search(p.replace('-',' '))

        remove_p(p)
        with open("id_file.txt", 'w') as id_file:
            if id+1 != num:
                id_file.write(f'{id+1}')
            else:
                id_file.write('0')

        print(p)
        
        n_pool = []
        n_videos = []
        n_videos_participants = []
        
        for v in range(5):
            try:
                print(v)
                video = search.get(v)
                pornstars = video.pornstars
                n_videos_participants.append(pornstars)
                n_videos.append(video)
                for participant in pornstars:
                    n_pool.append(participant.name)
            except phub.errors.NoResult:
                pass
    
        id_atual = id+1
        while id_atual != id:
            with open("id_file.txt", 'r') as id_file:
                id_atual = int(id_file.read())
            sleep(1)
        videos_participants, videos, searched_stars, pool = atualize_and_get(n_pool, n_videos, n_videos_participants)
    
import sys
if __name__ == '__main__':
    main(sys.argv)