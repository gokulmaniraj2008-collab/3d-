extends SceneTree

func fail(message: String) -> void:
    push_error("TN BUS SMOKE TEST FAILED: " + message)
    quit(1)

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var scene := load("res://main.tscn") as PackedScene
    if scene == null:
        fail("Main scene failed to load")
        return
    var world := scene.instantiate()
    root.add_child(world)
    await process_frame
    var village := world.get_node_or_null("TamilNaduVillage")
    if village == null or village.get_node_or_null("VillageRoad") == null or village.get_node_or_null("GroundCollision") == null or village.get_node_or_null("BusStopPlatform") == null:
        fail("Village road, ground collision or bus stop missing")
        return
    var bus := world.get_node_or_null("Bus") as CharacterBody3D
    if bus == null:
        fail("Bus node missing")
        return
    if world.get("camera") == null:
        fail("Follow camera missing")
        return
    var visual: Node3D = bus.get("visual")
    if visual == null or visual.get_child_count() == 0:
        fail("Bus model missing")
        return
    var original := bus.global_position
    bus.call("drive", 1.0, 1.0, 0.0, false)
    if bus.get("speed") <= 0.0:
        fail("Accelerator must increase speed")
        return
    if bus.global_position.distance_to(original) <= 0.01:
        fail("Bus must move")
        return
    bus.call("drive", 0.5, 0.0, 0.0, true)
    if bus.get("speed") >= 7.0:
        fail("Brake must reduce speed")
        return
    bus.set("speed", 0.0)
    bus.call("drive", 1.0, -1.0, 0.0, false)
    if bus.get("speed") >= 0.0 or absf(bus.get("speed")) > 5.01:
        fail("Reverse speed must be negative and limited")
        return
    bus.call("drive", 0.5, 1.0, 0.0, false)
    if bus.get("speed") > 0.0:
        fail("Direction changes must brake before accelerating forward")
        return
    print("TN BUS SMOKE TEST PASSED")
    quit(0)
