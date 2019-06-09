import threading
from time import sleep
from .models import Person
import random
import humankapital.balancing as balancing
from .models.events import Event

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

        acq = person.acquisitions.filter(sold__isnull=True).first()
        if not acq:
            continue

        player = acq.player
        player_karma = player.karma

        social_background_factor = balancing.social_background_factors[person.social_background]
        psycho_factors = (sum(trait.risk for trait in person.psychological_attributes.all())+5)/5
        psycho_factors = (psycho_factors + 1) / 2
        age_factor_success = 1.5-0.0007*(person.age-24)**2

        # habits
        for habit in person.habits.filter(risk__lt=0):
            risk_threshold = ((-habit.risk/1000)*delta_seconds)/player_karma
            if random.random() < risk_threshold:
                print("DUMDUMDUM....")
                person.alive = False
                text = f"{person.name} ist an {habit.name} verstorben"
                Event.objects.create(person_id=person.id, reason=f"habit {habit.id}", text=text, death=True,
                                     positive=False)
                person.save(update_fields=["alive"])

        if not person.alive:
            continue

        # job promo
        promo_chance = person.job.risk * social_background_factor * psycho_factors * age_factor_success
        promo_threshold = ((promo_chance/1000)*delta_seconds)/player_karma

        if random.random() < promo_threshold:
                person.salary_year = int(float(person.salary_year) * random.random()/10 + 1)
                person.save(update_fields=["salary_year"])
