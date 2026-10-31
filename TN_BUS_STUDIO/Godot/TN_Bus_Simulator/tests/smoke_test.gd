extends SceneTree

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var scene := load("res://main.tscn") as PackedScene
    assert(scene != null, "Main scene must load")
    var world := scene.instantiate()
    root.add_child(world)
    await process_frame
    var bus := world.get_node_or_null("Bus") as CharacterBody3D
    assert(bus != null, "Bus node missing")
    assert(world.get("camera") != null, "Follow camera missing")
    assert(bus.get('visual').get_child_count() > 0, "Bus model missing")
    var original := bus.global_position
    bus.call('drive', 1.0, 1.0, 0.0, false)
    assert(bus.get('speed') > 0.0, "Accelerator must increase speed")
    assert(bus.global_position.distance_to(original) > 0.01, "Bus must move")
    bus.drive(0.5, 0.0, 0.0, true)
    assert(bus.get('speed') < 7.0, "Brake must reduce speed")
    print("TN BUS SMOKE TEST PASSED")
    quit(0)
