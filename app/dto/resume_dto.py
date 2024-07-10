from typing import List

from cuid2 import cuid_wrapper
from langchain_core.pydantic_v1 import BaseModel, Field

cuid_generator = cuid_wrapper()


blank_url = {"href": "", "label": ""}


class ModelWithAutoIdAndVisible(BaseModel):
    """
    Base class for models that need an auto-generated id
    """

    @property
    def id(self):
        return cuid_generator()

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["id"] = self.id
        data["visible"] = True
        return data


class ModelWithAutoIdAndVisibleAndUrl(ModelWithAutoIdAndVisible):
    """
    Base class for models that need an auto-generated id
    """

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["url"] = blank_url
        return data


class BasicProfile(BaseModel):
    """
    Basic profile of the person
    """

    name: str | None = Field(
        description="Full name of the person, if not provided, give ''", default=None
    )
    email: str | None = Field(
        description="Email address of the person, if not provided, ignore this field",
        default=None,
    )
    phone: str = Field(description="Phone number, if not provided, give empty string")
    location: str = Field(description="Current location of the person")

    def dict(self, *args, **kwargs):
        """
        Override the dict method to add the id and include all fields
        """
        data = super().dict(*args, **kwargs)
        # Additional fields
        data["url"] = blank_url
        data["picture"] = {
            "url": "",
            "size": 64,
            "effects": {"border": False, "hidden": False, "grayscale": False},
            "aspectRatio": 1,
            "borderRadius": 0,
        }
        data["headline"] = ""
        data["customFields"] = []

        return data


class ExperienceItem(ModelWithAutoIdAndVisibleAndUrl):
    """
    Experience of the person
    """

    date: str = Field(description="Date of the experience")
    company: str = Field(description="Company name of the experience")
    summary: str = Field(description="Summary of the the experience")
    location: str = Field(description="Location of the experience")
    position: str = Field(description="Position of the experience")


class ExperienceSection(BaseModel):
    """
    experience section
    """

    items: List[ExperienceItem] = Field(description="List of experiences", default=[])

    def dict(self, *args, **kwargs):
        """
        Override the dict method to add the id to the dictionary
        """
        data = super().dict(*args, **kwargs)
        data["id"] = "experience"
        data["name"] = "Experience"
        data["columns"] = 1
        data["visible"] = True
        data["separateLinks"] = True
        return data


class Certification(ModelWithAutoIdAndVisible):
    """
    Certification of the person
    """

    url: dict = Field(
        default_factory=lambda: {"href": "", "label": ""},
        description="URL related to the certification",
    )
    date: str = Field(description="Date the certification was obtained")
    name: str = Field(description="Name of the certification")
    issuer: str = Field(description="Organization that issued the certification")
    summary: str = Field(
        description="Brief summary or description of the certification"
    )
    visible: bool = Field(
        default=True, description="Whether the certification is visible"
    )


class EducationItem(ModelWithAutoIdAndVisible):
    """
    Education details of the person
    """

    area: str = Field(description="Field of study or major, default is empty string")
    date: str = Field(
        description="Date of graduation or period of study, default is empty string"
    )
    score: str = Field(
        description="Grade, GPA, or other score, default is empty string"
    )
    summary: str = Field(
        description="Summary or highlights of the education, default is empty string"
    )
    studyType: str = Field(description="Type of degree or certification")
    institution: str = Field(
        description="Name of the educational institution, default is empty string"
    )

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["url"] = blank_url
        return data


class EducationSection(BaseModel):
    """
    Education section
    """

    items: List[EducationItem] = Field(
        description="List of educational qualifications", default=[]
    )

    def dict(self, *args, **kwargs):
        """
        Override the dict method to add the id to the dictionary
        """
        data = super().dict(*args, **kwargs)
        data["id"] = "education"
        data["name"] = "Education"
        data["columns"] = 1
        data["visible"] = True
        data["separateLinks"] = True
        return data


class SummarySection(BaseModel):
    """
    Summary section of the resume
    """

    content: str = Field(description="Content of the summary", default="")

    def dict(self, *args, **kwargs):
        """
        Override the dict method to add the id to the dictionary
        """
        data = super().dict(*args, **kwargs)
        data["name"] = "Education"
        data["id"] = "summary"
        data["columns"] = 1
        data["visible"] = True
        data["separateLinks"] = True
        return data


class Skill(BaseModel):
    """
    Skill of the person
    """

    name: str = Field(description="Name of the skill", default="")
    level: int = Field(description="Proficiency level (1-5)", default=0)
    keywords: List[str] = Field(description="Keywords related to the skill", default=[])
    description: str = Field(description="Brief description of the skill", default="")


class Language(BaseModel):
    """
    Language proficiency of the person
    """

    name: str = Field(description="Name of the language")
    level: int = Field(description="Proficiency level (1-5)")
    description: str = Field(description="Brief description of language proficiency")


class Sections(BaseModel):
    """
    Sections of the resume
    """

    experience: ExperienceSection = Field(
        description="List of experiences", default=ExperienceSection()
    )
    education: EducationSection = Field(
        description="List of educational qualifications", default=EducationSection()
    )
    # certifications: List[Certification] = Field(
    #     description="List of certifications", default=[]
    # )
    summary: SummarySection = Field(
        description="Summary section of the resume", default=SummarySection()
    )
    languages: List[Language] = Field(
        description="List of language proficiencies", default=[]
    )

    def dict(self, *args, **kwargs):
        """
        Override the dict method to add the id to the dictionary
        """
        data = super().dict(*args, **kwargs)
        data["summary"] = {
            "id": "summary",
            "name": "Summary",
            "columns": 1,
            "content": "<p></p>",
            "visible": True,
            "separateLinks": True,
        }
        data["awards"] = {
            "id": "awards",
            "name": "Awards",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        data["custom"] = {}
        data["certifications"] = {
            "id": "certifications",
            "name": "Certifications",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        data["volunteer"] = {
            "id": "volunteer",
            "name": "Volunteering",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        data["references"] = {
            "id": "references",
            "name": "References",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        # publications
        data["publications"] = {
            "id": "publications",
            "name": "Publications",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        # interests
        data["interests"] = {
            "id": "interests",
            "name": "Interests",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        # language
        data["languages"] = {
            "id": "languages",
            "name": "Languages",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        # profiles
        data["profiles"] = {
            "id": "profiles",
            "name": "Profiles",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        # projects
        data["projects"] = {
            "id": "projects",
            "name": "Projects",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        # skills
        data["skills"] = {
            "id": "skills",
            "name": "Skills",
            "items": [],
            "columns": 1,
            "visible": True,
            "separateLinks": True,
        }
        # metadata

        return data


class Data(BaseModel):
    """
    Data of the resume
    """

    basics: BasicProfile = Field(description="Basic profile of the person")
    sections: Sections = Field(description="Sections of the resume")

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["metadata"] = {
            "css": {
                "value": ".section {\n\toutline: 1px solid #000;\n\toutline-offset: 4px;\n}",
                "visible": False,
            },
            "page": {
                "format": "a4",
                "margin": 18,
                "options": {"breakLine": True, "pageNumbers": True},
            },
            "notes": "",
            "theme": {
                "text": "#000000",
                "primary": "#dc2626",
                "background": "#ffffff",
            },
            "layout": [
                [
                    [
                        "profiles",
                        "summary",
                        "experience",
                        "education",
                        "projects",
                        "volunteer",
                        "references",
                    ],
                    [
                        "skills",
                        "interests",
                        "certifications",
                        "awards",
                        "publications",
                        "languages",
                    ],
                ]
            ],
            "template": "rhyhorn",
            "typography": {
                "font": {
                    "size": 14,
                    "family": "IBM Plex Serif",
                    "subset": "latin",
                    "variants": ["regular", "italic", "600"],
                },
                "hideIcons": False,
                "lineHeight": 1.5,
                "underlineLinks": True,
            },
        }
        return data


class RootModel(BaseModel):
    data: Data = Field(description="Data of the resume")

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["metadata"] = {
            "css": {
                "value": ".section {\n\toutline: 1px solid #000;\n\toutline-offset: 4px;\n}",
                "visible": False,
            },
            "page": {
                "format": "a4",
                "margin": 18,
                "options": {"breakLine": True, "pageNumbers": True},
            },
            "notes": "",
            "theme": {"text": "#000000", "primary": "#dc2626", "background": "#ffffff"},
            "layout": [
                [
                    ["profiles", "summary", "experience", "education", "projects"],
                    [
                        "skills",
                        "interests",
                        "certifications",
                        "awards",
                        "publications",
                        "languages",
                    ],
                ]
            ],
            "template": "rhyhorn",
            "typography": {
                "font": {
                    "size": 14,
                    "family": "IBM Plex Serif",
                    "subset": "latin",
                    "variants": ["regular", "italic", "600"],
                },
                "hideIcons": False,
                "lineHeight": 1.5,
                "underlineLinks": True,
            },
        }
        return data
