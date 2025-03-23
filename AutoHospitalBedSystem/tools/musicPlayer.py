# import playsound as ps
# from pydub import AudioSegment
# from pydub.playback import play
# import mp3play
import time
import pygame
import asyncio
import threading


# def playMusic(path):
#     clip = mp3play.load(path)
#     print(clip.ispaused())
#     clip.play()
#     time.sleep(5)
#     clip.stop()


class Sound:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        time.sleep(0.1)
        self.sema = asyncio.Semaphore(value=20)
        self.loop = asyncio.get_event_loop()

    def play(self, path: str,
             epochs: int = 1,
             volume: float = 0.5):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        if epochs == -1:
            while True:
                sound.play()
                time.sleep(sound.get_length())
        for i in range(epochs):
            sound.play()
            # print(sound.get_volume())
            # pygame.mixer.music.play()
            time.sleep(sound.get_length())
            # pygame.mixer.music.stop()

    async def playSound(self, path: str,
                  epochs: int = 1,
                  volume: float = 0.5):

        # track = pygame.mixer.music.load('./kt.mp3')

        async with self.sema:
            r = await self.loop.run_in_executor(None, self.play,
                                                path, epochs, volume)


if __name__ == "__main__":
    sound = Sound()
    # task = [
    #     asyncio.ensure_future(sound.playSound('./kt.mp3', -1, 1))
    # ]
    #
    # sound.loop.run_until_complete(asyncio.wait(task))
    thread = threading.Thread(target=sound.play, args=('./kt.mp3', 1, 1.0))
    thread.start()
    # thread.join()  // wait until the function has done

    # sound.playSound("./kt.mp3", -1, 1)

