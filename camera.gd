extends Camera3D


func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			position *= 1.1
		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			position /= 1.1
