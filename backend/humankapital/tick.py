import threading
from time import sleep
from .models import Person
import random
import humankapital.balancing as balancing
from .models.events import Event
from .models.time import Time
from django.utils import timezone
from datetime import timedelta
from django.db.models import F


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


last_year = None


def tick(delta_seconds):
    global last_year
    v_time = Time.objects.first()
    if v_time is None:
        v_time = Time.objects.create(time=timezone.now())
    if last_year is None:
        last_year = v_time.time.year

    if last_year < v_time.time.year:
        Person.objects.filter(alive=True).update(age=F('age')+1)
        last_year = v_time.time.year

        death_age = random.randint(75, 90)
        Person.objects.filter(age__gt=death_age).update(alive=False)

    v_time.time += timedelta(seconds=delta_seconds*balancing.time_warp)
    v_time.save()

    warp_factor = delta_seconds*balancing.time_warp/balancing.event_risk_divider

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
            risk_threshold = ((-habit.risk/10000)*warp_factor)/player_karma
            if random.random() < risk_threshold:
                print("DUMDUMDUM....")
                person.alive = False
                text = f"{person.name} ist an {habit.name} verstorben"
                Event.objects.create(person_id=person.id, reason=f"habit {habit.id}", text=text, death=True,
                                     positive=False, decision=False)
                person.save(update_fields=["alive"])

        if not person.alive:
            continue

        # job promo
        promo_chance = person.job.risk * social_background_factor * psycho_factors * age_factor_success
        promo_threshold = ((promo_chance/1000)*warp_factor)/player_karma

        if random.random() < promo_threshold:
            factor = random.random()/10 + 1
            person.salary_year = int(float(person.salary_year) * factor)
            person.save(update_fields=["salary_year"])
            percent = int(100*factor)-100
            text = f"{person.name} hat eine Gehaltserhöhung von {percent}% erhalten"
            Event.objects.create(person_id=person.id, reason=f"raise {factor}", text=text, death=False,
                                 positive=True, decision=False)
