from django.core.cache import cache

HOLD_TTL_SECONDS = 600


def _redis_client():
    return cache.client.get_client(write=True)


def hold_key(trip_id, seat_number):
    return f"seat_hold:{trip_id}:{seat_number}"


def get_held_seats(trip_id, seat_numbers):
    client = _redis_client()
    pipe = client.pipeline()

    for seat in seat_numbers:
        pipe.exists(cache.make_key(hold_key(trip_id, seat)))

    results = pipe.execute()
    return {seat for seat, exists in zip(seat_numbers, results) if exists}


def place_holds(trip_id, seat_numbers, booking_id):
    client = _redis_client()
    acquired = []

    for seat in seat_numbers:
        key = cache.make_key(hold_key(trip_id, seat))
        success = client.set(key, str(booking_id), nx=True, ex=HOLD_TTL_SECONDS)

        if success:
            acquired.append(seat)
        else:
            for held_seat in acquired:
                client.delete(cache.make_key(hold_key(trip_id, held_seat)))
            return False

    return True


def release_holds(trip_id, seat_numbers):
    client = _redis_client()
    pipe = client.pipeline()

    for seat in seat_numbers:
        pipe.delete(cache.make_key(hold_key(trip_id, seat)))
