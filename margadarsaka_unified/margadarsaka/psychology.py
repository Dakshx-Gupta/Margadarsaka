"""
Psychological testing framework for Margadarsaka
Includes RIASEC model, personality tests, and mental skill assessments
"""

from typing import Dict, List, Any, Tuple
import json
from .models import (
    PsychologicalTest,
    TestResponse,
    RIASECCode,
    MentalSkill,
    UserProfile,
)
from datetime import datetime


class RIASECAssessment:
    """RIASEC (Holland's Career Codes) Assessment Implementation"""

    def __init__(self):
        self.questions = self._load_riasec_questions()

    def _load_riasec_questions(self) -> List[Dict[str, Any]]:
        """Load RIASEC assessment questions"""
        return [
            {
                "id": "R1",
                "question": "I enjoy working with tools and machinery",
                "question_hindi": "मुझे औजारों और मशीनों के साथ काम करना पसंद है",
                "category": "realistic",
                "weight": 1.0,
            },
            {
                "id": "R2",
                "question": "I like to build things with my hands",
                "question_hindi": "मुझे अपने हाथों से चीजें बनाना पसंद है",
                "category": "realistic",
                "weight": 1.0,
            },
            {
                "id": "R3",
                "question": "I prefer outdoor activities over indoor ones",
                "question_hindi": "मुझे घर के अंदर की बजाय बाहरी गतिविधियां पसंद हैं",
                "category": "realistic",
                "weight": 0.8,
            },
            {
                "id": "I1",
                "question": "I enjoy solving complex mathematical problems",
                "question_hindi": "मुझे जटिल गणितीय समस्याओं को हल करना पसंद है",
                "category": "investigative",
                "weight": 1.0,
            },
            {
                "id": "I2",
                "question": "I like to analyze data and find patterns",
                "question_hindi": "मुझे डेटा का विश्लेषण करना और पैटर्न खोजना पसंद है",
                "category": "investigative",
                "weight": 1.0,
            },
            {
                "id": "I3",
                "question": "I enjoy conducting experiments and research",
                "question_hindi": "मुझे प्रयोग और अनुसंधान करना पसंद है",
                "category": "investigative",
                "weight": 1.0,
            },
            {
                "id": "A1",
                "question": "I enjoy creative writing and storytelling",
                "question_hindi": "मुझे रचनात्मक लेखन और कहानी सुनाना पसंद है",
                "category": "artistic",
                "weight": 1.0,
            },
            {
                "id": "A2",
                "question": "I like to express myself through art, music, or dance",
                "question_hindi": "मुझे कला, संगीत या नृत्य के माध्यम से खुद को व्यक्त करना पसंद है",
                "category": "artistic",
                "weight": 1.0,
            },
            {
                "id": "A3",
                "question": "I appreciate beauty in design and aesthetics",
                "question_hindi": "मुझे डिजाइन और सौंदर्यशास्त्र में सुंदरता की सराहना करना पसंद है",
                "category": "artistic",
                "weight": 0.8,
            },
            {
                "id": "S1",
                "question": "I enjoy helping others solve their problems",
                "question_hindi": "मुझे दूसरों की समस्याओं को हल करने में मदद करना पसंद है",
                "category": "social",
                "weight": 1.0,
            },
            {
                "id": "S2",
                "question": "I like teaching and mentoring others",
                "question_hindi": "मुझे दूसरों को पढ़ाना और मार्गदर्शन करना पसंद है",
                "category": "social",
                "weight": 1.0,
            },
            {
                "id": "S3",
                "question": "I am good at understanding people's emotions",
                "question_hindi": "मैं लोगों की भावनाओं को समझने में अच्छा हूँ",
                "category": "social",
                "weight": 0.9,
            },
            {
                "id": "E1",
                "question": "I enjoy leading teams and projects",
                "question_hindi": "मुझे टीमों और परियोजनाओं का नेतृत्व करना पसंद है",
                "category": "enterprising",
                "weight": 1.0,
            },
            {
                "id": "E2",
                "question": "I like to persuade and influence others",
                "question_hindi": "मुझे दूसरों को समझाना और प्रभावित करना पसंद है",
                "category": "enterprising",
                "weight": 1.0,
            },
            {
                "id": "E3",
                "question": "I am comfortable taking risks for potential rewards",
                "question_hindi": "मैं संभावित लाभ के लिए जोखिम लेने में सहज हूँ",
                "category": "enterprising",
                "weight": 0.9,
            },
            {
                "id": "C1",
                "question": "I prefer structured and organized work environments",
                "question_hindi": "मुझे संरचित और संगठित कार्य वातावरण पसंद है",
                "category": "conventional",
                "weight": 1.0,
            },
            {
                "id": "C2",
                "question": "I enjoy working with numbers and detailed records",
                "question_hindi": "मुझे संख्याओं और विस्तृत रिकॉर्ड के साथ काम करना पसंद है",
                "category": "conventional",
                "weight": 1.0,
            },
            {
                "id": "C3",
                "question": "I like following established procedures and rules",
                "question_hindi": "मुझे स्थापित प्रक्रियाओं और नियमों का पालन करना पसंद है",
                "category": "conventional",
                "weight": 0.8,
            },
        ]

    def get_questions(self) -> List[Dict[str, Any]]:
        """Get all RIASEC assessment questions"""
        return self.questions

    def calculate_scores(self, responses: Dict[str, int]) -> Dict[RIASECCode, float]:
        """Calculate RIASEC scores from responses (1-5 scale)"""
        category_scores = {
            "realistic": 0.0,
            "investigative": 0.0,
            "artistic": 0.0,
            "social": 0.0,
            "enterprising": 0.0,
            "conventional": 0.0,
        }

        category_weights = {
            "realistic": 0.0,
            "investigative": 0.0,
            "artistic": 0.0,
            "social": 0.0,
            "enterprising": 0.0,
            "conventional": 0.0,
        }

        for question in self.questions:
            question_id = question["id"]
            if question_id in responses:
                score = responses[question_id] * question["weight"]
                category = question["category"]
                category_scores[category] += score
                category_weights[category] += question["weight"]

        # Normalize scores (0-1 scale)
        normalized_scores = {}
        for category in category_scores:
            if category_weights[category] > 0:
                normalized_scores[RIASECCode(category)] = min(
                    category_scores[category] / (category_weights[category] * 5), 1.0
                )
            else:
                normalized_scores[RIASECCode(category)] = 0.0

        return normalized_scores


class MentalSkillsAssessment:
    """Assessment for mental and psychological skills"""

    def __init__(self):
        self.questions = self._load_mental_skills_questions()

    def _load_mental_skills_questions(self) -> List[Dict[str, Any]]:
        """Load mental skills assessment questions"""
        return [
            {
                "id": "AS1",
                "question": "I can break down complex problems into smaller parts",
                "question_hindi": "मैं जटिल समस्याओं को छोटे भागों में विभाजित कर सकता हूँ",
                "skill": "analytical_thinking",
                "scenario": "You're given a dataset with declining sales. How would you approach analyzing it?",
            },
            {
                "id": "DR1",
                "question": "I can draw logical conclusions from given information",
                "question_hindi": "मैं दी गई जानकारी से तार्किक निष्कर्ष निकाल सकता हूँ",
                "skill": "deductive_reasoning",
                "scenario": "If A leads to B, and B leads to C, what can you conclude about A and C?",
            },
            {
                "id": "PR1",
                "question": "I quickly notice patterns in data or behavior",
                "question_hindi": "मैं डेटा या व्यवहार में पैटर्न को जल्दी देख लेता हूँ",
                "skill": "pattern_recognition",
                "scenario": "Looking at the sequence 2, 4, 8, 16, what comes next and why?",
            },
            {
                "id": "SP1",
                "question": "I can plan long-term strategies effectively",
                "question_hindi": "मैं दीर्घकालिक रणनीतियों की प्रभावी योजना बना सकता हूँ",
                "skill": "strategic_planning",
                "scenario": "How would you plan a 5-year career growth strategy?",
            },
            {
                "id": "EI1",
                "question": "I understand and manage emotions well",
                "question_hindi": "मैं भावनाओं को अच्छी तरह समझता और प्रबंधित करता हूँ",
                "skill": "emotional_intelligence",
                "scenario": "How would you handle a frustrated team member?",
            },
            {
                "id": "SM1",
                "question": "I remain calm under pressure",
                "question_hindi": "मैं दबाव में शांत रहता हूँ",
                "skill": "stress_management",
                "scenario": "Describe how you handle tight deadlines.",
            },
        ]

    def get_scenarios(self) -> List[Dict[str, Any]]:
        """Get all mental skills assessment scenarios"""
        return self.questions

    def calculate_mental_skills(
        self, responses: Dict[str, int], scenario_responses: Dict[str, str]
    ) -> Dict[MentalSkill, float]:
        """Calculate mental skills scores"""
        skill_scores = {}

        # Basic scoring from self-assessment (1-5 scale)
        for question in self.questions:
            question_id = question["id"]
            skill = MentalSkill(question["skill"])

            if question_id in responses:
                base_score = responses[question_id] / 5.0

                # Enhance score based on scenario response quality
                scenario_key = f"{question_id}_scenario"
                if scenario_key in scenario_responses:
                    scenario_bonus = self._evaluate_scenario_response(
                        scenario_responses[scenario_key], skill
                    )
                    base_score = min(base_score + scenario_bonus, 1.0)

                skill_scores[skill] = base_score

        return skill_scores

    def _evaluate_scenario_response(self, response: str, skill: MentalSkill) -> float:
        """Evaluate scenario response quality (0-0.2 bonus)"""
        if not response or len(response.strip()) < 20:
            return 0.0

        # Simple keyword-based evaluation
        skill_keywords = {
            MentalSkill.ANALYTICAL_THINKING: [
                "analyze",
                "break down",
                "data",
                "systematic",
                "method",
            ],
            MentalSkill.DEDUCTIVE_REASONING: [
                "logic",
                "conclude",
                "therefore",
                "reasoning",
                "inference",
            ],
            MentalSkill.PATTERN_RECOGNITION: [
                "pattern",
                "trend",
                "sequence",
                "relationship",
                "connection",
            ],
            MentalSkill.STRATEGIC_PLANNING: [
                "plan",
                "strategy",
                "goal",
                "long-term",
                "roadmap",
            ],
            MentalSkill.EMOTIONAL_INTELLIGENCE: [
                "empathy",
                "understand",
                "emotion",
                "communicate",
                "support",
            ],
            MentalSkill.STRESS_MANAGEMENT: [
                "calm",
                "prioritize",
                "organize",
                "manage",
                "balance",
            ],
        }

        keywords = skill_keywords.get(skill, [])
        response_lower = response.lower()
        keyword_matches = sum(1 for keyword in keywords if keyword in response_lower)

        # Bonus based on keyword matches and response length
        length_bonus = min(len(response) / 500, 0.1)  # Up to 0.1 for detailed responses
        keyword_bonus = min(
            keyword_matches * 0.02, 0.1
        )  # Up to 0.1 for keyword matches

        return length_bonus + keyword_bonus


class PersonalityAssessment:
    """Big Five personality assessment"""

    def __init__(self):
        self.questions = self._load_personality_questions()

    def _load_personality_questions(self) -> List[Dict[str, Any]]:
        """Load Big Five personality questions"""
        return [
            # Openness to Experience
            {
                "id": "O1",
                "question": "I enjoy exploring new ideas and concepts",
                "question_hindi": "मुझे नए विचारों और अवधारणाओं की खोज करना पसंद है",
                "trait": "openness",
                "reverse": False,
            },
            {
                "id": "O2",
                "question": "I prefer routine and familiar activities",
                "question_hindi": "मुझे दिनचर्या और परिचित गतिविधियां पसंद हैं",
                "trait": "openness",
                "reverse": True,
            },
            # Conscientiousness
            {
                "id": "C1",
                "question": "I am always prepared and organized",
                "question_hindi": "मैं हमेशा तैयार और संगठित रहता हूँ",
                "trait": "conscientiousness",
                "reverse": False,
            },
            {
                "id": "C2",
                "question": "I often leave tasks unfinished",
                "question_hindi": "मैं अक्सर काम अधूरे छोड़ देता हूँ",
                "trait": "conscientiousness",
                "reverse": True,
            },
            # Extraversion
            {
                "id": "E1",
                "question": "I enjoy being around people and socializing",
                "question_hindi": "मुझे लोगों के साथ रहना और मेल-जोल करना पसंद है",
                "trait": "extraversion",
                "reverse": False,
            },
            {
                "id": "E2",
                "question": "I prefer working alone rather than in groups",
                "question_hindi": "मुझे समूह में काम करने की बजाय अकेले काम करना पसंद है",
                "trait": "extraversion",
                "reverse": True,
            },
            # Agreeableness
            {
                "id": "A1",
                "question": "I am sympathetic and warm toward others",
                "question_hindi": "मैं दूसरों के प्रति सहानुभूतिपूर्ण और गर्मजोश हूँ",
                "trait": "agreeableness",
                "reverse": False,
            },
            {
                "id": "A2",
                "question": "I tend to be critical of others",
                "question_hindi": "मैं दूसरों की आलोचना करता हूँ",
                "trait": "agreeableness",
                "reverse": True,
            },
            # Neuroticism
            {
                "id": "N1",
                "question": "I often feel anxious and worried",
                "question_hindi": "मैं अक्सर चिंतित और परेशान महसूस करता हूँ",
                "trait": "neuroticism",
                "reverse": False,
            },
            {
                "id": "N2",
                "question": "I remain calm in stressful situations",
                "question_hindi": "मैं तनावपूर्ण स्थितियों में शांत रहता हूँ",
                "trait": "neuroticism",
                "reverse": True,
            },
        ]

    def calculate_personality_scores(
        self, responses: Dict[str, int]
    ) -> Dict[str, float]:
        """Calculate Big Five personality scores"""
        trait_scores = {
            "openness": 0.0,
            "conscientiousness": 0.0,
            "extraversion": 0.0,
            "agreeableness": 0.0,
            "neuroticism": 0.0,
        }

        trait_counts = {trait: 0 for trait in trait_scores}

        for question in self.questions:
            question_id = question["id"]
            if question_id in responses:
                score = responses[question_id]
                if question["reverse"]:
                    score = 6 - score  # Reverse score (1-5 scale)

                trait = question["trait"]
                trait_scores[trait] += score
                trait_counts[trait] += 1

        # Normalize scores (0-1 scale)
        normalized_scores = {}
        for trait in trait_scores:
            if trait_counts[trait] > 0:
                normalized_scores[trait] = trait_scores[trait] / (
                    trait_counts[trait] * 5
                )
            else:
                normalized_scores[trait] = 0.5  # Default middle score

        return normalized_scores


class TestingFramework:
    """Main testing framework coordinator"""

    def __init__(self):
        self.riasec_assessment = RIASECAssessment()
        self.mental_skills_assessment = MentalSkillsAssessment()
        self.personality_assessment = PersonalityAssessment()

    def get_test_by_type(self, test_type: str) -> PsychologicalTest:
        """Get test structure by type"""
        if test_type == "riasec":
            return PsychologicalTest(
                test_id="riasec_v1",
                test_name="RIASEC Career Interest Assessment",
                test_type="riasec",
                questions=self.riasec_assessment.questions,
                scoring_method="weighted_average",
                description="Assess your career interests based on Holland's RIASEC model",
                duration_minutes=15,
            )
        elif test_type == "mental_skills":
            return PsychologicalTest(
                test_id="mental_skills_v1",
                test_name="Mental Skills Assessment",
                test_type="mental_skills",
                questions=self.mental_skills_assessment.questions,
                scoring_method="scenario_enhanced",
                description="Evaluate your analytical, deductive, and psychological abilities",
                duration_minutes=25,
                riasec_scores={},  # Add default value
                mental_skills_scores={},  # Add default value
            )
        elif test_type == "personality":
            return PsychologicalTest(
                test_id="big_five_v1",
                test_name="Big Five Personality Assessment",
                test_type="personality",
                questions=self.personality_assessment.questions,
                scoring_method="trait_aggregation",
                description="Assess your personality traits using the Big Five model",
                duration_minutes=10,
                riasec_scores={},  # Add default value
                mental_skills_scores={},  # Add default value
            )
        else:
            raise ValueError(f"Unknown test type: {test_type}")

    def process_test_response(self, test_response: TestResponse) -> Dict[str, float]:
        """Process test response and calculate scores"""
        if test_response.test_id == "riasec_v1":
            scores = self.riasec_assessment.calculate_scores(test_response.responses)
            return {k.value: v for k, v in scores.items()}
        elif test_response.test_id == "mental_skills_v1":
            scenario_responses = {
                k: v
                for k, v in test_response.responses.items()
                if k.endswith("_scenario")
            }
            basic_responses = {
                k: v
                for k, v in test_response.responses.items()
                if not k.endswith("_scenario")
            }
            scores = self.mental_skills_assessment.calculate_mental_skills(
                basic_responses, scenario_responses
            )
            return {k.value: v for k, v in scores.items()}
        elif test_response.test_id == "big_five_v1":
            return self.personality_assessment.calculate_personality_scores(
                test_response.responses
            )
        else:
            raise ValueError(f"Unknown test ID: {test_response.test_id}")

    def generate_comprehensive_profile(
        self, test_responses: List[TestResponse]
    ) -> Dict[str, Any]:
        """Generate comprehensive psychological profile from all test responses"""
        profile = {
            "riasec_scores": {},
            "mental_skills": {},
            "personality_traits": {},
            "recommended_careers": [],
            "psychological_insights": [],
            "development_areas": [],
        }

        for response in test_responses:
            scores = self.process_test_response(response)

            if response.test_id == "riasec_v1":
                profile["riasec_scores"] = scores
            elif response.test_id == "mental_skills_v1":
                profile["mental_skills"] = scores
            elif response.test_id == "big_five_v1":
                profile["personality_traits"] = scores

        # Generate insights based on combined results
        profile["psychological_insights"] = self._generate_insights(profile)
        profile["development_areas"] = self._identify_development_areas(profile)

        return profile

    def _generate_insights(self, profile: Dict[str, Any]) -> List[str]:
        """Generate psychological insights from test results"""
        insights = []

        # RIASEC insights
        if profile["riasec_scores"]:
            top_codes = sorted(
                profile["riasec_scores"].items(), key=lambda x: x[1], reverse=True
            )[:2]
            if top_codes:
                insights.append(
                    f"Your strongest career interests are in {top_codes[0][0]} and {top_codes[1][0] if len(top_codes) > 1 else ''} areas"
                )

        # Mental skills insights
        if profile["mental_skills"]:
            strong_skills = [
                skill
                for skill, score in profile["mental_skills"].items()
                if score > 0.7
            ]
            if strong_skills:
                insights.append(
                    f"You demonstrate strong {', '.join(strong_skills[:3])} abilities"
                )

        # Personality insights
        if profile["personality_traits"]:
            for trait, score in profile["personality_traits"].items():
                if score > 0.7:
                    insights.append(
                        f"You score high on {trait}, indicating strong {trait} characteristics"
                    )

        return insights

    def _identify_development_areas(self, profile: Dict[str, Any]) -> List[str]:
        """Identify areas for skill development"""
        development_areas = []

        # Mental skills development
        if profile["mental_skills"]:
            weak_skills = [
                skill
                for skill, score in profile["mental_skills"].items()
                if score < 0.5
            ]
            for skill in weak_skills[:3]:  # Top 3 development areas
                development_areas.append(
                    f"Consider developing your {skill.replace('_', ' ')} abilities"
                )

        return development_areas
