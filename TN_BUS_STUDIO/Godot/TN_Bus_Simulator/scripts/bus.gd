extends CharacterBody3D
## Simple arcade bus controller, intended for desktop keyboard and touchscreen.
const MAX_SPEED := 17.0
const ACCEL := 7.0
const BRAKE := 13.0
const DRAG := 3.5
const TURN_RATE := 0.85
const REVERSE_MAX_SPEED := 5.0
const COAST_DRAG := 2.0
const STEERING_RESPONSE := 3.0
var steering_angle := 0.0
var speed := 0.0
var throttle_touch := false
var brake_touch := false
var left_touch := false
var right_touch := false
var visual: Node3D

func _ready() -> void:
    name = "Bus"
    var collider := CollisionShape3D.new()
    var shape := BoxShape3D.new()
    shape.size = Vector3(2.4, 2.8, 9.8)
    collider.shape = shape
    collider.position.y = 1.45
    add_child(collider)
    visual = Node3D.new()
    visual.name = "Visual"
    add_child(visual)
    var imported: Resource = null
    if ResourceLoader.exists("res://assets/TN_Bus.glb"):
        imported = load("res://assets/TN_Bus.glb")
    if imported is PackedScene:
        var model: Node = imported.instantiate()
        visual.add_child(model)
        # Blender exports Z-up converted to Godot Y-up; model's front is -Z.
    else:
        _fallback_bus()

func _box(label: String, position: Vector3, size: Vector3, color: Color) -> void:
    var mesh := MeshInstance3D.new()
    mesh.name = label
    var cube := BoxMesh.new()
    cube.size = size
    mesh.mesh = cube
    var mat := StandardMaterial3D.new()
    mat.albedo_color = color
    mesh.material_override = mat
    mesh.position = position
    visual.add_child(mesh)

func _fallback_bus() -> void:
    _box("Green body", Vector3(0, 1.35, 0), Vector3(2.4, 1.5, 10.2), Color(0.1, 0.35, 0.16))
    _box("Cream roof", Vector3(0, 2.48, 0), Vector3(2.45, 0.78, 10.25), Color(0.86, 0.8, 0.65))
    _box("Windscreen", Vector3(0, 2.4, -5.15), Vector3(2.0, 0.52, 0.04), Color(0.05, 0.12, 0.16))
    for side in [-1.0, 1.0]:
        for index in range(8):
            _box("Window", Vector3(side * 1.23, 2.45, -4.3 + index * 1.2), Vector3(0.025, 0.47, 0.96), Color(0.04, 0.1, 0.14))

func drive(delta: float, throttle: float, steering: float, braking: bool) -> void:
    throttle = clampf(throttle, -1.0, 1.0)
    steering = clampf(steering, -1.0, 1.0)
    if braking:
        speed = move_toward(speed, 0.0, BRAKE * delta)
    elif absf(throttle) > 0.01:
        var target_speed := throttle * (MAX_SPEED if throttle > 0.0 else REVERSE_MAX_SPEED)
        # Brake to a stop before switching driving direction.
        if absf(speed) > 0.05 and signf(speed) != signf(target_speed):
            speed = move_toward(speed, 0.0, BRAKE * delta)
        else:
            speed = move_toward(speed, target_speed, ACCEL * delta)
    else:
        speed = move_toward(speed, 0.0, COAST_DRAG * delta)
    steering_angle = move_toward(steering_angle, steering, STEERING_RESPONSE * delta)
    if absf(speed) > 0.05:
        rotation.y += steering_angle * TURN_RATE * delta * signf(speed) * minf(absf(speed) / 4.0, 1.0)
    velocity = -global_transform.basis.z * speed
    move_and_slide()

func _physics_process(delta: float) -> void:
    var throttle := Input.get_action_strength("accelerate") - Input.get_action_strength("reverse")
    if throttle_touch:
        throttle = 1.0
    var steering := Input.get_action_strength("steer_left") - Input.get_action_strength("steer_right")
    if left_touch:
        steering += 1.0
    if right_touch:
        steering -= 1.0
    drive(delta, throttle, steering, brake_touch or Input.is_action_pressed("brake"))
