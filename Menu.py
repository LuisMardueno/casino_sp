import os
from dotenv import load_dotenv
import pygame
import pygame_menu
from supabase import create_client
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
client = create_client(url, key)

def register_user(email, password, nombre):
    response = client.auth.sign_up({
        'email': email,
        'password': password
    })
    client.table("users").insert({"nombre": nombre}).execute()
    return response

# Initialize pygame
pygame.init()

# Set screen dimensions
screen = pygame.display.set_mode((600, 400))

# Set window title
pygame.display.set_caption('User Registration')

# Define global variables to store username and password
user_data = {'email': '', 'password': '','nombre': ''}

# Function to handle the registration button click

# Sign in user
def login_user():
    username = user_data.get('email')
    password = user_data.get('password')

    if not username or not password:
        print("Username and password are required!")
        return

    try:
        # Attempt to log in using Supabase auth
        response = client.auth.sign_in_with_password({
            'email': username,  # Assuming you're using email for login
            'password': password
        })
        print("Login successful!")
        return response
    except Exception as e:
        print(f"Login failed: {str(e)}")


def set_email(value):
    user_data['email'] = value
def set_password(value):
    user_data['password'] = value
def set_nombre(value):
    user_data['nombre'] = value

# Create a pygame_menu instance
menu = pygame_menu.Menu('Register', 600, 400, theme=pygame_menu.themes.THEME_BLUE)

# Add text input for username and password
menu.add.text_input('email: ', default='', onchange=set_email)
menu.add.text_input('Password: ', default='', onchange=set_password, password=True)
menu.add.text_input('nombre: ', default='Invitado', onchange=set_nombre,)

# Add a button to register
menu.add.button('Registrarse', lambda: register_user(user_data['email'], user_data['password'], user_data['nombre']))
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