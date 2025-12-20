from flask import Flask, render_template, request, jsonify
import copy
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

app = Flask(__name__)

# Original student data
students = [
    {'roll': 101, 'name': "Rohan", 'branch': "CSE", 'marks': (78, 67, 89)},
    {'roll': 102, 'name': "Riyaa", 'branch': "CSE", 'marks': (88, 91, 76)},
    {'roll': 103, 'name': "Suman", 'branch': "ECE", 'marks': (92, 81, 74)},
    {'roll': 104, 'name': "Priya", 'branch': "EEE", 'marks': (65, 69, 72)},
    {'roll': 105, 'name': "Kunal", 'branch': "CSE", 'marks': (91, 73, 84)},
    {'roll': 106, 'name': "Meera", 'branch': "ME", 'marks': (58, 82, 55)},
    {'roll': 107, 'name': "Ameet", 'branch': "CSE", 'marks': (78, 67, 89)},
    {'roll': 108, 'name': "Diyaa", 'branch': "EEE", 'marks': (85, 81, 76)},
    {'roll': 109, 'name': "Rohan", 'branch': "ECE", 'marks': (37, 87, 70)},
    {'roll': 110, 'name': "Sriya", 'branch': "EEE", 'marks': (65, 66, 72)},
    {'roll': 111, 'name': "Kusal", 'branch': "ME", 'marks': (88, 73, 84)},
    {'roll': 112, 'name': "Manoj", 'branch': "ME", 'marks': (78, 73, 65)}
]

def calculate_grade(percentage):
    """Calculate grade based on percentage"""
    if percentage >= 90:
        return 'O'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'P'
    else:
        return 'F'

def augment_data(student_list):
    """Calculate total, percentage, and grade for each student"""
    augmented_data = []
    for student in student_list:
        total_marks = sum(student['marks'])
        percentage = (total_marks / 300) * 100
        grade = calculate_grade(percentage)
        augmented_data.append({
            'total_marks': total_marks,
            'percentage': round(percentage, 2),
            'grade': grade
        })
    return augmented_data

def get_combined_data():
    """Combine student data with calculated metrics"""
    augmented = augment_data(students)
    combined = []
    for i, student in enumerate(students):
        combined.append({
            'roll': student['roll'],
            'name': student['name'],
            'branch': student['branch'],
            'marks': student['marks'],
            'total_marks': augmented[i]['total_marks'],
            'percentage': augmented[i]['percentage'],
            'grade': augmented[i]['grade']
        })
    return combined

def generate_graph_base64(fig):
    """Convert matplotlib figure to base64 string"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return img_base64

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/all-students')
def all_students():
    """Get all students with calculated data"""
    combined_data = get_combined_data()
    return jsonify(combined_data)

@app.route('/api/student/<int:roll>')
def student_by_roll(roll):
    """Get student details by roll number"""
    combined_data = get_combined_data()
    for student in combined_data:
        if student['roll'] == roll:
            return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404

@app.route('/api/students-by-grade/<grade>')
def students_by_grade(grade):
    """Get all students with a specific grade"""
    combined_data = get_combined_data()
    filtered = [s for s in combined_data if s['grade'] == grade.upper()]
    return jsonify(filtered)

@app.route('/api/branches')
def unique_branches():
    """Get unique branches and count"""
    branches = set(s['branch'] for s in students)
    branch_count = {}
    for branch in branches:
        count = sum(1 for s in students if s['branch'] == branch)
        branch_count[branch] = count
    return jsonify({
        'branches': list(branches),
        'branch_count': branch_count
    })

@app.route('/api/branch-wise-students')
def branch_wise_students():
    """Get branch-wise roll numbers"""
    branches = set(s['branch'] for s in students)
    branch_wise = {}
    for branch in branches:
        roll_nums = [s['roll'] for s in students if s['branch'] == branch]
        branch_wise[branch] = roll_nums
    return jsonify(branch_wise)

@app.route('/api/toppers')
def toppers():
    """Get overall and branch-wise toppers"""
    combined_data = get_combined_data()
    
    # Overall topper
    overall_topper = max(combined_data, key=lambda x: x['percentage'])
    
    # Branch-wise toppers
    branches = set(s['branch'] for s in students)
    branch_toppers = {}
    for branch in branches:
        branch_students = [s for s in combined_data if s['branch'] == branch]
        if branch_students:
            topper = max(branch_students, key=lambda x: x['percentage'])
            branch_toppers[branch] = topper
    
    return jsonify({
        'overall_topper': overall_topper,
        'branch_toppers': branch_toppers
    })

@app.route('/api/top-students/<int:count>')
def top_students(count):
    """Get top N students by percentage"""
    combined_data = get_combined_data()
    # Sort by percentage in descending order
    sorted_students = sorted(combined_data, key=lambda x: x['percentage'], reverse=True)
    return jsonify(sorted_students[:count])

@app.route('/api/students-above-percentage/<float:percentage>')
def students_above_percentage(percentage):
    """Get students scoring above a certain percentage"""
    combined_data = get_combined_data()
    filtered = [s for s in combined_data if s['percentage'] >= percentage]
    return jsonify(filtered)

@app.route('/api/statistics')
def statistics():
    """Get overall statistics"""
    combined_data = get_combined_data()
    
    percentages = [s['percentage'] for s in combined_data]
    avg_percentage = sum(percentages) / len(percentages)
    
    grades_count = {}
    for student in combined_data:
        grade = student['grade']
        grades_count[grade] = grades_count.get(grade, 0) + 1
    
    return jsonify({
        'total_students': len(students),
        'average_percentage': round(avg_percentage, 2),
        'highest_percentage': max(percentages),
        'lowest_percentage': min(percentages),
        'grades_distribution': grades_count
    })

@app.route('/api/report')
def generate_report():
    """Generate complete institute report"""
    combined_data = get_combined_data()
    branches = set(s['branch'] for s in students)
    
    # Overall topper
    overall_topper = max(combined_data, key=lambda x: x['percentage'])
    
    # Branch-wise toppers
    branch_toppers = {}
    for branch in branches:
        branch_students = [s for s in combined_data if s['branch'] == branch]
        if branch_students:
            topper = max(branch_students, key=lambda x: x['percentage'])
            branch_toppers[branch] = topper['name']
    
    report = {
        "total_students": len(students),
        "branches": list(branches),
        "toppers": {
            "overall": overall_topper['name'],
            **{branch: name for branch, name in branch_toppers.items()}
        }
    }
    
    return jsonify(report)

@app.route('/api/generate-graphs')
def generate_graphs():
    """Generate all graphs using matplotlib and pandas"""
    combined_data = get_combined_data()
    df = pd.DataFrame(combined_data)
    
    graphs = {}
    
    # 1. Grade Distribution (Pie Chart)
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    grade_counts = df['grade'].value_counts()
    colors = ['#28a745', '#17a2b8', '#007bff', '#ffc107', '#fd7e14', '#dc3545']
    ax1.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=colors[:len(grade_counts)])
    ax1.set_title('Grade Distribution', fontsize=16, fontweight='bold')
    graphs['grade_distribution'] = generate_graph_base64(fig1)
    
    # 2. Branch-wise Average Performance (Bar Chart)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    branch_avg = df.groupby('branch')['percentage'].mean().sort_values(ascending=False)
    bars = ax2.bar(branch_avg.index, branch_avg.values, color='#667eea', edgecolor='black')
    ax2.set_xlabel('Branch', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Average Percentage', fontsize=12, fontweight='bold')
    ax2.set_title('Branch-wise Average Performance', fontsize=16, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    graphs['branch_performance'] = generate_graph_base64(fig2)
    
    # 3. Percentage Distribution (Histogram)
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.hist(df['percentage'], bins=10, color='#764ba2', edgecolor='black', alpha=0.7)
    ax3.set_xlabel('Percentage', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
    ax3.set_title('Percentage Distribution', fontsize=16, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    graphs['percentage_histogram'] = generate_graph_base64(fig3)
    
    # 4. Top 10 Students (Horizontal Bar Chart)
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    top_10 = df.nlargest(10, 'percentage')
    colors_top10 = plt.cm.viridis(range(10))
    bars = ax4.barh(top_10['name'], top_10['percentage'], color=colors_top10, edgecolor='black')
    ax4.set_xlabel('Percentage', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Student Name', fontsize=12, fontweight='bold')
    ax4.set_title('Top 10 Students Performance', fontsize=16, fontweight='bold')
    ax4.invert_yaxis()
    ax4.grid(axis='x', alpha=0.3)
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax4.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%', ha='left', va='center', fontweight='bold')
    graphs['top_10_chart'] = generate_graph_base64(fig4)
    
    # 5. Subject-wise Average Marks (Bar Chart)
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    subject_1 = [s['marks'][0] for s in combined_data]
    subject_2 = [s['marks'][1] for s in combined_data]
    subject_3 = [s['marks'][2] for s in combined_data]
    
    subjects = ['Subject 1', 'Subject 2', 'Subject 3']
    averages = [sum(subject_1)/len(subject_1), sum(subject_2)/len(subject_2), sum(subject_3)/len(subject_3)]
    
    bars = ax5.bar(subjects, averages, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], edgecolor='black')
    ax5.set_ylabel('Average Marks', fontsize=12, fontweight='bold')
    ax5.set_title('Subject-wise Average Marks', fontsize=16, fontweight='bold')
    ax5.set_ylim(0, 100)
    ax5.grid(axis='y', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
    graphs['subject_analysis'] = generate_graph_base64(fig5)
    
    return jsonify(graphs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)