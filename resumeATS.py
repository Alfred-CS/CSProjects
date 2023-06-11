import tkinter as tk
from tkinter import scrolledtext
import pandas as pd

def analyze_resume():
    job_posting_text = job_posting_textarea.get("1.0", tk.END)
    resume_text = resume_textarea.get("1.0", tk.END)

    # Step 2: Remove punctuation from job posting
    job_posting_list = job_posting_text.split()
    clean_job_posting = [word.replace('•', "").replace(",", "").replace("""""", "").replace("-", "").replace("'", "")
                         .replace("''", "").replace(":", "").replace(";", "").replace("*", "").replace("!", "")
                         .replace("&", "").replace("/n", "").replace("/", "").replace("?", "").replace("(", "")
                         .replace(")", "") for line in job_posting_list for word in line.lower().split()]

    job_count = dict()
    for i in clean_job_posting:
        job_count[i] = job_count.get(i, 0) + 1

    # Step 3: Remove common filler words in job posting
    common_job_words = ['a', 'ability', 'about', 'added', 'against', 'an', 'and', 'any', 'are', 'as', 'assist',
                        'assisting', 'at', 'be', 'both', 'but', 'by', 'can', 'demonstrate', 'demonstrated', 'duties',
                        'employee', 'every', 'existing', 'experience', 'following', 'for', 'from', 'gpa', 'have', 'in',
                        'including', 'identify', 'into', 'is', 'it', 'make', 'members', 'more', 'must', 'not', 'obtain',
                        'of', 'on', 'opportunity', 'or', 'other', 'our', 'preferred', 'qualifications', 'reach',
                        'require', 'required', 'skill', 'skills', 'strong', 'such', 'support', 'supporting', 'that',
                        'the', 'their', 'this', 'to', 'upon', 'us', 'use', 'using', 'we', 'will', 'with', 'work',
                        'working', 'you', 'your']

    for key in list(job_count.keys()):
        if key in common_job_words:
            del job_count[key]

    # Step 4: Show top keywords in the job posting and count their frequency
    job_keywords_count = sorted(job_count.items(), key=lambda x: x[1], reverse=True)

    # Step 5: Copy your resume below within the triple quotes
    resume_list = resume_text.split()  # Creates a list of words in your resume

    clean_resume = [  # Remove punctuation from resume
        word.replace(",", "")
            .replace("""""", "")
            .replace("-", "")
            .replace("'", "")
            .replace("''", "")
            .replace(":", "")
            .replace(";", "")
            .replace("*", "")
            .replace("!", "")
            .replace("&", "")
            .replace("/n", "")
            .replace("/", "")
            .replace("?", "")
            .replace("(", "")
            .replace(")", "")
            .replace("•", "")
        for line in resume_list for word in line.lower().split()]

    resume_count = dict()
    for i in clean_resume:
        resume_count[i] = resume_count.get(i, 0) + 1

    # Step 6: Remove common filler words in your resume
    common_resume_words = [
        '2018', '2019', '202']

    for key in list(resume_count.keys()):
        if key in common_resume_words:
            del resume_count[key]

    # Step 7: Show top keywords in your resume and count their frequency
    resume_keywords_count = sorted(resume_count.items(), key=lambda x: x[1], reverse=True)

    # Step 8: Calculate match rate
    total_keywords = len(job_keywords_count)
    matched_keywords = sum(1 for keyword, _ in job_keywords_count if keyword in resume_count)

    match_rate = (matched_keywords / total_keywords) * 100

    # Step 9: Identify key words in job posting that are not in your resume
    missing = {k: v for k, v in job_count.items() if k not in resume_count}
    missing_keywords = sorted(missing.items(), key=lambda x: x[1], reverse=True)

    # Create a pandas DataFrame for the results
    results = pd.DataFrame(columns=["Job Posting Keywords", "Count"])
    results = pd.concat([results, pd.DataFrame(job_keywords_count, columns=["Job Posting Keywords", "Count"])])
    results = pd.concat([results, pd.DataFrame([["", ""]], columns=["Job Posting Keywords", "Count"])])
    results = pd.concat([results, pd.DataFrame([["Resume Keywords", "Count"]], columns=["Job Posting Keywords", "Count"])])
    results = pd.concat([results, pd.DataFrame(resume_keywords_count, columns=["Job Posting Keywords", "Count"])])
    results = pd.concat([results, pd.DataFrame([["", ""]], columns=["Job Posting Keywords", "Count"])])
    results = pd.concat([results, pd.DataFrame([["Match Rate", f"{match_rate:.2f}%"]], columns=["Job Posting Keywords", "Count"])])
    results = pd.concat([results, pd.DataFrame([["", ""]], columns=["Job Posting Keywords", "Count"])])
    results = pd.concat([results, pd.DataFrame([["Missing Keywords in Resume", "Count"]], columns=["Job Posting Keywords", "Count"])])
    results = pd.concat([results, pd.DataFrame(missing_keywords, columns=["Job Posting Keywords", "Count"])])

    # Export the results to Excel
    results.to_excel("resume_analysis.xlsx", index=False)

    print("Results exported to resume_analysis.xlsx")

root = tk.Tk()
root.title("Job Scan Replica")
root.geometry("800x600")

job_posting_label = tk.Label(root, text="Job Posting")
job_posting_label.pack()

job_posting_textarea = scrolledtext.ScrolledText(root, width=80, height=10)
job_posting_textarea.pack()

resume_label = tk.Label(root, text="Resume")
resume_label.pack()

resume_textarea = scrolledtext.ScrolledText(root, width=80, height=10)
resume_textarea.pack()

analyze_button = tk.Button(root, text="Analyze Resume", command=analyze_resume)
analyze_button.pack()

root.mainloop()
