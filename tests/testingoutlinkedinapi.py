# use linkedin api to get the profile of a user

import http.client
import logging
from linkedin_api import Linkedin
import json

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
    network_depths=["O"],
    include_private_profiles=True
)

print(f"\nNumber of results: {len(people)}")

# Print first 3 results with their contact info
print("\nFirst 3 results with contact info:")
for i, person in enumerate(people[:3]):
    print(f"\nPerson {i + 1}:")
    print(f"Name: {person.get('name', 'Unknown')}")
    
    if person.get('urn_id'):
        try:
            # Get detailed profile
            profile = api.get_profile(person['urn_id'])
            # Get contact info using the same urn_id
            contact_info = api.get_profile_contact_info(person['urn_id'])
            
            print("Profile data:")
            print(f"Full Name: {profile.get('firstName', '')} {profile.get('lastName', '')}")
            print(f"Contact Info: {json.dumps(contact_info, indent=2)}")
        except Exception as e:
            print(f"Couldn't get profile/contact data: {e}")
    print("---")

# Print some statistics
print("\nStatistics:")
print(f"Total profiles: {len(people)}")
print(f"Private profiles: {sum(1 for p in people if p['name'] == 'LinkedIn Member')}")
print(f"Public profiles: {sum(1 for p in people if p['name'] != 'LinkedIn Member')}")
