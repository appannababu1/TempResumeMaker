DIRECT_RESUME_MAKER_PROMPT = """
I will provide my personal details below. Please generate a complete, beautiful, modern resume in clean, semantic HTML and Tailwind CSS. 

The output should be:
    - Fully filled with my provided details
    - Formatted specifically to fit perfectly on an A4-sized page (21cm x 29.7cm / 8.27in x 11.69in) for both web viewing and printing
    - Ensure that when printed on an A4 sheet, the styling, spacing, and layout do not break, overflow, or misalign
    - Use print-specific CSS (@media print) to control margins, hide unnecessary elements (if any), and optimize readability on paper
    - Maintain all styling, fonts, and visual hierarchy consistently between screen and print
    - Include clear typography, ample white space, and a professional color palette
    - Include these sections (only if data is provided): Header (Name, Title, Contact Info), Summary/About Me, Experience, Education, Skills, Projects, Certifications, and Languages
    - Adapt the layout/format intelligently based on the length and type of my details (adjust spacing, section placement, or use sidebar if beneficial)
    - Automatically format dates, titles, and descriptions consistently
    - Use accessible, semantic HTML (proper headings, lists, etc.) and Tailwind CSS utility classes for easy customization
    - Comment the code clearly to indicate where each section starts and ends

Important: Prioritize that the entire resume cleanly fits within 1 to 2 A4 pages maximum, without elements being cut off or wrapped awkwardly in print view.
"""

RESUME_TEMPLATE_CREATION_PROMPT = """
Generate a modern, professional, and ATS-friendly resume template using clean, semantic HTML and Tailwind CSS.

The template must meet all the following requirements:

ATS-Friendly Requirements
•	Use semantic HTML: <h1>, <h2>, <section>, <ul>, <li>, <p> (no tables, no unnecessary div nesting)
•	Use text-based headings and contact info (no icons for phone/email)
•	Avoid complex layouts that break ATS parsing (use CSS Grid or Flexbox, not absolute positioning)
•	Keep all text selectable and parsable (do not embed text in images)

A4 Layout & Print Requirements
•	Format perfectly for A4 size (21cm x 29.7cm / 8.27in x 11.69in)
•	Ensure when printed:
    o	No elements are cut off, misaligned, or overflowing
    o	Uses print-specific CSS (@media print) to optimize margins, remove unnecessary shadows or borders
•	The entire resume must fit cleanly within 1 to 2 A4 pages maximum

Content Sections (placeholders)
Include placeholders (empty text or sample dummy text) for:
•	Header: Name, Title, Contact Info, Profile Picture
•	Summary/About Me
•	Experience
•	Education
•	Skills
•	Projects
•	Certifications
•	Languages

Design & Code Quality
•	Use clear, legible typography and generous white space
•	Include sidebar layout option (ideal for profile pic + contact + skills), but ensure it degrades gracefully to single-column
•	Style with Tailwind CSS utility classes only (no inline styles, no external CSS files)
•	Comment the code clearly to indicate where each section starts and where to replace content
•	Ensure template is responsive (optional), but prioritize A4 print layout first
•	Avoid JavaScript, animations, or non-text graphics (to keep ATS-safe)

The result should be a clean, customizable, reusable HTML resume template with good accessibility, printability, and ATS compatibility.

"""

"""
Profile Picture Requirements
•	Include a clearly defined placeholder for a profile picture
•	Recommended dimensions: 300px x 300px, styled to 128x128px using Tailwind: w-32 h-32 rounded-full object-cover border border-gray-300 shadow print:shadow-none print:border-none print:w-24 print:h-24
•	Position the profile picture elegantly in header or sidebar
•	Add a developer comment indicating:
<!-- Replace "profile-pic.jpg" with your actual profile picture file path or URL -->
"""