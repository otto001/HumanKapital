import threading
from time import sleep
from .models import Person
import random

tick_interval = 10

tick_thread = None


def start():
    global tick_thread
    random.seed(100)

    def tick_wrapper():
        global tick_interval
        while True:
            tick(tick_interval)
            sleep(tick_interval)

    tick_thread = threading.Thread(target=tick_wrapper, daemon=True)
    tick_thread.start()


def tick(delta_seconds):

    for person in Person.objects.filter(alive=True):
        for habit in person.habits.filter(risk__lt=0):
            risk_threshold = -habit.risk/10*(delta_seconds/10)
            r_val = random.random()

            if r_val < risk_threshold:
                print("DUMDUMDUM....")
