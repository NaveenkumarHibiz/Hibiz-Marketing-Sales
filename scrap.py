import requests
from bs4 import BeautifulSoup

# URL of the site
url = "https://hibizsolutions.com/"

# Make a request to the website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
response = requests.get(url, headers=headers)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the testimonial section (it's usually identified with a section or div class name)
# We'll search for elements with known patterns from the site structure
testimonials = soup.find_all('div', class_ = 'qodef-e-inner')

#print(testimonials)
# Extract testimonial text and author (if available)
for t in testimonials:
    print("------------")
    quote_content = t.find('p', class_ = 'qodef-e-text')
    author = t.find('h5', class_ = 'qodef-e-author-name')
    author_job = t.find('span', class_ = 'qodef-e-author-job').get_text(strip=True)
    author_job_role = author_job.split(' - ')[0] if author_job else 'Unknown'
    author_job_company = author_job.split(' - ')[1] if author_job and '-' in author_job else 'Unknown'
    print("------------")
    print(f"Testimonial: {quote_content.get_text(strip=True) if quote_content else 'No quote found'}")
    print(f"Author: {author.get_text(strip=True) if author else 'Unknown'}")
    print(f"Author Job: {author_job}")
    print(f"Author Job Role: {author_job_role}")
    print(f"Author Job Company: {author_job_company}")

company_points = soup.find_all('div', class_='elementor-element elementor-element-dfbec90 e-con-full e-flex e-con e-child')

print("\nCompany Points:", company_points)
print("\n",len(company_points))

for point in company_points:
    point_title = point.find('h3', class_='qodef-m-title').get_text(strip=True)
    point_div = point.find('div', class_ = 'elementor-element elementor-element-ed589a8 elementor-widget elementor-widget-text-editor" data-element_type="widget')
    
    point_content = point.find('div', class_='elementor-widget-container').get_text(strip=True)
    print("------------")
    print(f"Title: {point_title}")
    print(f"Content: {point_content}")


# print("\n Services Offered")

# services = soup.find_all('div', class_='elementor-element elementor-element-12d6cd30 e-con-full e-flex e-con e-child')
# print("Services found: ", len(services))
# print("Services:", services)
# for service in services:
#     service_title = service.find('h2', class_='qodef-m-title').get_text(strip=True)
#     service_content = service.find('div', class_ = 'elementor-widget-container')
#     print("Service title: ", service_title)
#     print("Service content: ",service_content.get_text(strip=True))

print("\n---------------------------")
