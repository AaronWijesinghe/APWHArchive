import os
import json

bold = "\033[1m"
underline = "\033[4m"
end = "\033[0m"

def get_dir_size(path="."):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

version = "v0/20241118"

fileMissing = False
os.system("clear || cls")
print(f"{bold}[DEV] APWHArchive | File Checker{end}")
print(f"Client Version: {version}\n")

def generate_units():
    global units
    units = json.loads(open("data.json", "r").read())

generate_units()
for unit in units:
    unit["filesize"] = get_dir_size(f"{unit["lessons"][0]["lesson"].replace(os.path.basename(unit["lessons"][0]["lesson"]), "")}")
    print(f"[Unit: {unit["title"]} | Filesize: {round(unit["filesize"] / 1024**2, 2)} MB]")
    for lesson in unit["lessons"]:
        if os.path.exists(lesson["lesson"]):
            print(f"Lesson '{lesson["name"]}' exists.")
        else:
            fileMissing = True
            del lesson
            print(f"Lesson '{lesson["name"]}' DOES NOT exist.")
            print(f"  - Expected Location: {lesson["lesson"]}")
        if "classwork" in lesson.keys():
            if os.path.exists(lesson["classwork"]):
                print(f"  - Classwork for '{lesson["name"]}' exists.")
            else:
                fileMissing = True
                del lesson["classwork"]
                print(f"  - Classwork for '{lesson["name"]}' DOES NOT exist.")
                print(f"    -> Expected Location: {lesson["classwork"]}")
    if "assignments" in unit.keys():
        print("\nAssignments:")
        for assignment in unit["assignments"]:
            if "assignment" in assignment.keys():
                if os.path.exists(assignment["assignment"]):
                    print(f"  - Assignment '{assignment["name"]}' exists.")
                else:
                    fileMissing = True
                    print(f"  - Assignment '{assignment["name"]}' DOES NOT exist.")
                    print(f"    -> Expected Location: {assignment["assignment"]}")
                    del assignment
            if "material" in assignment.keys():
                if os.path.exists(assignment["material"]):
                    print(f"  - Material '{assignment["material"]}' exists.")
                else:
                    fileMissing = True
                    print(f"  - Material '{assignment["material"]}' DOES NOT exist.")
                    del assignment
    print("")
if fileMissing:
    print("Some files are missing. Their expected paths are displayed above.")
    input("If these files aren't present, APWHArchive will still function but won't show content using the files. ")

while True:
    os.system("clear || cls")
    print(f"{bold}[DEV] APWHArchive{end}")
    print(f"Client Version: {version}")

    print(f"\n{underline}Announcements:{end}")
    print("APWHArchive is NOT ready for release and individual files are NOT available for download.")
    print("However, it is almost ready for BETA testing.")
    print("Before the BETA release, I will make sure that all available APWH files are available to download.")

    print(f"\n{underline}Plans:{end}")
    print("1. Make a dedicated assignment + classwork function, with a way to save assignments separately")
    print("2. Upload all APWH data to GitHub or whichever platform I see fit")
    print("3. Release APWHArchive in a ready, working state by SHSAT results day or earlier")

    print(f"\n{underline}Units:{end}")
    for unit in range(len(units)):
        print(f"[{unit}] {units[unit]['title']}")
    unit = input("\nEnter the unit you would like to view: ")
    try:
        unit = int(unit)
        if unit not in range(0, 6):
            input("That unit doesn't exist (yet!). ")
            continue
    except:
        input("That unit doesn't exist (yet!). ")
        continue

    current_unit = units[unit]
    
    os.system("clear || cls")
    print(f"[DEV] APWHArchive Viewer")
    print(f"{bold}Unit: {current_unit['title']}{end}")

    print(f"\n{underline}Lessons in this unit:{end}")
    for lesson in range(len(current_unit["lessons"])):
        print(f"[{lesson + 1}] {current_unit["lessons"][lesson]["name"]}")
    lesson = input("\nEnter the lesson you would like to view: ")
    try:
        lesson = int(lesson) - 1
        if lesson in range(0, len(current_unit["lessons"])):
            pass
        else:
            input("That lesson doesn't exist. ")
            continue
    except:
        input("That lesson doesn't exist. ")
        continue

    os.system("clear || cls")
    print("[DEV] APWHArchive")
    print(f"\n{bold}Lesson: {current_unit["lessons"][lesson]["name"]}{end}")
    print(f"Location of Lesson: {current_unit["lessons"][lesson]["lesson"]}")
    if "classwork" in current_unit["lessons"][lesson].keys():
        print(f"Classwork: {current_unit["lessons"][lesson]["classwork"]}")
    input("\nPress Enter to open the slideshow for this lesson. ")
    os.system(f"cp \"{current_unit['lessons'][lesson]['lesson']}\" ./lesson.pptx || copy \"{current_unit['lessons'][lesson]['lesson']}\" ./lesson.pptx")
    os.system("open lesson.pptx || start lesson.pptx")
    if "classwork" in current_unit["lessons"][lesson].keys():
        input("Press Enter to open the classwork for this lesson. ")
        os.system(f"cp \"{current_unit['lessons'][lesson]['classwork']}\" ./classwork.docx || copy \"{current_unit['lessons'][lesson]['classwork']}\" ./classwork.docx")
        os.system("open classwork.docx || start classwork.docx")
    else:
        print("There is no classwork for this lesson!")
    print(f"\n{bold}DO THIS WHEN YOU ARE DONE!{end}")
    print("Temporary files (copy of the lesson) will be deleted.")
    print("[WIP] Classwork will be saved to ./Classwork/?.docx!")
    input("Press Enter if you are DONE with everything above. ")
    os.system("rm lesson.pptx || erase lesson.pptx")

    generate_units()
    # os.system("mv classwork.docx ./classwork/ || copy classwork.docx ./classwork/ && erase classwork.docx")