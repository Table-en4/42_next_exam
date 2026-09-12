Write a function that determines the minimum number of meeting rooms required to schedule a list of meeting time intervals without overlap, and assigns meetings to rooms.

Each interval is represented as a tuple of `(start_time, end_time)`.

The function should:
- Sort meetings by start time and assign them to available rooms sequentially.
- Return a tuple `(num_rooms, rooms)` where `num_rooms` is the integer count of rooms required, and `rooms` is a list of lists containing the scheduled intervals for each room.
- If the input list is empty, return `(0, [])`.