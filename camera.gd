extends Camera3D


func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			position /= 1.1
		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			position *= 1.1
	if event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
		get_parent().rotate_y(-event.screen_relative.x / 100)
		#get_parent().rotate(position.cross(get_parent().rotation), event.screen_relative.y / 100)
		
		get_parent().rotate(global_position.cross(Vector3.UP).normalized(), event.screen_relative.y / 100)
