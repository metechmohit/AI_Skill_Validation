# Automated Skill Validation via AI Agents
This full-stack Flask application automates the initial technical screening of job applicants. It parses resumes, generates tailored skill assessments using AI, and automatically scores the responses, providing a streamlined workflow for hiring managers.

## Key Features
*AI-Powered Resume Parsing:* Extracts key skills directly from uploaded resumes (.pdf, .docx).

*Dynamic Assessments:* Generates a relevant, 15-20 question test with mixed formats (coding, MCQ, subjective) based on the candidate's unique skill set.

*Automated Scoring:* Uses OpenAI embeddings and cosine similarity for nuanced scoring of responses against model answers.

*HR Dashboard:* Provides a clean interface for hiring managers to review candidate scores, see detailed answers, and flag responses for manual review.

## Technical Approach
*Backend:* Python with Flask, using a modular structure for services, models, and utilities.

*AI & Scoring:* OpenAI API (GPT models) for skill extraction and assessment generation. Text embeddings are used for semantic scoring.

*Frontend:* Server-rendered HTML with Jinja2 templating, styled with standard CSS and enhanced with minimal vanilla JavaScript for UI interactivity.

*Data:* A simple JSON file-based system for data handling in this demonstration project.

Demo video link : https://drive.google.com/file/d/1AcrfP4tILh60fuNnV--_lczcCH00xx6t/view?usp=sharing
