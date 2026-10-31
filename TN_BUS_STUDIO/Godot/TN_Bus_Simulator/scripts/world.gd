extends Node3D
const BusScript = preload("res://scripts/bus.gd")
const VillageRoad = preload("res://scripts/village_road.gd")
const RouteManager = preload("res://scripts/route_manager.gd")
var route_manager: Node
var bus
var camera: Camera3D
var speed_label: Label

func _ready() -> void:
    _setup_inputs()
    VillageRoad.new().build(self)
    bus = CharacterBody3D.new()
    bus.set_script(BusScript)
    bus.position = Vector3(0, 0.1, 0)
    add_child(bus)
    camera = Camera3D.new()
    camera.current = true
    camera.fov = 65.0
    add_child(camera)
    var sunlight := DirectionalLight3D.new()
    sunlight.rotation_degrees = Vector3(-50, -35, 0)
    sunlight.light_energy = 1.6
    add_child(sunlight)
    route_manager = RouteManager.new()
    route_manager.name = "RouteManager"
    add_child(route_manager)
    _hud()

func _setup_inputs() -> void:
    var mapping := {"accelerate": KEY_W, "reverse": KEY_S, "steer_left": KEY_A, "steer_right": KEY_D, "brake": KEY_SPACE}
    for action in mapping:
        if not InputMap.has_action(action):
            InputMap.add_action(action)
        var event := InputEventKey.new()
        event.physical_keycode = mapping[action]
        InputMap.action_add_event(action, event)
    var arrows := {"accelerate": KEY_UP, "reverse": KEY_DOWN, "steer_left": KEY_LEFT, "steer_right": KEY_RIGHT}
    for action in arrows:
        var event := InputEventKey.new()
        event.physical_keycode = arrows[action]
        InputMap.action_add_event(action, event)

func _environment() -> void:
    var ground := StaticBody3D.new()
    ground.name = "Road"
    add_child(ground)
    var shape := CollisionShape3D.new()
    var box := BoxShape3D.new()
    box.size = Vector3(180, 0.2, 220)
    shape.shape = box
    shape.position.y = -0.15
    ground.add_child(shape)
    var road := MeshInstance3D.new()
    var plane := BoxMesh.new()
    plane.size = Vector3(13, 0.1, 200)
    road.mesh = plane
    var road_mat := StandardMaterial3D.new()
    road_mat.albedo_color = Color(0.19, 0.21, 0.23)
    road.material_override = road_mat
    road.position.y = -0.05
    add_child(road)
    for side in [-1.0, 1.0]:
        var verge := MeshInstance3D.new()
        var mesh := BoxMesh.new()
        mesh.size = Vector3(30, 0.08, 200)
        verge.mesh = mesh
        verge.position = Vector3(side * 21.5, -0.08, 0)
        var grass := StandardMaterial3D.new()
        grass.albedo_color = Color(0.22, 0.42, 0.19)
        verge.material_override = grass
        add_child(verge)
    for z in range(-95, 100, 10):
        var dash := MeshInstance3D.new()
        var mesh := BoxMesh.new()
        mesh.size = Vector3(0.15, 0.015, 4)
        dash.mesh = mesh
        dash.position = Vector3(0, 0.01, z)
        var paint := StandardMaterial3D.new()
        paint.albedo_color = Color(0.95, 0.88, 0.55)
        dash.material_override = paint
        add_child(dash)

func _hud() -> void:
    var layer := CanvasLayer.new()
    add_child(layer)
    var root := Control.new()
    root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    root.mouse_filter = Control.MOUSE_FILTER_IGNORE
    layer.add_child(root)
    speed_label = Label.new()
    speed_label.position = Vector2(18, 16)
    speed_label.add_theme_font_size_override("font_size", 25)
    root.add_child(speed_label)
    var help := Label.new()
    help.text = "W/↑ Go   S/↓ Reverse   A/D Steer   Space Brake   H Handbrake   O Doors   E Serve Stop"
    help.position = Vector2(18, 54)
    root.add_child(help)
    var buttons := [
        ["◀", Vector2(22, -100), "left_touch"],
        ["▶", Vector2(120, -100), "right_touch"],
        ["GO", Vector2(-210, -100), "throttle_touch"],
        ["STOP", Vector2(-110, -100), "brake_touch"]
    ]
    for entry in buttons:
        var button := Button.new()
        button.text = entry[0]
        button.custom_minimum_size = Vector2(86, 70)
        if entry[1].x < 0:
            button.anchor_left = 1
            button.anchor_right = 1
        button.anchor_top = 1
        button.anchor_bottom = 1
        button.position = entry[1]
        button.mouse_filter = Control.MOUSE_FILTER_STOP
        root.add_child(button)
        var property_name: String = entry[2]
        button.button_down.connect(func(): bus.set(property_name, true))
        button.button_up.connect(func(): bus.set(property_name, false))

func _unhandled_key_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        if event.physical_keycode == KEY_H:
            bus.toggle_handbrake()
        elif event.physical_keycode == KEY_O:
            bus.set_doors_open(not bus.doors_open)
        elif event.physical_keycode == KEY_E:
            route_manager.try_complete_stop(bus)

func _process(delta: float) -> void:
    if bus == null:
        return
    speed_label.text = "TN BUS | %03d km/h | %s | %s" % [roundi(absf(bus.speed) * 3.6), ("DOORS OPEN" if bus.doors_open else "DOORS CLOSED"), route_manager.status_text()]
    var desired: Vector3 = bus.global_position + bus.global_transform.basis.z * 17.0 + Vector3.UP * 8.0
    camera.global_position = camera.global_position.lerp(desired, minf(delta * 5.0, 1.0))
    camera.look_at(bus.global_position + Vector3.UP * 1.7, Vector3.UP)
