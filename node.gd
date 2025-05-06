class_name CourseNode extends RigidBody3D


var course_data: Dictionary

var height: int = -1
var target_radius: int = 10

func init(code, courses_data):
	name = code
	course_data = courses_data[code]
	match code[3]:
		'A': 
			target_radius = 1
			$MeshInstance3D.mesh.material.albedo_color = Color(1, 0, 0)
		'B':
			target_radius = 2
			$MeshInstance3D.mesh.material.albedo_color = Color(0, 1, 0)
		'C':
			target_radius = 3
			$MeshInstance3D.mesh.material.albedo_color = Color(0, 0, 1)
		'D':
			target_radius = 4
			$MeshInstance3D.mesh.material.albedo_color = Color(0.5, 0.5, 1)
		_:
			error_string("Unsupported coursecode " + code)
	target_radius *= 20
	position = Vector3(randf_range(0, 1) + (height * 10), randf_range(0, 1), randf_range(0, 1))
	#
	#var r = RegEx.new()
	#r.compile("[a-zA-Z]{3}[ABCD] + 0.1)\\d\\dH3")
	#for res in r.search_all(str(["prereqs_str"])):
		#print(res.get_string())
	#
	$Label.text = code + " - " + course_data["name"]
	#if course_data["offered"] == false:
		#$Panel/LblCodeName.text += " (Not Offered)"
	#
	#$Panel/LblDesc.text = course_data["description"]
	
	
	
	#code = data["code"]

func set_height(new_height: int):
	if new_height > height:
		height = new_height
		#print(name + " --> ", height)
		for post in course_data["postreqs"]:
			Data.nodes[post].set_height(height + 1)

func force_target_radius(strength: int):
	var target_position = position.normalized() * target_radius
	var dist = position.distance_to(target_position)
	var dir = position.direction_to(target_position)
	var force = (dir * sign(dist) / (dist * dist * strength)).inverse()
	apply_central_force(force)

func force_repel_nodes(strength: int):
	for n: CourseNode in get_parent().get_children().filter(func(child): return child is CourseNode and child != self):
		var force = n.position.direction_to(position) * strength / (pow(n.position.distance_to(position), 2))
		apply_central_force(force)

func force_attract_edges(strength: int):
	for pre in course_data["prereqs"]:
		pre = Data.nodes[pre]
		if pre.is_inside_tree():
			var force = (position.direction_to(pre.position) / (strength * pow(pre.position.distance_to(position), 2))).inverse()
			apply_central_force(force)
	
	for post in course_data["postreqs"]:
		post = Data.nodes[post]
		if post.is_inside_tree():
			var force = (position.direction_to(post.position) / (strength * pow(post.position.distance_to(position), 2))).inverse()
			apply_central_force(force)


func _physics_process(_delta: float) -> void:
	linear_velocity = linear_velocity.slerp(Vector3.ZERO, 0.99)
	force_target_radius(0.1)
	force_repel_nodes(10)
	#force_attract_edges(0.5)
	
	
	if position.length() > 1000:
		position = Vector3(0, randf_range(0, 1), randf_range(0, 1))



	
#"ANTC14H3": { 	"breadth": "Social and Behavioural Sciences",
				#"description": "Examines why, when, and how gender inequality became an anthropological concern by tracing the development of feminist thought in a comparative ethnographic framework.", 
								#"exclusions": [],
								#"name": "Feminism and Anthropology",
								#"offered": true,
								#"prereqs": [],
								#"prereqs_str": "[ANTB19H3 and ANTB20H3] or [1.0 credit at the B-level in WST courses]",
								#"sameas": [],
								#"url": "https://utsc.calendar.utoronto.ca/course/ANTC14H3" }


func _on_input_event(_camera: Node, event: InputEvent, _event_position: Vector3, _normal: Vector3, _shape_idx: int) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.is_pressed():
		get_node("/root/Graph/Rig").global_position = global_position
