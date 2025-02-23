# use linkedin api to get the profile of a user

import http.client
import logging
from linkedin_api import Linkedin
import json
import csv

# Enable HTTP debugging
http.client.HTTPConnection.debuglevel = 1

# Set up logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

print("Starting LinkedIn API test...")
api = Linkedin('cubyic3@gmail.com', 'i*rPy7@KZ.,A33S')
print("Authentication complete")


'''# Test a simple API call
print("Attempting to get profile...")
profile = api.get_profile('william-gates')  # Bill Gates' profile as an example
print("Profile retrieved!")
print(profile)

# Get contact information
contact_info = api.get_profile_contact_info('william-gates')

print(f"Name: {profile['firstName']} {profile['lastName']}")
print(f"Email: {contact_info.get('email_address')}")
print("---")
'''


"""# off the documentation:
# Search for software engineers at Google
people = api.search_people(
    keyword_title="Software Engineer",
    keyword_company="Google",
    limit = 10,
    include_private_profiles=False,
    network_depths=["F", "S", "O"]
)
print("got the people")
# Process the results
for person in people:
    print(f"Name: {person['name']}")
    print(f"Title: {person['jobtitle']}")
    print(f"Location: {person['location']}")
    print("---")

print(f"\nNumber of results: {len(people)}")"""

# Try a simple keyword search with private profiles included
people = api.search_people(
    keywords="software engineer",
    network_depths=["F", "S", "O"],
    include_private_profiles=True
)

print(f"\nNumber of results: {len(people)}")

# Prepare CSV file
with open('linkedin_results.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Name', 'Job Title', 'Location', 'Profile Type', 'URN ID', 
                    'Full Name', 'Email', 'Phone Numbers', 'Websites'])
    
    # Write data for each person
    for person in people:
        name = person.get('name', 'Unknown')
        job_title = person.get('jobtitle', 'Unknown')
        location = person.get('location', 'Unknown')
        profile_type = 'Private' if name == 'LinkedIn Member' else 'Public'
        urn_id = person.get('urn_id', 'Unknown')
        
        # Default values for profile data
        full_name = email = phone_numbers = websites = 'Not accessible'
        
        # Try to get additional info if profile is public
        if profile_type == 'Public' and urn_id != 'Unknown':
            try:
                profile = api.get_profile(urn_id)
                contact_info = api.get_profile_contact_info(urn_id)
                
                full_name = f"{profile.get('firstName', '')} {profile.get('lastName', '')}"
                email = contact_info.get('email_address', 'Not available')
                phone_numbers = ', '.join(contact_info.get('phone_numbers', [])) or 'Not available'
                websites = ', '.join(contact_info.get('websites', [])) or 'Not available'
            except Exception as e:
                print(f"Couldn't get additional data for {name}: {e}")
        
        # Write row to CSV
        writer.writerow([name, job_title, location, profile_type, urn_id, 
                        full_name, email, phone_numbers, websites])

print(f"\nExported {len(people)} results to linkedin_results.csv")

# Print statistics
print("\nStatistics:")
print(f"Total profiles: {len(people)}")
print(f"Private profiles: {sum(1 for p in people if p['name'] == 'LinkedIn Member')}")
print(f"Public profiles: {sum(1 for p in people if p['name'] != 'LinkedIn Member')}")
