extends Node

var nodes: Dictionary

func _ready() -> void:
	var data: String = FileAccess.get_file_as_string("./data.txt")
	var json: JSON = JSON.new()
	json.parse(data)
	var courses_data = json.data[2]
	
	for code in courses_data:
		var node: CourseNode = preload("res://node.tscn").instantiate()
		node.init(code, courses_data)
		nodes[code] = node
	
	for node in nodes.values():
		if node.course_data["prereqs"].is_empty():
			node.set_height(0)
