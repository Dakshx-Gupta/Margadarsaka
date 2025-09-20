"""
PDF Roadmap Generator for Margadarsaka
Creates visual career roadmaps and learning paths
"""

import io
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
import numpy as np

from .models import UserProfile, CareerPath, PsychologicalTest, LearningResource


class RoadmapVisualizer:
    """Create visual career roadmaps and learning paths"""

    def __init__(self):
        self.colors = {
            "primary": "#2E86AB",
            "secondary": "#A23B72",
            "accent": "#F18F01",
            "success": "#C73E1D",
            "background": "#F5F5F5",
            "text": "#2D3748",
        }

        # Set up matplotlib style
        plt.style.use("seaborn-v0_8")
        sns.set_palette("husl")

    def create_career_roadmap_pdf(
        self,
        user_profile: UserProfile,
        career_paths: List[CareerPath],
        psychological_results: Optional[PsychologicalTest] = None,
        output_path: str = "career_roadmap.pdf",
    ) -> str:
        """Create comprehensive career roadmap PDF"""

        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []

        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor(self.colors["primary"]),
        )

        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading1"],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor(self.colors["secondary"]),
        )

        # Title page
        story.append(Paragraph("🎯 Career Roadmap", title_style))
        story.append(
            Paragraph(f"Personalized for {user_profile.name}", styles["Normal"])
        )
        story.append(
            Paragraph(
                f"Generated on {datetime.now().strftime('%B %d, %Y')}", styles["Normal"]
            )
        )
        story.append(Spacer(1, 0.5 * inch))

        # User profile summary
        story.append(Paragraph("👤 Profile Summary", heading_style))
        profile_data = [
            ["Name", user_profile.name],
            ["Age", str(user_profile.age)],
            ["Education Level", user_profile.education_level],
            ["Current Field", user_profile.field_of_study],
            [
                "Language Preference",
                user_profile.language_preference.value
                if user_profile.language_preference
                else "English",
            ],
            [
                "Family Background",
                user_profile.family_background.value
                if user_profile.family_background
                else "Not specified",
            ],
        ]

        profile_table = Table(profile_data, colWidths=[2 * inch, 3 * inch])
        profile_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor(self.colors["primary"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(profile_table)
        story.append(Spacer(1, 0.3 * inch))

        # Psychological assessment results
        if psychological_results:
            story.append(Paragraph("🧠 Psychological Assessment", heading_style))

            # RIASEC results chart
            riasec_chart = self._create_riasec_chart(
                psychological_results.riasec_scores
            )
            story.append(riasec_chart)
            story.append(Spacer(1, 0.2 * inch))

            # Mental skills radar chart
            mental_skills_chart = self._create_mental_skills_chart(
                psychological_results.mental_skills_scores
            )
            story.append(mental_skills_chart)
            story.append(Spacer(1, 0.3 * inch))

        story.append(PageBreak())

        # Career paths analysis
        story.append(Paragraph("🚀 Recommended Career Paths", heading_style))

        for i, career_path in enumerate(career_paths[:3], 1):  # Top 3 paths
            story.append(Paragraph(f"{i}. {career_path.title}", styles["Heading2"]))
            story.append(
                Paragraph(
                    f"Match Score: {career_path.match_score:.1f}%", styles["Normal"]
                )
            )
            story.append(Paragraph(career_path.description, styles["Normal"]))

            # Skills required
            if career_path.required_skills:
                story.append(Paragraph("Required Skills:", styles["Heading3"]))
                skills_text = " • ".join(career_path.required_skills)
                story.append(Paragraph(skills_text, styles["Normal"]))

            # Salary information
            if career_path.salary_range_inr:
                story.append(
                    Paragraph(
                        f"Salary Range: ₹{career_path.salary_range_inr}",
                        styles["Normal"],
                    )
                )

            story.append(Spacer(1, 0.2 * inch))

        story.append(PageBreak())

        # Learning roadmap timeline
        story.append(Paragraph("📚 Learning Roadmap", heading_style))

        # Create timeline visualization
        timeline_image = self._create_learning_timeline(
            career_paths[0] if career_paths else None
        )
        story.append(timeline_image)
        story.append(Spacer(1, 0.3 * inch))

        # Skills development matrix
        story.append(Paragraph("💪 Skills Development Matrix", heading_style))
        skills_matrix = self._create_skills_matrix(career_paths)
        story.append(skills_matrix)

        story.append(PageBreak())

        # Action plan
        story.append(Paragraph("🎯 30-60-90 Day Action Plan", heading_style))
        action_plan = self._create_action_plan(
            career_paths[0] if career_paths else None, user_profile
        )

        for period, actions in action_plan.items():
            story.append(Paragraph(f"{period} Days", styles["Heading2"]))
            for action in actions:
                story.append(Paragraph(f"• {action}", styles["Normal"]))
            story.append(Spacer(1, 0.2 * inch))

        # Build PDF
        doc.build(story)

        return output_path

    def _create_riasec_chart(self, riasec_scores: Dict[str, float]) -> Image:
        """Create RIASEC personality type chart"""
        fig, ax = plt.subplots(figsize=(8, 6))

        categories = list(riasec_scores.keys())
        scores = list(riasec_scores.values())

        # Create bar chart
        bars = ax.bar(
            categories, scores, color=sns.color_palette("husl", len(categories))
        )

        # Customize chart
        ax.set_title("RIASEC Personality Profile", fontsize=16, fontweight="bold")
        ax.set_ylabel("Score", fontsize=12)
        ax.set_ylim(0, 100)

        # Add value labels on bars
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 1,
                f"{score:.1f}",
                ha="center",
                va="bottom",
            )

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
        buffer.seek(0)
        plt.close()

        # Create ReportLab Image
        img = Image(buffer, width=6 * inch, height=4 * inch)
        return img

    def _create_mental_skills_chart(self, mental_skills: Dict[str, float]) -> Image:
        """Create mental skills radar chart"""
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection="polar"))

        categories = list(mental_skills.keys())
        values = list(mental_skills.values())

        # Add first value at end to close the circle
        values += values[:1]

        # Calculate angles for each category
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        # Plot
        ax.plot(angles, values, "o-", linewidth=2, color=self.colors["primary"])
        ax.fill(angles, values, alpha=0.25, color=self.colors["primary"])

        # Customize
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 100)
        ax.set_title("Mental Skills Profile", size=16, fontweight="bold", pad=20)
        ax.grid(True)

        plt.tight_layout()

        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
        buffer.seek(0)
        plt.close()

        img = Image(buffer, width=5 * inch, height=5 * inch)
        return img

    def _create_learning_timeline(self, career_path: Optional[CareerPath]) -> Image:
        """Create learning timeline visualization"""
        fig, ax = plt.subplots(figsize=(12, 6))

        # Sample timeline data (in real implementation, this would come from career_path)
        milestones = [
            (
                "Month 1-2",
                "Foundation Skills",
                ["Basic Programming", "Problem Solving"],
            ),
            ("Month 3-4", "Intermediate Skills", ["Data Structures", "Algorithms"]),
            ("Month 5-6", "Advanced Skills", ["System Design", "Projects"]),
            ("Month 7-8", "Specialization", ["Domain Knowledge", "Industry Skills"]),
            ("Month 9-12", "Professional Skills", ["Communication", "Leadership"]),
        ]

        # Create timeline
        y_pos = 0
        colors_list = sns.color_palette("husl", len(milestones))

        for i, (period, phase, skills) in enumerate(milestones):
            # Draw timeline bar
            rect = patches.Rectangle(
                (i, y_pos), 0.8, 0.8, facecolor=colors_list[i], alpha=0.7
            )
            ax.add_patch(rect)

            # Add period text
            ax.text(
                i + 0.4,
                y_pos + 1.2,
                period,
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=10,
            )

            # Add phase text
            ax.text(
                i + 0.4,
                y_pos + 0.4,
                phase,
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
            )

            # Add skills text
            skills_text = "\n".join(skills)
            ax.text(
                i + 0.4, y_pos - 0.5, skills_text, ha="center", va="top", fontsize=8
            )

        # Customize chart
        ax.set_xlim(-0.5, len(milestones) - 0.5)
        ax.set_ylim(-2, 2)
        ax.set_title(
            "Learning Timeline - 12 Month Plan", fontsize=16, fontweight="bold"
        )
        ax.axis("off")

        plt.tight_layout()

        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
        buffer.seek(0)
        plt.close()

        img = Image(buffer, width=10 * inch, height=4 * inch)
        return img

    def _create_skills_matrix(self, career_paths: List[CareerPath]) -> Table:
        """Create skills development matrix table"""
        if not career_paths:
            return Table([["No career paths available"]])

        # Collect all unique skills
        all_skills = set()
        for path in career_paths[:3]:  # Top 3 paths
            if path.required_skills:
                all_skills.update(path.required_skills)

        all_skills = sorted(list(all_skills))

        # Create matrix data
        matrix_data = [
            ["Skill"] + [f"Path {i + 1}" for i in range(min(3, len(career_paths)))]
        ]

        for skill in all_skills[:10]:  # Limit to 10 skills
            row = [skill]
            for path in career_paths[:3]:
                if path.required_skills and skill in path.required_skills:
                    row.append("✓")
                else:
                    row.append("-")
            matrix_data.append(row)

        # Create table
        table = Table(
            matrix_data, colWidths=[2.5 * inch] + [1 * inch] * min(3, len(career_paths))
        )
        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor(self.colors["primary"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                ]
            )
        )

        return table

    def _create_action_plan(
        self, career_path: Optional[CareerPath], user_profile: UserProfile
    ) -> Dict[str, List[str]]:
        """Create 30-60-90 day action plan"""

        base_plan = {
            "30": [
                "Complete career assessment and identify strengths",
                "Research target industry and companies",
                "Update and optimize resume/portfolio",
                "Start learning fundamental skills",
                "Join relevant online communities",
            ],
            "60": [
                "Complete 2-3 small projects or assignments",
                "Network with professionals in target field",
                "Apply for internships or entry-level positions",
                "Attend industry webinars or workshops",
                "Seek mentorship opportunities",
            ],
            "90": [
                "Complete major project demonstrating skills",
                "Prepare for technical interviews",
                "Build professional online presence",
                "Apply to target companies",
                "Evaluate progress and adjust strategy",
            ],
        }

        # Customize based on career path
        if career_path and career_path.required_skills:
            primary_skill = (
                career_path.required_skills[0]
                if career_path.required_skills
                else "programming"
            )
            base_plan["30"].append(f"Focus on learning {primary_skill}")
            base_plan["60"].append(f"Build project showcasing {primary_skill}")

        # Customize for Indian context
        if user_profile.family_background:
            base_plan["30"].append("Discuss career plans with family")
            base_plan["60"].append("Research local opportunities and market")

        return base_plan

    def create_skills_visualization(
        self,
        current_skills: List[str],
        target_skills: List[str],
        output_path: str = "skills_gap.png",
    ) -> str:
        """Create skills gap visualization"""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Current skills pie chart
        if current_skills:
            skill_categories = self._categorize_skills(current_skills)
            ax1.pie(
                skill_categories.values(),
                labels=skill_categories.keys(),
                autopct="%1.1f%%",
                startangle=90,
            )
            ax1.set_title("Current Skills Distribution")

        # Target skills bar chart
        if target_skills:
            skill_levels = [
                np.random.randint(30, 90) for _ in target_skills
            ]  # Mock proficiency
            ax2.barh(
                target_skills,
                skill_levels,
                color=sns.color_palette("viridis", len(target_skills)),
            )
            ax2.set_xlabel("Proficiency Level (%)")
            ax2.set_title("Target Skills to Develop")
            ax2.set_xlim(0, 100)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return output_path

    def _categorize_skills(self, skills: List[str]) -> Dict[str, int]:
        """Categorize skills into technical/soft/domain categories"""
        categories = {"Technical": 0, "Soft Skills": 0, "Domain": 0}

        technical_keywords = ["programming", "python", "java", "sql", "git", "api"]
        soft_keywords = ["communication", "leadership", "teamwork", "problem solving"]

        for skill in skills:
            skill_lower = skill.lower()
            if any(keyword in skill_lower for keyword in technical_keywords):
                categories["Technical"] += 1
            elif any(keyword in skill_lower for keyword in soft_keywords):
                categories["Soft Skills"] += 1
            else:
                categories["Domain"] += 1

        return categories


class CareerReportGenerator:
    """Generate comprehensive career assessment reports"""

    def __init__(self):
        self.visualizer = RoadmapVisualizer()

    def generate_comprehensive_report(
        self,
        user_profile: UserProfile,
        career_paths: List[CareerPath],
        psychological_results: Optional[PsychologicalTest] = None,
        ats_analysis: Optional[Dict[str, Any]] = None,
        output_dir: str = "./reports",
    ) -> Dict[str, str]:
        """Generate all career assessment reports"""

        import os

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{user_profile.name.replace(' ', '_')}_{timestamp}"

        generated_files = {}

        try:
            # 1. Career roadmap PDF
            roadmap_path = os.path.join(output_dir, f"{base_name}_roadmap.pdf")
            self.visualizer.create_career_roadmap_pdf(
                user_profile, career_paths, psychological_results, roadmap_path
            )
            generated_files["roadmap"] = roadmap_path

            # 2. Skills gap visualization
            if career_paths:
                current_skills = (
                    user_profile.skills if hasattr(user_profile, "skills") else []
                )
                target_skills = (
                    career_paths[0].required_skills
                    if career_paths[0].required_skills
                    else []
                )

                skills_path = os.path.join(output_dir, f"{base_name}_skills_gap.png")
                self.visualizer.create_skills_visualization(
                    current_skills, target_skills, skills_path
                )
                generated_files["skills_visualization"] = skills_path

            # 3. Summary report
            summary_path = os.path.join(output_dir, f"{base_name}_summary.txt")
            self._generate_text_summary(
                user_profile, career_paths, psychological_results, summary_path
            )
            generated_files["summary"] = summary_path

        except Exception as e:
            print(f"Error generating reports: {str(e)}")

        return generated_files

    def _generate_text_summary(
        self,
        user_profile: UserProfile,
        career_paths: List[CareerPath],
        psychological_results: Optional[PsychologicalTest],
        output_path: str,
    ) -> None:
        """Generate text summary of assessment"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("CAREER ASSESSMENT SUMMARY\n")
            f.write("=" * 50 + "\n\n")

            f.write(f"Name: {user_profile.name}\n")
            f.write(f"Age: {user_profile.age}\n")
            f.write(f"Education: {user_profile.education_level}\n")
            f.write(f"Field: {user_profile.field_of_study}\n\n")

            if psychological_results:
                f.write("PSYCHOLOGICAL PROFILE:\n")
                f.write("-" * 20 + "\n")
                if psychological_results.riasec_scores:
                    dominant_type = max(
                        psychological_results.riasec_scores.items(), key=lambda x: x[1]
                    )
                    f.write(
                        f"Dominant RIASEC Type: {dominant_type[0]} ({dominant_type[1]:.1f}%)\n"
                    )

                if psychological_results.mental_skills_scores:
                    top_skill = max(
                        psychological_results.mental_skills_scores.items(),
                        key=lambda x: x[1],
                    )
                    f.write(f"Top Mental Skill: {top_skill[0]} ({top_skill[1]:.1f}%)\n")
                f.write("\n")

            f.write("RECOMMENDED CAREER PATHS:\n")
            f.write("-" * 25 + "\n")
            for i, path in enumerate(career_paths[:3], 1):
                f.write(f"{i}. {path.title} (Match: {path.match_score:.1f}%)\n")
                f.write(f"   {path.description}\n\n")

            f.write("KEY RECOMMENDATIONS:\n")
            f.write("-" * 18 + "\n")
            f.write("• Focus on developing technical skills\n")
            f.write("• Build a strong portfolio with projects\n")
            f.write("• Network with professionals in target field\n")
            f.write("• Consider internships or entry-level positions\n")
            f.write("• Stay updated with industry trends\n")
