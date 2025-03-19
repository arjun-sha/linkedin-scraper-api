class LinkedinParser:
    """
    Parses LinkedIn profile data from a JSON response.
    Extracts details such as profile information, contact details, skills, 
    experience, education, and connections.
    """

    def __init__(self, response):
        """
        Initializes the LinkedinParser with a response object.
        Args:
            response (Response): The response object containing LinkedIn profile data.
        """
        self.response = response
        self.json_data = response.json()

    def extract_profile_data(self) -> dict:
        """
        Extracts general profile details including name, headline, summary, 
        industry, location, skills, experience, and education.
        Returns:
            dict: A dictionary containing the extracted profile information:
                - public_id (str): LinkedIn public identifier.
                - full_name (str): Full name (first and last).
                - headline (str): Profile headline.
                - summary (str): Profile summary.
                - industry_name (str): Industry name.
                - location (str): Geographic location.
                - skills (list): List of skills.
                - experience (list): List of work experiences.
                - education (list): List of education details.
        """
        first_name = self.json_data.get("profile", {}).get("firstName")
        last_name = self.json_data.get("profile", {}).get("lastName")
        public_id = self.json_data.get("profile", {}).get("miniProfile", {}).get("publicIdentifier")
        summary = self.json_data.get("profile", {}).get("summary")
        headline = self.json_data.get("profile", {}).get("headline")
        industry_name = self.json_data.get("profile", {}).get("industryName")
        location = self.json_data.get("profile", {}).get("geoLocationName")
        skills = self._extract_skills()
        experience = self._extract_experience()
        education = self._extract_education()

        full_name = f"{first_name} {last_name}"
        summary = " ".join(summary.split()).strip() if summary else None
        return {
            "public_id": public_id,
            "full_name": full_name,
            "headline": headline,
            "summary": summary,
            "industry_name": industry_name,
            "location": location,
            "skills": skills,
            "experience": experience,
            "education": education,
        }

    def extract_contact_details(self) -> dict:
        """
        Extracts the contact details such as email and phone number.
        Returns:
            dict: A dictionary containing:
                - email (str): The user's email address.
                - phone (str): The user's phone number.
        """
        email = self.json_data.get("emailAddress")
        phone = self.json_data.get("phoneNumbers", [{}])[0].get("number")

        return {"email": email, "phone": phone}

    def extract_connections_profile_ids(self) -> list:
        """
        Extracts LinkedIn public identifiers of connections.
        Returns:
            list: A list of LinkedIn profile IDs of the user's connections.
        """
        connections_elements = self.json_data.get("elements", [])
        if not connections_elements:
            return []

        extracted_profile_ids = [
            item.get("connectedMemberResolutionResult", {}).get("publicIdentifier")
            for item in connections_elements
            if item.get("connectedMemberResolutionResult", {}).get("publicIdentifier")
        ]
        return extracted_profile_ids

    def _extract_skills(self) -> list:
        """
        Extracts a list of skills from the profile.
        Returns:
            list: A list of skill names.
        """
        raw_skills = self.json_data.get("skillView", {}).get("elements")
        if not raw_skills:
            return []

        return [skill.get("name") for skill in raw_skills if skill.get("name")]

    def _extract_experience(self) -> list:
        """
        Extracts work experience details.
        Returns:
            list: A list of dictionaries containing:
                - job_title (str): Job title.
                - company_name (str): Name of the company.
                - location (str): Job location.
                - period (dict): Time period of employment.
                - description (str): Job description.
        """
        raw_experience = self.json_data.get("positionView", {}).get("elements")
        if not raw_experience:
            return []

        return [
            {
                "job_title": item.get("title"),
                "company_name": item.get("companyName"),
                "location": item.get("locationName"),
                "period": item.get("timePeriod"),
                "description": item.get("description"),
            }
            for item in raw_experience
        ]

    def _extract_education(self) -> list:
        """
        Extracts education details.
        Returns:
            list: A list of dictionaries containing:
                - school_name (str): Name of the school/university.
                - degree (str): Degree obtained.
                - period (dict): Time period attended.
        """
        raw_education_data = self.json_data.get("educationView", {}).get("elements")
        if not raw_education_data:
            return []

        return [
            {
                "school_name": item.get("schoolName"),
                "degree": item.get("degreeName"),
                "period": item.get("timePeriod"),
            }
            for item in raw_education_data
        ]
