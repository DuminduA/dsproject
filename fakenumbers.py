import csv
from faker import Faker

# Create a Faker instance
faker = Faker()

# Define the number of contacts to generate
num_contacts = 5000

# Define the path for the CSV file
csv_file = 'contacts.csv'

# Define the field names for the CSV file
field_names = ['Contact Name', 'Phone Number']
generated_numbers = set()

# Generate fake contacts and write them to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    
    while len(generated_numbers) < num_contacts:  # Continue until desired number of unique contacts is generated
        contact_name = faker.name()  # Generate a fake name
        phone_number = faker.random_number(digits=10)  # Generate a 10-digit fake phone number
        if phone_number not in generated_numbers:  # Check if the number is unique
            generated_numbers.add(phone_number)  # Add the number to the set of generated numbers
            writer.writerow({'Contact Name': contact_name, 'Phone Number': f"+{phone_number}"})  # Write the contact to the CSV file

print(f'Generated {num_contacts} contacts in {csv_file}.')