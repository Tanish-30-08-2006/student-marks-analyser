import os
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

base_dir = os.path.dirname(__file__)

#----------------------------------PATHS FOR FILES AND FOLDERS----------------------------------#

student_path                       = os.path.join(base_dir,"..","data","students.txt")
subjects_path                      = os.path.join(base_dir,"..","data","subjects.txt")
results_path                       = os.path.join(base_dir,"..","data","results_summary_.txt")
passed_path                        = os.path.join(base_dir,"..","data","passed_students_.txt")
failed_path                        = os.path.join(base_dir,"..","data","failed_students_.txt")
rank_list_path                     = os.path.join(base_dir,"..","data","rank_list_.txt")
toppers_path                       = os.path.join(base_dir,"..","data","subject_toppers_.txt")
subject_average_path               = os.path.join(base_dir,"..","data","subject_averages_.txt")
analytics_path                     = os.path.join(base_dir,"..","data","data_analytics.txt")
grade_analytics_path               = os.path.join(base_dir, "..", "data","grade_analytics.txt")
subject_analytics_path             = os.path.join(base_dir, "..", "data","subject_analytics.txt")
grade_chart_image_path             = os.path.join(base_dir,"..","data","grade_visual_chart.png")
average_chart_image_path           = os.path.join(base_dir,"..","data","subject_toughness_chart.png")
pass_fail_count_chart_path         = os.path.join(base_dir,"..","data", "pass_rate_chart.png")
max_score_per_subject_chart_path   = os.path.join(base_dir,"..","data", "max_score_per_subject.png")
grade_pie_chart_path               = os.path.join(base_dir, "..", "data", "grade_pie_distribution.png")
heat_map_scores_path               = os.path.join(base_dir,"..","data","heat_map_scores.png")
attendance_scatter_chart_path      = os.path.join(base_dir,"..","data","attendance_vs_totalmarks_chart.png")



# Create a specific FOLDER for PDF report cards
pdf_reports_dir_path                   = os.path.join(base_dir, "..", "data", "student_pdf_reports")
if not os.path.exists(pdf_reports_dir_path):
    os.makedirs(pdf_reports_dir_path)



# Path for the individual report cards FOLDER
report_cards_dir_path                   = os.path.join(base_dir, "..", "data", "student_report_cards")
#create the folder if it doesn't exist
if not os.path.exists(report_cards_dir_path):
    os.makedirs(report_cards_dir_path)

# Path for certificates for top 3 students FOLDER 
certificates_dir_path = os.path.join(base_dir, "..", "data", "certificates_pdf")
if not os.path.exists(certificates_dir_path):
    os.makedirs(certificates_dir_path)
    

#--------------------------INITIALIZING DATA FOR OUTPUT [FILES] [FOLDER] [PDF] -----------------------------#

lines=[]
subjects=[]
failed_students=[]
passed_students=[]
results_summary=[]
rank_data = [] #to store dictionaries for every student for sorting.. 
rank_list_output =[]
subject_toppers=[]
subject_average_output=[]
subject_averages=[] #storing subject averages in a list for y axis of bar chart to plot..

#storing pass and fail counts of subjects for pass vs fail count chart
pass_counts= []
fail_counts = []

#storing max scores of every subject and create a bar chart
max_scores_per_subject= []

# FOR ANALYTICS
subject_analytics_output=[]
min_avg = 101
max_avg = -1
max_subject_difficulty=""
min_subject_difficulty=""
grade_counts = {"AA": 0, "AB": 0, "BB": 0, "BC": 0, "CC": 0, "CD": 0, "DD": 0}  


#----------------------------------FUNCITONS : [CHARTS GENERATION] [PDF GENERATION]-------------------------------------------------#


def generate_subject_average_chart(subjects , subject_averages, average_chart_image_path):
    
    x_label = subjects
    y_label = subject_averages
    
    plt.figure(figsize=(13,13))
    bars = plt.bar(x_label,y_label, color ="mediumseagreen" ,edgecolor = "darkgreen" , alpha = 0.6,width =0.4)
    plt.bar_label( bars , padding =3 ,fontsize=12,fontweight ='bold')
    
    #ADD A PASSING THRESHHOLD LINE OF 40
    plt.axhline( y=40 , color ="red" , linestyle ="--" ,label ="Passing mark =40" ) #axis horizontal line
    plt.title("Class Average per Subject", fontsize=14)
    plt.xlabel("Subject Name")
    plt.ylabel("Average Marks")
    plt.legend() # Shows the red line label
    
    plt.savefig(average_chart_image_path)
    plt.show()
    plt.close()

def generate_grade_chart(grade_counts, grade_chart_image_path):
    
    x_label = list(grade_counts.keys())
    y_label = list(grade_counts.values())

    plt.figure(figsize=(6,6))

    bars = plt.bar(x_label , y_label , color = "skyblue" , edgecolor = "salmon",alpha =0.4,width = 0.4)
    plt.bar_label(bars,padding=3,fontsize=10,fontweight ='bold')

    plt.xlabel("Grade", fontsize =10)
    plt.ylabel("Grade count" , fontsize = 10)
    plt.title("Grade Distribution",fontsize =12)
    

    plt.savefig(grade_chart_image_path)
    plt.show()
    plt.close()

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

def generate_pass_rate_chart (subjects,pass_counts,fail_counts,pass_fail_count_chart_path):

    plt.figure(figsize=(12,12))

    #Draw the Pass bars at the bottom
    bars1 = plt.bar(subjects, pass_counts, label='Passed', color='mediumseagreen', width=0.5)
    
    # Draw the Fail bars STARTING from where the Pass bars ended
    # The 'bottom' parameter tells Matplotlib where to start drawing
    bars2 = plt.bar(subjects ,fail_counts ,bottom = pass_counts,label='failed',color ='tomato', width =0.5)

    plt.bar_label(bars1 ,label_type='center', padding =3 , color ='white' , fontweight ='bold')
    plt.bar_label(bars2, label_type='center',padding=3, color ='white',fontweight ='bold')

    plt.title("Pass vs Fail Distribution per Subject")
    plt.ylabel("Number of Students")
    plt.legend()
    
    plt.savefig(pass_fail_count_chart_path)
    plt.show()
    plt.close()

def generate_max_scores_per_subject_chart( subjects, max_scores_per_subject , max_score_per_subject_chart_path):

    x_label = subjects
    y_label = max_scores_per_subject
    
    plt.figure(figsize=(12,12))
    
    bars = plt.bar(x_label, y_label , color = 'gold', edgecolor='darkgoldenrod',alpha = 0.5,width = 0.5)
    plt.bar_label(bars,label_type='center', padding=3, fontsize=10, fontweight='bold')

    plt.axhline(y=100, color ='black' , linestyle=':', label='Perfect Score (100)')

    plt.title("Maximum Score achieved per Subject", fontsize=14)
    plt.xlabel("Subject",fontsize =11)
    plt.ylabel("Max score",fontsize =11)
    
    plt.ylim(0,110) # Set limit slightly higher than 100 so the bars don't hit the ceiling

    plt.tight_layout() #t automatically adjusts the padding so your subject names (like "Electronics") don't get cut off at the bottom of the image.
    plt.savefig(max_score_per_subject_chart_path)
    plt.show()
    plt.close()

def generate_grade_pie_chart(grade_counts, grade_pie_chart_path):
   
    labels = list(grade_counts.keys())
    values = list(grade_counts.values())
    set_explode = [0.1,0.1,0.1,0.1,0.1,0.1,0.1]

    plt.figure(figsize=(8, 8))

    plt.pie(values, labels=labels, autopct='%1.1f%%', explode=set_explode, startangle=90, colors=['gold', 'lightskyblue', 'lightgreen', 'orange', 'salmon', 'plum', 'tomato'],shadow=True)
    
    plt.title("Grade Distribution Percentage", fontsize=14)

    plt.savefig(grade_pie_chart_path)
    plt.show()
    plt.close()

def generate_heat_map_scores(heat_map_scores,heat_map_names,subjects,heat_map_scores_path):
    
    plt.figure(figsize=(12,12))

    sns.heatmap(heat_map_scores ,annot =True , xticklabels=subjects , yticklabels = heat_map_names, cmap = 'RdYlGn' ,vmin=0,vmax=100)
    plt.title("Student Performance Map")
    plt.savefig(heat_map_scores_path)
    plt.show()
    plt.close()

def generate_final_report_pdf(output_path, images, analytics_file):
    # 1. Initialize PDF
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- PAGE 1: COVER & HEATMAP ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 20, "Academic Performance Report", ln=1, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Class Performance Heatmap (Overall View):", ln=1)
    # Positioning the big heatmap
    pdf.image(images['heatmap'], x=10, y=40, w=190)
    
    # --- PAGE 2: GRADE DISTRIBUTION ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Grade Distribution Analysis", ln=1, align='C')
    
    # Placing Pie and Bar chart side-by-side or stacked
    pdf.image(images['grade_pie'], x=10, y=30, w=90)
    pdf.image(images['grade_bar'], x=105, y=30, w=90)
    
    pdf.set_y(130) # Move cursor down after images
    pdf.cell(0, 10, "Subject Toughness & Pass Rates", ln=1, align='C')
    pdf.image(images['pass_fail'], x=10, y=140, w=190, h=120)

    # --- PAGE 3: SUBJECT AVERAGES & MAX SCORES ---
    pdf.add_page()
    pdf.image(images['subject_avg'], x=10, y=20, w=190, h=120)
    pdf.image(images['max_score'], x=10, y=150, w=190, h=120)
    
    # --- PAGE 4: CORRELATION ANALYSIS ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "4. Attendance Correlation Analysis", ln=1, align='C')
    pdf.image(images['attendance_scatter'], x=10, y=30, w=190)

    # --- PAGE 5: FULL DATA ANALYTICS TEXT ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Detailed Data Analytics Summary", ln=1)
    pdf.ln(5)
    
    pdf.set_font("Courier", size=10) # Using Courier for that 'text-file' look
    with open(analytics_file, "r") as f:
        for line in f:
            # multi_cell handles the wrapping so text doesn't go off page
            pdf.multi_cell(0, 6, line)

    # 5. Save the PDF
    pdf.output(output_path)
    print(f"\nSUCCESS: Final report generated at {output_path}")

def generate_subject_teacher_report(sub_name, sub_avg, sub_topper_list, sub_fail_list, save_path):

    pdf = FPDF()
    pdf.add_page()
    
    # 1. Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Subject Report: {sub_name}", ln=1, align='C')
    pdf.ln(10)
    
    # 2. Stats
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Class Average: {sub_avg:.2f}", ln=1)
    pdf.ln(5)
    
    # 3. Toppers Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Subject Toppers:", ln=1)
    pdf.set_font("Courier", size=10)
    for topper in sub_topper_list:
        pdf.multi_cell(0, 6, topper)
    pdf.ln(10)
    
    # 4. Failure/Action List
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(255, 0, 0) # Set text to Red
    pdf.cell(0, 10, "Students Requiring Attention (Failed):", ln=1)
    pdf.set_font("Courier", size=10)
    pdf.set_text_color(0, 0, 0) # Back to Black
    
    if not sub_fail_list:
        pdf.cell(0, 10, "No failures in this subject!", ln=1)
    else:
        for fail_line in sub_fail_list:
            pdf.multi_cell(0, 6, fail_line)
            
    pdf.output(save_path)

def generate_attendance_scatter_chart(attendance_list, total_marks_list,attendance_scatter_chart_path):
    
    plt.figure(figsize=(10,6))

    # s=100 is size, alpha is transparency to see overlapping dots
    plt.scatter(attendance_list,total_marks_list,color ='darkorchid',s=100,alpha=0.6,edgecolors='black')
    plt.title("Correlation: Attendance % vs Total Marks", fontsize=14)
    plt.xlabel("Attendance (%)", fontsize=12)
    plt.ylabel("Total Marks", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(attendance_scatter_chart_path)
    plt.show()
    plt.close()
    
def generate_student_report_card(student, subjects, report_cards_dir_path):
    s_name = student['name'].replace(" ", "_")
    file_path = os.path.join(report_cards_dir_path, f"{s_name}_Report_Card.txt")
    
    # Determine pass/fail status for the header
    status = "PASS" if student['avg'] >= 40 and student['attendance'] >= 75 else "FAIL"

    with open(file_path, "w") as f:
        f.write(" ----------------------------------------------------\n")
        f.write(f"          ANNUAL REPORT : {s_name}                  \n")
        f.write(" ----------------------------------------------------  \n\n")
        f.write(f" STUDENT NAME  : {student['name']}\n")
        f.write(f" ATTENDANCE    : {student['attendance']}%\n")
        f.write(f" RESULT STATUS : {status}\n")
        f.write("\n----------------------------------------------------\n")
        f.write(f" {'SUBJECT':<20} | {'SCORE':<10} | {'GRADE':<8}\n")
        f.write("----------------------------------------------------\n")
        
        for i in range(len(subjects)):
            score = student['scores'][i]
            f.write(f" {subjects[i]:<20} | {score:<10} | {get_grade(score):<8}\n")
            
        f.write("----------------------------------------------------\n")
        f.write(f" FINAL AVERAGE : {student['avg']:.2f}%\n")
        f.write(f" OVERALL GRADE : {student['grade']}\n")
        f.write("====================================================\n")
        
        # Professional Comment Logic
        comment = "Excellent academic standing." if student['grade'] == "AA" else \
                  "Satisfactory performance." if status == "PASS" else \
                  "Academic probation - Immediate counseling required."
        f.write(f" REMARKS: {comment}\n")
        f.write("====================================================\n")

def generate_excellence_certificate_pdf(student, certificates_dir_path, rank):

    safe_name = student['name'].replace(" ", "_")
    file_path = os.path.join(certificates_dir_path, f"{safe_name}_Certificate.pdf")
    
    # Initialize PDF in Landscape mode (L) for a wider certificate look
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # --- DRAW BORDERS ---
    pdf.set_line_width(2)
    pdf.rect(10, 10, 277, 190) # Outer Border
    pdf.set_line_width(0.5)
    pdf.rect(12, 12, 273, 186) # Inner Decorative Border
    
    # --- HEADER ---
    pdf.set_font("Times", 'B', 30)
    pdf.set_text_color(184, 134, 11) # Dark Golden Color
    pdf.cell(0, 40, "CERTIFICATE OF EXCELLENCE", ln=1, align='C')
    
    # --- BODY TEXT ---
    pdf.set_text_color(0, 0, 0) # Back to Black
    pdf.set_font("Times", 'I', 18)
    pdf.cell(0, 15, "This is to certify that", ln=1, align='C')
    
    pdf.set_font("Times", 'B', 24)
    pdf.cell(0, 20, student['name'], ln=1, align='C')
    
    pdf.set_font("Times", '', 16)
    pdf.multi_cell(0, 10, f"has achieved RANK {rank} in the Semester Evaluation\n" +
                   f"with an outstanding score of {student['avg']:.2f}%.", align='C')
    
    pdf.ln(10)
    pdf.set_font("Times", 'I', 14)
    pdf.cell(0, 10, "Awarded for demonstrating exceptional academic prowess and dedication.", ln=1, align='C')
    
    # --- SIGNATURE SECTION ---
    pdf.set_y(160)
    pdf.set_font("Times", 'B', 12)
    pdf.cell(100, 10, "__________________________", ln=0, align='C')
    pdf.cell(100, 10, "", ln=0) # Spacer
    pdf.cell(0, 10, "__________________________", ln=1, align='C')
    
    pdf.cell(100, 10, "Head of Department", ln=0, align='C')
    pdf.cell(100, 10, "", ln=0) # Spacer
    pdf.cell(0, 10, "Date of Issue: 2026-02-19", ln=1, align='C')

    pdf.output(file_path)

def generate_student_report_card_pdf(student, subjects, report_cards_dir_path):
    # Sanitize name for filename
    s_name = student['name'].replace(" ", "_")
    file_path = os.path.join(report_cards_dir_path, f"{s_name}_Official_Report.pdf")
    
    # Initialize PDF in Portrait mode
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # --- 1. DECORATIVE BORDER ---
    pdf.set_line_width(1)
    pdf.rect(5, 5, 200, 287) # Outer frame
    
    # --- 2. INSTITUTIONAL HEADER (NAVY BLUE) ---
    pdf.set_fill_color(44, 62, 80) # Dark Navy
    pdf.rect(5, 5, 200, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 22)
    pdf.cell(0, 25, "INSTITUTE OF TECHNOLOGY", ln=1, align='C')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 5, "OFFICIAL ACADEMIC TRANSCRIPT | 2026", ln=1, align='C')
    
    # --- 3. STUDENT METADATA ---
    pdf.ln(15)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 11)
    # Row 1: Name and Year
    pdf.cell(100, 8, f"STUDENT NAME: {student['name'].upper()}", 0, 0)
    pdf.cell(0, 8, f"ACADEMIC YEAR: 2025-2026", 0, 1, 'R')
    
    # Row 2: Attendance and Status
    pdf.cell(100, 8, f"ATTENDANCE: {student['attendance']}%", 0, 0)
    status = "PASS" if student['avg'] >= 40 and student['attendance'] >= 75 else "FAIL"
    pdf.cell(0, 8, f"RESULT STATUS: {status}", 0, 1, 'R')
    
    pdf.ln(5)
    pdf.line(10, 75, 200, 75) # Divider line
    
    # --- 4. ACADEMIC PERFORMANCE TABLE ---
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(230, 230, 230) # Light grey header
    pdf.cell(80, 12, " SUBJECT NAME", 1, 0, 'L', True)
    pdf.cell(40, 12, " MARKS", 1, 0, 'C', True)
    pdf.cell(40, 12, " GRADE", 1, 0, 'C', True)
    pdf.cell(30, 12, " RESULT", 1, 1, 'C', True)
    
    pdf.set_font("Courier", '', 12)
    for i, sub in enumerate(subjects):
        score = student['scores'][i]
        grade = get_grade(score)
        res = "PASS" if score >= 40 else "FAIL"
        
        pdf.cell(80, 10, f" {sub}", 1)
        pdf.cell(40, 10, f" {score}/100", 1, 0, 'C')
        pdf.cell(40, 10, f" {grade}", 1, 0, 'C')
        
        # Color fail result in Red for emphasis
        if res == "FAIL": 
            pdf.set_text_color(200, 0, 0)
        pdf.cell(30, 10, f" {res}", 1, 1, 'C')
        pdf.set_text_color(0, 0, 0)

    # --- 5. PERFORMANCE SUMMARY BOX ---
    pdf.ln(10)
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, pdf.get_y(), 190, 30, 'F')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, " PERFORMANCE SUMMARY", 0, 1)
    pdf.set_font("Arial", '', 11)
    pdf.cell(60, 8, f" Total Marks: {student['totalmarks']}", 0, 0)
    pdf.cell(70, 8, f" Average Percentage: {student['avg']:.2f}%", 0, 0)
    pdf.cell(0, 8, f" Final Class Grade: {student['grade']}", 0, 1)
    
    # --- 6. FORMAL REMARKS & SIGNATURES ---
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "GENERAL REMARKS:", ln=1)
    pdf.set_font("Arial", 'I', 11)
    
    # Custom feedback based on performance
    comment = "Excellent academic standing. Eligible for Semester Honors." if student['avg'] >= 85 else \
              "Satisfactory performance. Focus on consistent attendance." if status == "PASS" else \
              "Academic Probation: Mandatory meeting with the Department Head required."
    pdf.multi_cell(0, 8, comment)
    
    # Formal signatures at the bottom
    pdf.set_y(260)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(95, 10, "__________________________", 0, 0, 'C')
    pdf.cell(95, 10, "__________________________", 0, 1, 'C')
    pdf.cell(95, 5, "Controller of Examinations", 0, 0, 'C')
    pdf.cell(95, 5, "Director / Principal", 0, 1, 'C')
    
    pdf.output(file_path)


#----------------------READING INPUT FILES [students.txt] [subjects.txt]--------------------------
with open(student_path,"r") as s:
    lines = s.readlines() #f.readlines used to read tuples or lists i.e multiple strings in different lines at once 

with open(subjects_path,"r") as b:
    subjects = b.read().split() #still we have to break it in parts to access each subject..
    #list of all subjects



for currline in lines:
    parts = currline.split()

    if not parts: # if currline is empty i.e no data of student on that line then continue to next line..
        continue

    #---------BREAKING CURRENT LINE INTO PARTS TO ACCESS [NAME] [ATTENDANCE] [LIST(SCORES)] -----------#
    name = parts[0]
    attendance = int(parts[1])
    scoreslist = list(map(int , parts[2:]))

    
    #-------------- DATA VALIDATION CONSTRAINTS-----------------------#
    is_valid = True
    for score in scoreslist:
        if score < 0 or score > 100:
            print(f"Warning: Skipping {name} due to invalid score ({score}). Marks must be 0-100.")
            is_valid = False
            break
    
    # If any score was invalid, we skip this student entirely
    if is_valid == False:
        continue

    
    # --------------FOR EACH STUDENT [TOTAL MARKS] [OVERALL AVERAGE] [OVERALL GRADE] ---------------
    totalsubject = len(scoreslist)
    totalmarks = sum(scoreslist)
    avg = (totalmarks)/(totalsubject)

    grade = get_grade(avg)

    #--------------UPDATE GRADE COUNT FOR OVERALL ANALYTICS -----------------
    grade_counts[grade] = grade_counts[grade] + 1

    # -------------OVERALL PASS OR FAIL LOGIC ------------------------------
    if avg<40 or attendance<75 :
        status = "FAIL"
    else:
        status="PASS"
    
    # ---------------------------------APPENDING OVERALL RESULT (UNSORTED) OF EVERY STUDENT------------------------------#
    results_summary.append(f"{name:<30}| Avg: {avg:<15.2f} | Grade: {grade:<15} | Attendance: {attendance:<15}% | Status: {status}\n")

    
    # ---------------------------------APPENDING [PASSED STUDENTS:passed_students.txt] [FAILED STUDENTS:failed_students.txt]----------------------#
    if status=="PASS":
        passed_students.append(f"{name:<30}| Status: {status}\n")
    else:

        if avg<40 and attendance<75 :
            reason = "Low Average and Low Attendance"
        elif attendance<75:
            reason = "Low Attendance"
        elif avg<40:
            reason = "Low Average"
        failed_students.append(f"{name:<30}| Status: {status:<15} | Reason of Failure:   {reason}\n")
    
    # -------STORING DATA OF EVERY STUDENT IN A DICTIONARY TO SORT THEM VIA [SUBJECTS:subject_wise_ranklist] [TOTAL MARKS:overall rank list]---------
    rank_data.append(
        {
            "attendance" :attendance,     #storing attendance for attendance vs total marks scatter plot
            "name" : name,
            "totalmarks" : totalmarks,    #overall ranklist sorted by rank_data["total marks"]
            "avg" : avg,
            "grade" : grade,
            "scores" : scoreslist         #subject wise ranklist sorted by rank_data[scores][i] accessing (i+1)th subject marks 
        }
    )


#---------------------RANK LIST SORTED ON TOTAL MARKS----------------------------#
rank_data.sort(key=lambda x: x["totalmarks"],reverse=True)


# --------------------LOGIC FOR TOP TOP 5 STUDENTS FOR CERTIFICATE ALLOCATION------------------#


#students with same total marks get same rank i.e there can be 3 rank 1 students if same total marks 
current_rank = 0
prev_score = -1
count = 0
for student in rank_data:
    # Update rank only if the score changes
    if student["totalmarks"] != prev_score:
        current_rank += 1
    # Stop once we've processed the top 5 rank brackets
    if current_rank > 5:
        break
    # Generate the formal PDF certificate
    generate_excellence_certificate_pdf(student, certificates_dir_path, current_rank)

    # Update prev_score for the next iteration
    prev_score = student["totalmarks"]


# ------------------LOGIC FOR ACCESSING OVERALL TOPPERS OF CLASS (for data_analytics.txt)----------------------#

#logic for multiple overall toppers with same total marks
max_total = rank_data[0]["totalmarks"]
topper_names = "" #empty string for topper names (will add the names in string)

for student in rank_data: 
    if student["totalmarks"] == max_total :   #rank_data still sorted by total marks(reverse) 
        topper_names = topper_names + student["name"] + ", " 
        # Now topper_names contains all  like "overall toppers like "Rahul Priya "
        # Added ", " space and comma for readability no rocket science to confuse



#-------------------------------OVERALL RANKLIST (for rank_list.txt)--------------------------#
rank_number=1
for student in rank_data:
    
    #ranklist by total marks (here logic of same total marks is not included)
    name = student["name"]
    totalmarks = student["totalmarks"]
    avg = student["avg"]
    grade = student["grade"]    
    line = f"{rank_number:8} | {name:<30} | Total_Marks: {totalmarks:<15} | Avg: {avg:<15} | Grade: {grade:<8}\n"
    rank_list_output.append(line)
    rank_number=rank_number+1
    
    #--------------REPORT CARD GENERATION [PDF FILE] [TXT FILE]
    generate_student_report_card(student, subjects, report_cards_dir_path)
    generate_student_report_card_pdf(student, subjects, pdf_reports_dir_path)

#-------------------------------------- ACCESSING ALL SUBJECTS   ----------------------------------- #
for i in range(len(subjects)):

    sub_name = subjects[i]
    subject_file_path = os.path.join(base_dir,"..","data",f"{sub_name}_rank_list_.txt")

    #----------------SORTING VIA SUBJECT MARKS(reverse) TO GET SUBJECT WISE RANK LIST------------------#
    rank_data.sort(key=lambda x:x["scores"][i] , reverse=True)

    sub_data_output=[]    #storing subject wise rank list
    sub_failed_output=[]  #storing subject wise failed students for probation from subject teacher

    total_sub_score = 0 #needed for class average per subject analytics(toughest and easiest subject)
    sub_pass_count = 0 #needed for pass rate analytics
    
    
    #------------------------------------------LOGIC OF SUBJECT WISE TOPPERS(multiple included)--------------------------#

    # store max score to append multiple toppers
    max_score = rank_data[0]["scores"][i]

    #appending max score of every subject as a list for a bar graph of top scores
    max_scores_per_subject.append(max_score)

    
    
    rank_number=1
    for student in rank_data:

        s_name = student["name"]
        s_score = student["scores"][i]

        #---------------------------------SUBJECT WISE TOPPERS LOGIC(multiple) FOR TOPPERS.TXT ---------------------#
        if s_score == max_score:
            subject_toppers.append(f"Subject: {sub_name:<30} | Topper: {s_name:<30} | Score: {s_score}\n")

        #---------------------------------SUBJECT WISE RANK LIST-----------------------------#
        s_grade = get_grade(s_score)
        line = f"{rank_number:<8} | {s_name:<30} | Subject: {sub_name:<39} |  Score: {s_score:<15} | Grade: {s_grade:<15}\n"
        sub_data_output.append(line)
        rank_number=rank_number+1
        
        total_sub_score = total_sub_score + s_score # for subject average we need total marks per subject

        # ------------------------------- SUBJECT WISE PASS AND FAIL COUNT FOR PASS RATE ANALYTICS----------------------@
        if s_score>=40:
            sub_pass_count = sub_pass_count + 1 

        #--------------------------------- APPENDING SUBJECT WISE FAILED STUDENTS.TXT------------------#
        if s_score<40 :
            line = f"{s_name:<30} | Subject : {sub_name:30} | Grade : {s_grade:<15} | Status : FAIL\n"
            sub_failed_output.append(line)
        
        
   #-------------------------------------------SUBJECT WISE ANALYITCS -------------------------------------------------------------#

   #[SUBJECT AVERAGE]   [SUBJECT AVERAGE CHART]
   #[PASS /FAIL COUNTS] [PASS RATE CHART]
   #[SUBJECT WISE FAILED STUDENTS.TXT]
   #[SUBJECT REPORT PDF TO SUBJECT PROFFESOR]

   # ------------- APPENDING SUBJECT AVERAGE AS EVERY STUDENT PER SUBJECT GOT ITERATED----------------#
   # ------------- TOTAL SUBJECT SCORE IS CALCULATED FROM ABOVE LOOP                  ---------------------------#
    sub_avg = (total_sub_score)/len(rank_data)
    line=f"Subject: {sub_name:<30} | Average: {sub_avg:.3f}\n"
    subject_average_output.append(line)
    subject_averages.append(sub_avg) #list of average of every subject for x axis of bar chart for subject toughness 


    #------------------- TRACKING HARDEST(MIN AVG) AND EASIEST(MAX AVG) SUBJECT FOR ANALYITCS---------------------#
    if sub_avg < min_avg:
        min_avg = sub_avg
        max_subject_difficulty = sub_name
    if sub_avg > max_avg:
        max_avg = sub_avg
        min_subject_difficulty = sub_name
    
    # --------------TRACKING PASS RATE(pass count / fail count) FOR SUBJECT WISE ANALYTICS ---------------------------#
    pass_rate = ((sub_pass_count)/len(rank_data))*100
    analytics_line = f"Subject: {sub_name:<30} | Passed: {sub_pass_count:<5} | Fail: {len(rank_data)-sub_pass_count:<5} | Pass Rate: {pass_rate:>6.2f}%\n"
    subject_analytics_output.append(analytics_line)

    # list of pass and fail counts of each subject via list
    pass_counts.append(sub_pass_count)
    fail_counts.append(len(rank_data) - sub_pass_count)


    # appending fooster line of class average at the end of subject wise rank list(sub_data_output)
    sub_data_output.append("-" * 35 + "\n")
    sub_data_output.append(f"CLASS AVERAGE: {sub_avg:.3f}\n") #fooster line at the end of subject wise rank list

    # ---------------------------SUBJECT WISE FAILED STUDENTS--------------------#  
    subject_failure_path = os.path.join(base_dir,"..","data",f"{sub_name}_failed_students_.txt")
    with open(subject_failure_path,"w") as f_sub:
        f_sub.writelines(sub_failed_output)
        

    # subject rank list in sub data output written into path of subject wise rank list.txt
    with open(subject_file_path,"w") as j:
        j.writelines(sub_data_output)
    
    #------------------SUBJECT TEACHER REPORT[PDF] CREATED FOR EACH SUBJECT ---------------#

    teacher_pdf_path = os.path.join(base_dir, "..", "data", f"{sub_name}_teacher_report.pdf")

    #accessing subject wise toppers from subject_toppers which have toppers for each subject
    current_sub_toppers = [t for t in subject_toppers if f"Subject: {sub_name}" in t]
    generate_subject_teacher_report(sub_name, sub_avg, current_sub_toppers, sub_failed_output, teacher_pdf_path)




# -----------------------------------------------------------FINAL ANALYTICS------------------------------------------------------#

#  FINAL ANALYTICS = SUBJECT WISE ANALYTICS + OVERALL ANALYTICS + GRADE DISTRIBUTION ANALYTICS
#  SUBJECT WISE ANALYTICS   :COUNT OF PASS,FAIL , PASSRATE 
#  OVERALL ANALYTICS        :OVERALL PASS FAIL COUNT AND PASS RATE
#  GRADE DISTRIBUTION       :GRADE COUNTS FOR A BROADER VIEW OF CLASS GRADES DISTRIBUTION AMONG STUDENTS


#----------------------------OVERALL ANALYTICS------------------------------#
overall_analytics = [
    "=========================================\n",
    "        CLASS ANALYTICS\n",
    "=========================================\n",
    f"Total Students: {len(rank_data)}\n",
    f"Overall Topper: {topper_names} ({max_total} Marks)\n",
    f"Hardest Subject: {max_subject_difficulty} (Avg: {min_avg:.2f})\n",
    f"Easiest Subject: {min_subject_difficulty} (Avg: {max_avg:.2f})\n",
    "-----------------------------------------\n",
    "SUBJECT-WISE DETAIL:\n"
] 

#---------------------------GRADE DISTRIBUTION-------------------------------#

grade_dist_lines = ["\n-----------------------------------------\n", "OVERALL GRADE DISTRIBUTION:\n"]
for g in ["AA", "AB", "BB", "BC", "CC", "CD", "DD"]:
    grade_dist_lines.append(f"Grade {g:<2}: {grade_counts[g]} students\n") # MAINTAINED A DICTIONARY FOR GRADE [KEY="AA" AND VALUE = COUNT OF AA(INT)] 

final_analytics = overall_analytics + subject_analytics_output + grade_dist_lines   


#----------------------------------------------------FINAL FILE WRITES-----------------------------------------------------------------------------#
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


# -------------FUNCTION CALLING OF GRADE VISUAL CHART --------------------#
generate_grade_chart(grade_counts , grade_chart_image_path)

#--------------FUNCTION CALLING OF SUBJECT AVERAGES CHART-----------------#
generate_subject_average_chart(subjects , subject_averages, average_chart_image_path)

#--------------FUNCTION CALLING PASS RATE CHART----------------------------#
generate_pass_rate_chart(subjects, pass_counts, fail_counts, pass_fail_count_chart_path)

#--------------FUNCTION CALLING OF MAX SCORE PER SUBJECT--------------------# 
generate_max_scores_per_subject_chart( subjects, max_scores_per_subject , max_score_per_subject_chart_path)

#--------------FUNCTION CALLING FOR GRADE PIE CHART-------------------------#
generate_grade_pie_chart(grade_counts, grade_pie_chart_path)

#--------------FUNCTION CALLING FOR HEAT MAP---------------------------------#
rank_data.sort(key=lambda x: x["totalmarks"], reverse=True)
heat_map_names=[]
heat_map_scores=[]

# resort by total marks again as in subject wise loop rank_data was sorted by subject wise marks and 
# currently rank_data is sorted by last subject's marks

for student in rank_data:
    s_name = student["name"]
    s_score_list = student["scores"]
    heat_map_names.append(s_name)
    heat_map_scores.append(s_score_list)

generate_heat_map_scores(heat_map_scores,heat_map_names,subjects,heat_map_scores_path)


#------------------------------FUNCTION CALLING FOR [ATTENDANCE]vs[TOTAL MARKS] SCATTER PLOT-----------------------------#
attendance_values=[] 
attendance_values = [student["attendance"] for student in rank_data]
total_marks_values = [student["totalmarks"] for student in rank_data]
generate_attendance_scatter_chart(attendance_values, total_marks_values, attendance_scatter_chart_path)


#----------------------------FUNCTION CALLING FOR FINAL REPORT GENERATION-----------------------------------------#


# storing path of all images to be included in final report 
all_images = {
    'heatmap': heat_map_scores_path,
    'grade_pie': grade_pie_chart_path,
    'grade_bar': grade_chart_image_path,
    'pass_fail': pass_fail_count_chart_path,
    'subject_avg': average_chart_image_path,
    'max_score': max_score_per_subject_chart_path,
    'attendance_scatter': attendance_scatter_chart_path
}
final_report_path = os.path.join(base_dir, "..", "data", "Final_Class_Report.pdf")
generate_final_report_pdf(final_report_path, all_images, analytics_path)



#---------------------------------STUDENT SEARCH FEATURE------------------------------------------#


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



#----------------------------------------------END------------------------------------------------------------#


