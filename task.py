import re

class EnhancedLearningPlatform:
    COURSES = ["Python", "DSA", "Databases", "Flask"]
    COURSE_INDEX = {name: i for i, name in enumerate(COURSES)}
    COURSE_LOOKUP = {name.lower(): name for name in COURSES}
    MAX_POINTS = [600, 400, 480, 550]

    def __init__(self):
        self.students = {}
        self.email_set = set()
        self.next_id = 10000
        self.notifications_sent = set()  # (student_id, course_index)

    def is_valid_name(self, name):
        parts = name.strip().split()
        for part in parts:
            if len(part) < 2:
                return False
            if not re.fullmatch(r"[A-Za-z]+([\-'][A-Za-z]+)*", part):
                return False
        return True

    def is_valid_email(self, email):
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

    def add_student(self, first_name, last_name, email):
        if not self.is_valid_name(first_name):
            return "Incorrect first name."
        if not self.is_valid_name(last_name):
            return "Incorrect last name."
        if not self.is_valid_email(email):
            return "Incorrect email."
        if email in self.email_set:
            return "This email is already taken."

        student_id = str(self.next_id)
        self.students[student_id] = {
            "name": f"{first_name} {last_name}",
            "email": email,
            "points": [0, 0, 0, 0],
            "activity": [0, 0, 0, 0]
        }
        self.email_set.add(email)
        self.next_id += 1
        return "The student has been added."

    def list_students(self):
        return "No students found." if not self.students else "Students:\n" + "\n".join(self.students.keys())

    def add_points(self, student_id, points):
        if student_id not in self.students:
            return f"No student is found for id={student_id}."
        if len(points) != 4 or any(not p.isdigit() or int(p) < 0 for p in points):
            return "Incorrect points format."
        points = list(map(int, points))
        student = self.students[student_id]
        for i, p in enumerate(points):
            if p > 0:
                student["activity"][i] += 1
            student["points"][i] += p
        return "Points updated."

    def find_student(self, student_id):
        if student_id not in self.students:
            return f"No student is found for id={student_id}."
        p = self.students[student_id]["points"]
        return f"{student_id} points: Python={p[0]}; DSA={p[1]}; Databases={p[2]}; Flask={p[3]}"

    def get_statistics(self):
        enrollment = [set() for _ in self.COURSES]
        activity = [0] * len(self.COURSES)
        total_points = [0] * len(self.COURSES)
        total_tasks = [0] * len(self.COURSES)

        for student_id, data in self.students.items():
            for i, (pts, acts) in enumerate(zip(data["points"], data["activity"])):
                if pts > 0:
                    enrollment[i].add(student_id)
                activity[i] += acts
                total_points[i] += pts
                total_tasks[i] += acts

        def analyze(metric):
            max_val = max(metric)
            min_val = min(metric)
            most = [self.COURSES[i] for i, v in enumerate(metric) if v == max_val and v > 0]
            least = [self.COURSES[i] for i, v in enumerate(metric) if v == min_val and v > 0 and self.COURSES[i] not in most]
            return most or ["n/a"], least or ["n/a"]

        most_popular, least_popular = analyze([len(e) for e in enrollment])
        highest_activity, lowest_activity = analyze(activity)
        avg_score = [(total_points[i] / total_tasks[i]) if total_tasks[i] > 0 else 0 for i in range(4)]
        easiest, hardest = analyze(avg_score)

        return {
            "Most popular": most_popular,
            "Least popular": least_popular,
            "Highest activity": highest_activity,
            "Lowest activity": lowest_activity,
            "Easiest course": easiest,
            "Hardest course": hardest,
        }

    def get_course_details(self, course_name):
        if course_name not in self.COURSES:
            return None

        index = self.COURSE_INDEX[course_name]
        results = []
        for student_id, data in self.students.items():
            pts = data["points"][index]
            if pts > 0:
                percent = round(pts / self.MAX_POINTS[index] * 100, 1)
                results.append((student_id, pts, percent))

        results.sort(key=lambda x: (-x[1], int(x[0])))
        return results

    def notify_students(self):
        notified_student_ids = set()
        for student_id, student in self.students.items():
            messages_sent = 0
            for i, course in enumerate(self.COURSES):
                if student["points"][i] >= self.MAX_POINTS[i] and (student_id, i) not in self.notifications_sent:
                    print(f"To: {student['email']}")
                    print("Re: Your Learning Progress")
                    print(f"Hello, {student['name']}! You have accomplished our {course} course!")
                    self.notifications_sent.add((student_id, i))
                    messages_sent += 1
            if messages_sent > 0:
                notified_student_ids.add(student_id)
        print(f"Total {len(notified_student_ids)} students have been notified.")


def main():
    platform = EnhancedLearningPlatform()
    print("Learning Progress Tracker")

    while True:
        command = input().strip().lower()

        if command == "exit":
            print("Bye!")
            break

        elif command == "add students":
            print("Enter student credentials or 'back' to return:")
            count = 0
            while True:
                line = input().strip()
                if line == "back":
                    break
                parts = line.split()
                if len(parts) < 3:
                    print("Incorrect credentials.")
                    continue
                first_name, last_name, email = parts[0], " ".join(parts[1:-1]), parts[-1]
                response = platform.add_student(first_name, last_name, email)
                print(response)
                if response == "The student has been added.":
                    count += 1
            print(f"Total {count} students have been added.")

        elif command == "list":
            print(platform.list_students())

        elif command == "add points":
            print("Enter an id and points or 'back' to return:")
            while True:
                line = input().strip()
                if line == "back":
                    break
                parts = line.split()
                print(platform.add_points(parts[0], parts[1:]))

        elif command == "find":
            print("Enter an id or 'back' to return:")
            while True:
                line = input().strip()
                if line == "back":
                    break
                print(platform.find_student(line))

        elif command == "statistics":
            print("Type the name of a course to see details or 'back' to quit:")
            stats = platform.get_statistics()
            for label, value in stats.items():
                print(f"{label}: {', '.join(value)}")

            while True:
                line = input().strip()
                if line.lower() == "back":
                    break
                course_key = line.lower()
                course_name = EnhancedLearningPlatform.COURSE_LOOKUP.get(course_key)
                if course_name:
                    details = platform.get_course_details(course_name)
                    print(course_name)
                    print("id    points    completed")
                    for student_id, points, percent in details:
                        print(f"{student_id} {points:<10} {percent}%")
                else:
                    print("Unknown course.")

        elif command == "notify":
            platform.notify_students()

        elif command == "back":
            print("Enter 'exit' to exit the program")

        elif command == "":
            print("No input.")

        else:
            print("Unknown command!")


if __name__ == "__main__":
    main()
