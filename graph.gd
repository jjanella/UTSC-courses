extends Node3D


func _ready() -> void:
	graph_node("CSCD58H3")
	graph_node("CSCD27H3")
	graph_node("CSCD84H3")

func draw_edge(from: Vector3, to: Vector3):
	var l = ImmediateMesh.new()
	l.surface_begin(Mesh.PRIMITIVE_LINES)
	l.surface_add_vertex(from)
	l.surface_add_vertex(to)
	l.surface_end()
	

func graph_node(code: String) -> CourseNode:
	if get_node_or_null(code) != null:
		return
	var node = Data.nodes[code]
	
	add_child(node)
	for pre in node.course_data["prereqs"]:
		graph_node(pre)
		draw_edge(node.global_position, Data.nodes[pre].global_position)
	
	return

func _physics_process(delta: float) -> void:
	return
	
