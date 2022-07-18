# import requests
# import json
#
# def get_student_info(student_id):
#     result = requests.get(
#         f"http://localhost:5001/students/{student_id}",
#         headers={'content-type': 'application/json'}
#     )
#     return result.json()
#
# def get_grade_by_task(task_id):
#     result = requests.get(
#         f"http://localhost:5001/tasks/{task_id}",
#         headers={'content-type': 'application/json'}
#     )
#     return result.json()
#
# def average_score(student_id):
#     result = requests.get(
#         f"http://localhost:5001/grades/{student_id}",
#         headers={'content-type': 'application/json'}
#     )
#     return result.json()
#
#
# def add_student_info(student_first_name, student_last_name, course_id):
#     student = {
#         "firstName": student_first_name,
#         "lastName": student_last_name,
#         "courseId": course_id
#     }
#     result = requests.post(
#         'http://localhost:5001/students',
#         headers={'content-type': 'application/json'},
#         data=json.dumps(student)
#     )
#     return result
#
#
# def run():
#     print('############################')
#     print('Hello, welcome to our school')
#     print("Press 1 to view a student, Press 2 to add a student, Press 3 to view all the grades for task. Press 4 to check student's grade")
#     print('############################')
#     choice = int(input("Which do you want to do? : "))
#     if choice == 1:
#         student_id = input("Which student would you like to see ? :")
#         print(get_student_info(student_id))
#     elif choice == 2:
#         student_first_name = input("First Name ? :")
#         student_last_name = input("Last Name ? :")
#         course_id = input("Course ID ? :")
#         add_student_info(student_first_name, student_last_name, course_id)
#     elif choice == 3:
#         task_id = input("Which task would you like to view? : ")
#         print(get_grade_by_task(task_id))
#     elif choice == 4:
#         student_id = input("Which student grades would like to see? : ")
#         print(average_score(student_id))
#
#
#
# if __name__ == '__main__':
#     run()