import os

base_dir = os.path.dirname(__file__)


student_path = os.path.join(base_dir,"..","data","students.txt")
subjects_path = os.path.join(base_dir,"..","data","subjects.txt")
results_path = os.path.join(base_dir,"..","data","results_summary_.txt")
passed_path = os.path.join(base_dir,"..","data","passed_students_.txt")
failed_path = os.path.join(base_dir,"..","data","failed_students_.txt")
rank_list_path = os.path.join(base_dir,"..","data","rank_list_.txt")
toppers_path = os.path.join(base_dir,"..","data","subject_toppers_.txt")
subject_average_path = os.path.join(base_dir,"..","data","subject_averages_.txt")
analytics_path = os.path.join(base_dir,"..","data","data_analytics.txt")
grade_analytics_path = os.path.join(base_dir, "..", "data","grade_analytics.txt")
subject_analytics_path = os.path.join(base_dir, "..", "data","subject_analytics.txt")

lines=[]
subjects=[]
failed_students=[]
passed_students=[]
results_summary=[]
rank_data = [] #to store dictionaries for every student for sorting.. 
rank_list_output =[]
subject_toppers=[]
subject_average_output=[]

# FOR ANALYTICS
subject_analytics_output=[]
min_avg = 101
max_avg = -1
max_subject_difficulty=""
min_subject_difficulty=""
grade_counts = {"AA": 0, "AB": 0, "BB": 0, "BC": 0, "CC": 0, "CD": 0, "DD": 0}  

def get_grade(avg):
    if avg>=90:
        return "AA"
    elif avg>=80:
        return "AB"
    elif avg>=70:
        return "BB"
    elif avg>=60:
        return "BC"
    elif avg>=50:
        return "CC"
    elif avg>=40:
        return "CD"
    else:
        return "DD"


with open(student_path,"r") as s:
    lines = s.readlines() #f.readlines used to read tuples or lists i.e multiple strings in different lines at once 

with open(subjects_path,"r") as b:
    subjects = b.read().split() #still we have to break it in parts to access each subject..


for currline in lines:
    parts = currline.split()

    if not parts: # if currline is empty i.e no data of student on that line then continue to next line..
        continue

    name = parts[0]
    attendance = int(parts[1])
    scoreslist = list(map(int , parts[2:]))
    
    totalsubject = len(scoreslist)
    totalmarks = sum(scoreslist)
    avg = (totalmarks)/(totalsubject)

    grade = get_grade(avg)

    #UPDATE GRADE COUNT FOR ANALYTICS(GRADE LINE)
    grade_counts[grade] = grade_counts[grade] + 1

    if avg<40 or attendance<75 :
        status = "FAIL"
    else:
        status="PASS"
    
    results_summary.append(f"{name:<12}| Avg: {avg:<8.2f} | Grade: {grade:<8} | Attendance: {attendance:<8}% | Status: {status}\n")

    if status=="PASS":
        passed_students.append(f"{name:<12}| Status: {status}\n")
    else:

        if avg<40 and attendance<75 :
            reason = "Low Average and Low Attendance"
        elif attendance<75:
            reason = "Low Attendance"
        elif avg<40:
            reason = "Low Average"
        failed_students.append(f"{name:<12}| Status: {status:<8} | Reason of Failure:   {reason}\n")
    
    rank_data.append(
        {
            "name" : name,
            "totalmarks" : totalmarks,
            "avg" : avg,
            "grade" : grade,
            "scores" : scoreslist
        }
    )


#CREATE RANK LIST..
rank_data.sort(key=lambda x: x["totalmarks"],reverse=True)

rank_number=1
for student in rank_data:
    
    #OVERALL RANKLIST.TXT (BY TOTALMARKS)
    name = student["name"]
    totalmarks = student["totalmarks"]
    avg = student["avg"]
    grade = student["grade"]    
    line = f"{rank_number:8} | {name:<12} | Total_Marks: {totalmarks:<8} | Avg: {avg:<8} | Grade: {grade:<8}\n"
    rank_list_output.append(line)
    rank_number=rank_number+1
    

#CREATE 5 SUBJECT FILES
for i in range(len(subjects)):

    sub_name = subjects[i]
    subject_file_path = os.path.join(base_dir,"..","data",f"{sub_name}_rank_list_.txt")

    #SORTING BY EACH SUBJECT MARKS T0 GET RANKLIST FOR EACH SUBJECT
    rank_data.sort(key=lambda x:x["scores"][i] , reverse=True)
    sub_data_output=[]
    sub_failed_output=[]

    total_sub_score = 0 #needed for average 
    sub_pass_count = 0 #needed for analytics
    
    
    #TOPPER [AFTER REVERSE SORTING RANK[0] IS TOPPER FOR THAT SUBJECT]
    top_student = rank_data[0] 
    top_name = top_student["name"]
    top_score = top_student["scores"][i]
    subject_toppers.append(f"Subject: {sub_name:<12} | Topper: {top_name:<12} | Score: {top_score}\n")

    
    #AFTER SORTING VIA scores[i] i.e i+1th subject we create subject wise rank list and subject wise failed students rank list
    rank_number=1
    for student in rank_data:

        s_name = student["name"]
        s_score = student["scores"][i]
        s_grade = get_grade(s_score)
        line = f"{rank_number:<8} | {s_name:<12} | Subject: {sub_name:<12} |  Score: {s_score:<8} | Grade: {s_grade:<8}\n"
        sub_data_output.append(line)
        rank_number=rank_number+1

        total_sub_score = total_sub_score + s_score

        
        if s_score>=40:
            sub_pass_count = sub_pass_count + 1

        #ADDING FAILED STUDENTS IN SUB_FAILED_OUTPUT
        if s_score<40 :
            line = f"{s_name:<12} | Subject : {sub_name:12} | Grade : {s_grade:<8} | Status : FAIL\n"
            sub_failed_output.append(line)

   
    # CALCULATE SUBJECT AVERAGE BEFORE ITERATING TO NEXT SUBJECT AND ADDING IT TO SUBJECT_AVERAGE_OUTPUT
    sub_avg = (total_sub_score)/len(rank_data)
    line=f"Subject: {sub_name:<12} | Average: {sub_avg:.3f}\n"
    subject_average_output.append(line)


    # ANALYTICS...

    # TRACK HARDEST/EASIEST SUBJECT
    if sub_avg < min_avg:
        min_avg = sub_avg
        max_subject_difficulty = sub_name
    if sub_avg > max_avg:
        max_avg = sub_avg
        min_subject_difficulty = sub_name
    
    #APPEND PASSED , FAILED COUNT AND PASS RATE FOR EACH SUB IN ANALYTICS_OUTPUT LIST
    pass_rate = ((sub_pass_count)/len(rank_data))*100
    analytics_line = f"Subject: {sub_name:<12} | Passed: {sub_pass_count:<3} | Fail: {len(rank_data)-sub_pass_count:<3} | Pass Rate: {pass_rate:>6.2f}%\n"
    subject_analytics_output.append(analytics_line)



    #FOOSTER LINE OF CLASS AVG AT THE END OF SUBJECT WISE RANKLIST
    sub_data_output.append("-" * 35 + "\n")
    sub_data_output.append(f"CLASS AVERAGE: {sub_avg:.3f}\n")

    # ALL FAILED STUDENTS (sub_failed_output) IN SUB_FAILED.TXT FILES FOR EACH SUBJECT  
    subject_failure_path = os.path.join(base_dir,"..","data",f"{sub_name}_failed_students_.txt")
    with open(subject_failure_path,"w") as f_sub:
        f_sub.writelines(sub_failed_output)
        

    #RANK LIST FOR EVERY SUBJECT TO ADD IN SUBJECT.TXT FILE FOR EVERY SUBJECT
    with open(subject_file_path,"w") as j:
        j.writelines(sub_data_output)



# FINAL ANALYTICS = SUBJECT WISE ANALYTICS(COUNT OF PASS,FAIL , PASSRATE) +
#  OVERALL ANALYTICS(OVERALL PASS FAIL COUNT AND PASS RATE) +
#  grade analytics
overall_topper = rank_data[0]
overall_analytics = [
    "=========================================\n",
    "        CLASS ANALYTICS SUMMARY\n",
    "=========================================\n",
    f"Total Students: {len(rank_data)}\n",
    f"Overall Topper: {overall_topper['name']} ({overall_topper['totalmarks']} Marks)\n",
    f"Hardest Subject: {max_subject_difficulty} (Avg: {min_avg:.2f})\n",
    f"Easiest Subject: {min_subject_difficulty} (Avg: {max_avg:.2f})\n",
    "-----------------------------------------\n",
    "SUBJECT-WISE DETAIL:\n"
] 

#ADDING GRADE COUNT FEATURE....
grade_dist_lines = ["\n-----------------------------------------\n", "OVERALL GRADE DISTRIBUTION:\n"]
for g in ["AA", "AB", "BB", "BC", "CC", "CD", "DD"]:
    grade_dist_lines.append(f"Grade {g:<2}: {grade_counts[g]} students\n") # MAINTAINED A DICTIONARY FOR GRADE [KEY="AA" AND VALUE = COUNT OF AA(INT)] 


final_analytics = overall_analytics + subject_analytics_output + grade_dist_lines   

#FINAL FILE WRITES..

with open (results_path,"w") as r:
    r.writelines(results_summary)

with open (passed_path,"w") as p:
    p.writelines(passed_students)

with open (failed_path,"w") as f:
    f.writelines(failed_students)

with open (rank_list_path,"w") as l:
    l.writelines(rank_list_output)

with open (toppers_path,"w") as t:
    t.writelines(subject_toppers)

with open (subject_average_path,"w") as a:
    a.writelines(subject_average_output)

with open (analytics_path,"w") as aly:
    aly.writelines(final_analytics)

with open (subject_analytics_path,"w") as sub_a:
    sub_a.writelines(subject_analytics_output)

with open (grade_analytics_path,"w") as g:
    g.writelines(grade_dist_lines)


#STUDENT SEARCH FUNCTION

# DESIGN 
print(40*"-" + "\n")
print("STUDENT SEARCH SYSTEM")
print(40*"-")

# .strip() removes any accidental spaces the user might type before or after the name.
# Example: " Rahul " becomes "Rahul
search_name = input("Enter name to look up: ").strip()

found = False
for student in rank_data:
    
    s_name = student["name"]
    # This ensures "RAHUL", "rahul", and "Rahul" are all seen as the same name.
    if s_name.lower() == search_name.lower():
        
        s_totalmarks = student["totalmarks"]
        s_avg = student["avg"]
        s_grade = student["grade"]

        print(f"\nReport for: {s_name}")
        print("-" * 20) # A smaller divider for the sub-header
        
        # Pulling data from the dictionary keys we defined at the start of the script.
        print(f"Overall Total : {s_totalmarks}")
        print(f"Overall Avg   : {s_avg:.2f}")
        print(f"Overall Grade : {s_grade}")
        print("\nSubject-wise Breakdown:")
        

        #SUBJECT WISE BREAKDOWM
        for i in range(len(subjects)):
            sub_name = subjects[i]
            sub_score = student["scores"][i]
            print(f"{sub_name:<12}: {sub_score} | Grade : {get_grade(sub_score)}")
        
        found = True
        break

# If the loop finishes and 'found' is still False, it means the name wasn't in our list.
if found == False:
    print(f"Error: No student found with the name '{search_name}'.")
    
