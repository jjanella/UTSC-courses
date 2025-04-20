class_name CourseNode extends RigidBody3D


var course_data: Dictionary

var height: int = -1

func init(code, courses_data):
	name = code
	course_data = courses_data[code]
	#
	#var r = RegEx.new()
	#r.compile("[a-zA-Z]{3}[ABCD]\\d\\dH3")
	#for res in r.search_all(str(["prereqs_str"])):
		#print(res.get_string())
	#
	#$Panel/LblCodeName.text = code + " - " + course_data["name"]
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
	


	
#"ANTC14H3": { 	"breadth": "Social and Behavioural Sciences",
				#"description": "Examines why, when, and how gender inequality became an anthropological concern by tracing the development of feminist thought in a comparative ethnographic framework.", 
								#"exclusions": [],
								#"name": "Feminism and Anthropology",
								#"offered": true,
								#"prereqs": [],
								#"prereqs_str": "[ANTB19H3 and ANTB20H3] or [1.0 credit at the B-level in WST courses]",
								#"sameas": [],
								#"url": "https://utsc.calendar.utoronto.ca/course/ANTC14H3" }
