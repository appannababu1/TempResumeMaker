from GeminiAI import AI as bot
from ResumeMakerPrompts import DIRECT_RESUME_MAKER_PROMPT, RESUME_TEMPLATE_CREATION_PROMPT
import requests

class ResumeMaker:
    def __init__(self):
        self.bot = bot()
        self.user_details = None
        self.current_resume = None
        self.resumes_list = []

    def __response_to_html(response):
        # Filter content to ensure it is valid HTML
        # Trim content in between ```html to ``` 
        response = response.split("```html")[1] if "```html" in response else response
        response = response.split("```")[0] if "```" in response else response
        response = response.replace("```html", "")
        response = response.replace("```", "")
        
        return response

    def create_resume(self, job_description=None, job_description_url=None, user_prompt=None, resume_template=None):

        # Check if job description is provided
        if job_description is None and job_description_url is None:
            raise ValueError("Either job description or job description URL must be provided.")

        # Check if user details are provided
        if self.user_details is None:
            raise ValueError("User details are not set. Please set user details before creating a resume.")
        
        # If job description URL is provided, fetch the job description from the URL
        if job_description_url:
            try:
                response = requests.get(job_description_url)
                response.raise_for_status()  # Raise an error for bad responses
                job_description_from_url = response.content.decode('utf-8')
                job_description = job_description + "\n content from URL: " + job_description_from_url if job_description else job_description_from_url
            except requests.RequestException as e:
                raise ValueError(f"Error fetching job description from URL: {e}")
        
        final_prompt = RESUME_TEMPLATE_CREATION_PROMPT + DIRECT_RESUME_MAKER_PROMPT
        final_prompt += f"\n\nUser Details: {self.user_details}"
        final_prompt += f"\n\nJob Description: {job_description}"
        if resume_template:
            final_prompt += f"\n\nResume Template: {resume_template}"
        if user_prompt:
            final_prompt += f"\n\nIf possible, use the following prompt: {user_prompt}"

        # Create a resume based on the job description and user prompt
        response = self.bot.send_message(final_prompt)

        # Get HTML content from the response
        self.current_resume = ResumeMaker.__response_to_html(response)

        # Add the current resume to the list of resumes
        self.resumes_list.append(self.current_resume)

        # Return the current resume
        return self.current_resume, len(self.resumes_list) - 1
    
    def get_resumes_list(self):
        # Return the list of resumes
        return self.resumes_list
    
    def set_user_details(self, user_details):
        # Set the user details
        self.user_details = user_details

