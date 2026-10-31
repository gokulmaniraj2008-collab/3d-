extends Node
## Deterministic prototype: a stop completes only when the bus is nearby, stationary and doors are open.
signal stop_completed(index: int, boarded: int, alighted: int)
const STOP_POSITIONS := [Vector3(-3.0, 0.0, -24.0), Vector3(-3.0, 0.0, -60.0), Vector3(-3.0, 0.0, -85.0)]
const STOP_NAMES := ["Village Stop", "Agricultural Market", "Town Terminal"]
const BOARDING := [5, 3, 0]
const ALIGHTING := [0, 2, 6]
const STOP_RADIUS := 8.0
var current_stop := 0
var passengers := 1
var completed := false

func try_complete_stop(bus: Node3D) -> bool:
    if completed or current_stop >= STOP_POSITIONS.size():
        return false
    if bus.global_position.distance_to(STOP_POSITIONS[current_stop]) > STOP_RADIUS:
        return false
    if absf(float(bus.get("speed"))) > 0.1 or not bool(bus.get("doors_open")):
        return false
    var alighted: int = mini(passengers, ALIGHTING[current_stop])
    passengers = passengers - alighted + BOARDING[current_stop]
    stop_completed.emit(current_stop, BOARDING[current_stop], alighted)
    current_stop += 1
    completed = current_stop >= STOP_POSITIONS.size()
    return true

func status_text() -> String:
    if completed:
        return "Route complete | Passengers: %d" % passengers
    return "Next: %s (%d/%d) | Passengers: %d" % [STOP_NAMES[current_stop], current_stop + 1, STOP_NAMES.size(), passengers]
