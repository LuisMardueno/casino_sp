import os
from dotenv import load_dotenv
import pygame
import pygame_menu
from supabase import create_client

# Load environment variables
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
client = create_client(url, key)

# Register a user function using Supabase
def register_user(email, password):
    try:
        # Step 1: Sign up the user using Supabase Auth
        response = client.auth.sign_up({
            'email': email,
            'password': password
        })

        # Accessing the user object using the dot notation
        user = response.user  # This is the user object returned by the sign_up method

        if not user:
            print("User registration failed.")
            return

        # Get the user ID from the user object
        user_id = user.id

        # Step 2: Insert additional user data into the 'profiles' table
        additional_data = {
            'id': user_id,  # Use the ID from the auth user
            'email': email,
            'created_at': 'now()'  # Let the database handle the timestamp
        }

        # Insert the additional data into the 'profiles' table
        insert_response = client.table('profiles').insert(additional_data).execute()

        if insert_response.error:
            print("Error inserting user data into 'profiles'.")
            return

        print(f"User {email} registered successfully!")
        return response
    except Exception as e:
        print(f"Registration failed: {str(e)}")

# Initialize pygame
pygame.init()

# Set screen dimensions
screen = pygame.display.set_mode((600, 400))

# Set window title
pygame.display.set_caption('User Registration')

# Define global variables to store email and password
user_data = {'email': '', 'password': ''}

# Function to handle user login
def login_user():
    email = user_data.get('email')
    password = user_data.get('password')

    if not email or not password:
        print("Email and password are required!")
        return

    try:
        # Attempt to log in using Supabase auth
        response = client.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        print("Login successful!")
        pygame.display.set_mode((400, 300))
        pygame.display.flip()
        return response
    except Exception as e:
        print(f"Login failed: {str(e)}")

# Function to store email
def set_email(value):
    user_data['email'] = value

# Function to store the password
def set_password(value):
    user_data['password'] = value

# Create a pygame_menu instance
menu = pygame_menu.Menu('Register', 600, 400, theme=pygame_menu.themes.THEME_BLUE)

# Add text input for email and password
menu.add.text_input('Email: ', default='', onchange=set_email)
menu.add.text_input('Password: ', default='', onchange=set_password, password=True)

# Add a button to register (use lambda to delay the function call until button is pressed)
menu.add.button('Registrarse', lambda: register_user(user_data['email'], user_data['password']))

# Add a button to login (also wrapped in lambda)
menu.add.button('Login', lambda: login_user())

# Add a button to exit
menu.add.button('Salir', pygame_menu.events.EXIT)

# Game loop
def main():
    running = True
    while running:
        screen.fill((0, 0, 0))

        # Check for pygame events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Update the menu
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
