class_name CourseNode extends RigidBody3D


var course_data: Dictionary

var height: int = -1
var target_radius: int = 10

func init(code, courses_data):
	name = code
	course_data = courses_data[code]
	match code[3]:
		'A': target_radius = 1
		'B': target_radius = 2
		'C': target_radius = 3
		'D': target_radius = 4
		_:   error_string("Unsupported coursecode " + code)
	target_radius *= 10
	position = Vector3(randf_range(-1, 1), randf_range(-1, 1), randf_range(-1, 1))
	#
	#var r = RegEx.new()
	#r.compile("[a-zA-Z]{3}[ABCD] + 0.1)\\d\\dH3")
	#for res in r.search_all(str(["prereqs_str"])):
		#print(res.get_string())
	#
	$SubViewport/Panel/LblCodeName.text = code + " - " + course_data["name"]
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

func _physics_process(_delta: float) -> void:
	$Panel.look_at(get_node("/root/Graph/Rig/Camera").global_position, Vector3.UP, true)
	linear_velocity = linear_velocity.slerp(Vector3.ZERO, 0.2)
	var target_position = position.normalized() * target_radius
	var dist = position.distance_to(target_position)
	var dir = position.direction_to(target_position)
	var force = (dir * sign(dist) / (dist * dist)).inverse()
	
	apply_central_force(force)
	
	for n: CourseNode in get_parent().get_children().filter(func(child): return child is CourseNode and child != self):
		force = n.position.direction_to(position) * 1 / (pow(n.position.distance_to(position), 2))
		apply_central_force(force)
	
	for pre in course_data["prereqs"]:
		pre = Data.nodes[pre]
		if pre.is_inside_tree():
			force = (position.direction_to(pre.position) * 1000 / (pow(pre.position.distance_to(position), 2))).inverse()
			apply_central_force(force)
	
	for post in course_data["postreqs"]:
		post = Data.nodes[post]
		if post.is_inside_tree():
			force = (position.direction_to(post.position) * 1000 / (pow(post.position.distance_to(position), 2))).inverse()
			apply_central_force(force)
	
	#apply_central_force(Vector3.UP)
	
	#print(name, linear_velocity, position)
	
	#linear_velocity = Vector3.UP
	
	
	



	
#"ANTC14H3": { 	"breadth": "Social and Behavioural Sciences",
				#"description": "Examines why, when, and how gender inequality became an anthropological concern by tracing the development of feminist thought in a comparative ethnographic framework.", 
								#"exclusions": [],
								#"name": "Feminism and Anthropology",
								#"offered": true,
								#"prereqs": [],
								#"prereqs_str": "[ANTB19H3 and ANTB20H3] or [1.0 credit at the B-level in WST courses]",
								#"sameas": [],
								#"url": "https://utsc.calendar.utoronto.ca/course/ANTC14H3" }
