extends Node3D

var l: ImmediateMesh

func _ready() -> void:
	l = ImmediateMesh.new()
	graph_node("CSCA48H3")
	graph_node("CSCB63H3")
	graph_node("MATB41H3")
	graph_node("CSCD27H3")
	graph_node("CSCD84H3")
	graph_node("CSCD37H3")


func _physics_process(_delta: float) -> void:
	var pos = $Rig/Camera.global_position - $Rig.global_position
	pos.y = 0
	for node: CourseNode in get_children().filter(func(child): return child is CourseNode and child != self):
		node.look_at(pos + node.global_position, Vector3.UP, true)
		
	#var target = get_node("/root/Graph/Rig/Camera").global_position
	#target.y = position.y
	#$Panel.look_at(target, Vector3.UP, true)
	
	
	var mesh: ImmediateMesh = $Edges.mesh
	mesh.clear_surfaces()
	mesh.surface_begin(Mesh.PRIMITIVE_LINES)
	for n: CourseNode in get_children().filter(func(child): return child is CourseNode and child != self):
		for pre in n.course_data["prereqs"]:
			mesh.surface_add_vertex(n.global_position)
			mesh.surface_add_vertex(Data.nodes[pre].global_position)
	mesh.surface_end()

func graph_node(code: String) -> CourseNode:
	if get_node_or_null(code) != null:
		return
	var node = Data.nodes[code]
	
	add_child(node)
	for pre in node.course_data["prereqs"]:
		graph_node(pre)
		#draw_edge(node.global_position, Data.nodes[pre].global_position)
	
	return
