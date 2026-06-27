import os
from openai import OpenAI

BASE_CV_SKILLS = {
    "hydrology": "Applied hydrological modelling and catchment-scale analysis to assess rainfall-runoff processes, flood risk, drought impacts and water resources management.",
    "flood risk": "Conducted flood and drought assessment using hydrological datasets, GIS analysis and model-based interpretation to support risk-informed decision-making.",
    "catchment": "Worked on catchment management, soil erosion control, water quality protection and nature-based solutions for sustainable watershed planning.",
    "gis": "Used GIS, remote sensing and environmental data analysis tools including ArcGIS, QGIS, R and Python.",
    "stakeholder": "Communicated complex technical findings through reports, presentations, training and stakeholder engagement with academic, government and community partners."
}

class AIDrafter:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def rule_based_draft(self, job):
        text = f"{job.title} {job.description}".lower()
        bullets = []
        for key, bullet in BASE_CV_SKILLS.items():
            if key in text:
                bullets.append(f"• {bullet}")
        if not bullets:
            bullets.append("• Strong background in hydrology, water resources management, environmental modelling and climate-resilient catchment management.")
        paragraph = (
            f"I am interested in the {job.title} role at {job.employer} because it aligns closely with my background in hydrology, "
            f"water resources management, flood and drought risk, catchment management, GIS, remote sensing and climate resilience. "
            f"My experience in hydrological modelling, environmental data analysis, technical reporting and stakeholder engagement would enable me to contribute effectively to this role."
        )
        return {"job_id": job.id, "title": job.title, "employer": job.employer, "cv_bullets": "\n".join(bullets), "cover_letter_paragraph": paragraph}

    def ai_draft(self, job):
        if not self.client:
            return self.rule_based_draft(job)
        prompt = f"""
Create concise UK-style application draft content for this hydrology-related job.
Return two sections only:
1) 5 tailored CV bullet points
2) One cover-letter paragraph
Human review required before use.

Job title: {job.title}
Employer: {job.employer}
Location: {job.location}
Description: {job.description[:4000]}
Candidate: PhD Hydrology and Water Resources Management; 7+ years hydrological modelling, flood/drought, catchment management, SWAT+, HEC-HMS, GIS, R, Python, stakeholder engagement, teaching/research.
"""
        response = self.client.responses.create(model="gpt-4.1-mini", input=prompt)
        text = response.output_text
        return {"job_id": job.id, "title": job.title, "employer": job.employer, "cv_bullets": text, "cover_letter_paragraph": "See AI draft above"}

    def generate_for_jobs(self, jobs):
        return [self.ai_draft(j) for j in jobs if j.score >= 70]
