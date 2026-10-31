extends RefCounted
## Deterministic, self-contained Tamil Nadu-inspired village environment.
## All dimensions are metres. Driving corridor is X -5.5..5.5, Z -95..95.
const ROAD_LENGTH := 200.0
const ROAD_WIDTH := 11.0
const TREE_POSITIONS := [-83.0, -57.0, -31.0, 2.0, 27.0, 54.0, 79.0]

func material(color: Color, roughness: float = 1.0) -> StandardMaterial3D:
    var m := StandardMaterial3D.new()
    m.albedo_color = color
    m.roughness = roughness
    return m

func block(parent: Node3D, label: String, pos: Vector3, size: Vector3, mat: Material, collision: bool = false) -> Node3D:
    var node: Node3D
    if collision:
        node = StaticBody3D.new()
        var hit := CollisionShape3D.new()
        var shape := BoxShape3D.new()
        shape.size = size
        hit.shape = shape
        node.add_child(hit)
    else:
        node = Node3D.new()
    node.name = label
    node.position = pos
    parent.add_child(node)
    var mesh := MeshInstance3D.new()
    var cube := BoxMesh.new()
    cube.size = size
    mesh.mesh = cube
    mesh.material_override = mat
    node.add_child(mesh)
    return node

func cylinder(parent: Node3D, label: String, pos: Vector3, radius: float, height: float, mat: Material, collision: bool = false) -> void:
    var holder := Node3D.new()
    holder.name = label
    holder.position = pos
    parent.add_child(holder)
    var mesh := MeshInstance3D.new()
    var shape := CylinderMesh.new()
    shape.top_radius = radius
    shape.bottom_radius = radius
    shape.height = height
    mesh.mesh = shape
    mesh.material_override = mat
    holder.add_child(mesh)
    if collision:
        var body := StaticBody3D.new()
        holder.add_child(body)
        var hit := CollisionShape3D.new()
        var hit_shape := CylinderShape3D.new()
        hit_shape.radius = radius
        hit_shape.height = height
        hit.shape = hit_shape
        body.add_child(hit)

func build(world: Node3D) -> Node3D:
    var village := Node3D.new()
    village.name = "TamilNaduVillage"
    world.add_child(village)
    var asphalt := material(Color(0.22, 0.23, 0.22))
    var soil := material(Color(0.47, 0.32, 0.17))
    var green := material(Color(0.21, 0.43, 0.15))
    var paddy := material(Color(0.49, 0.64, 0.15))
    var white := material(Color(0.91, 0.88, 0.73))
    var yellow := material(Color(0.94, 0.79, 0.32))
    var brown := material(Color(0.32, 0.19, 0.10))
    var leaf := material(Color(0.09, 0.36, 0.13))
    var roof := material(Color(0.55, 0.20, 0.12))
    var blue := material(Color(0.13, 0.36, 0.49))
    # One continuous collision surface for the bus, including the shoulders.
    block(village, "GroundCollision", Vector3(0, -0.20, 0), Vector3(140, 0.3, 210), soil, true)
    block(village, "VillageRoad", Vector3(0, -0.025, 0), Vector3(ROAD_WIDTH, 0.08, ROAD_LENGTH), asphalt)
    for side in [-1.0, 1.0]:
        block(village, "DirtShoulder", Vector3(side * 6.15, 0.01, 0), Vector3(1.2, 0.06, ROAD_LENGTH), soil)
        block(village, "RoadEdge", Vector3(side * 5.32, 0.025, 0), Vector3(0.10, 0.015, 195), white)
        block(village, "PaddyField", Vector3(side * 17.0, -0.025, 0), Vector3(17, 0.07, 195), paddy)
        # Water channel separates the agricultural fields from the shoulder.
        block(village, "IrrigationCanal", Vector3(side * 7.35, 0.012, 0), Vector3(0.65, 0.025, 188), blue)
        for z in TREE_POSITIONS:
            var x: float = side * 10.0
            cylinder(village, "CoconutTrunk", Vector3(x, 2.4, z), 0.16, 4.8, brown, true)
            for offset in [-1.0, 0.0, 1.0]:
                block(village, "PalmFrond", Vector3(x + offset * 0.9, 4.85, z + offset * 0.3), Vector3(2.0, 0.12, 0.46), leaf)
        for z in [-68.0, -10.0, 48.0]:
            var x: float = side * 28.0
            block(village, "VillageHouse", Vector3(x, 1.25, z), Vector3(5, 2.5, 5.5), white, true)
            block(village, "TerracottaRoof", Vector3(x, 2.65, z), Vector3(5.6, 0.35, 6.0), roof)
            block(village, "HouseDoor", Vector3(x - side * 2.53, 0.85, z), Vector3(0.06, 1.7, 0.85), brown)
            block(village, "HouseWindow", Vector3(x - side * 2.54, 1.5, z + 1.6), Vector3(0.07, 0.7, 0.9), blue)
        for z in [-80.0, -40.0, 0.0, 40.0, 80.0]:
            cylinder(village, "ElectricPole", Vector3(side * 8.4, 2.4, z), 0.11, 4.8, white, true)
            block(village, "PoleCrossbar", Vector3(side * 8.4, 4.55, z), Vector3(0.10, 0.12, 1.45), brown)
    for z in range(-90, 91, 12):
        block(village, "DashedCentreLine", Vector3(0, 0.025, float(z)), Vector3(0.12, 0.015, 4.0), yellow)
    # Rural bus stop on the left shoulder, safely outside the drivable lane.
    block(village, "BusStopPlatform", Vector3(-8.5, 0.13, -24), Vector3(2.5, 0.25, 6), white)
    for z in [-26.0, -22.0]:
        cylinder(village, "BusStopPost", Vector3(-9.4, 1.4, z), 0.075, 2.7, brown)
    block(village, "BusStopShelterRoof", Vector3(-9.4, 2.85, -24), Vector3(2.3, 0.17, 5.1), roof)
    block(village, "BusStopBench", Vector3(-9.4, 0.65, -24), Vector3(0.45, 0.17, 2.4), brown)
    block(village, "BusStopSign", Vector3(-6.7, 2.3, -24), Vector3(0.10, 0.6, 1.2), yellow)
    # Route 001: two additional identifiable stops; keep the original Village Stop.
    for stop_name in ["AgriculturalMarketStop", "TownTerminalStop"]:
        var z: float = -60.0 if stop_name == "AgriculturalMarketStop" else -85.0
        block(village, stop_name, Vector3(-8.5, 0.13, z), Vector3(2.5, 0.25, 6.0), white)
        block(village, stop_name + "Sign", Vector3(-6.7, 2.2, z), Vector3(0.1, 0.6, 1.2), yellow)
    return village
