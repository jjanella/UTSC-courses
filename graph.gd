extends Node3D

var l: ImmediateMesh

func _ready() -> void:
	l = ImmediateMesh.new()
	#graph_node("CSCA48H3")
	graph_node("CSCB63H3")
	#graph_node("CSCD27H3")
	#graph_node("CSCD84H3")


func _physics_process(_delta: float) -> void:
	var mesh: ImmediateMesh = $Edges.mesh
	mesh.clear_surfaces()
	mesh.surface_begin(Mesh.PRIMITIVE_LINES)
	for n: CourseNode in get_children().filter(func(child): return child is CourseNode and child != self):
		print(n.name)
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
