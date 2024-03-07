# Password Manager

## Overview

The Password Manager is a simple Python application that securely stores and manages user passwords. It allows users to store passwords for various accounts, retrieve passwords, generate strong passwords, and more.

## Features

1. **Secure Password Storage**: Uses encryption to securely store passwords.
2. **User-Friendly Interface**: Provides a simple and interactive graphical user interface (GUI).
3. **Master Password**: Users need to set and enter a master password to access their stored passwords.
4. **Password Generation**: Allows users to generate strong and random passwords.
5. **Database Storage**: Stores passwords in a local database file (`passwords.json`).

## Getting Started

1. **Set Master Password**:
    - When you run the application for the first time, it will prompt you to set a master password.
    - This master password is crucial and should be remembered, as it is needed to access stored passwords.

2. **Login**:
    - Enter your master password to log in and access the main menu.

3. **Main Menu Options**:
    - **Save Password**: Store a new password for a service.
    - **Retrieve Password**: Retrieve a stored password for a service.
    - **Generate Password**: Generate a strong and random password.
    - **Exit**: Close the application.

## Usage Example

```plaintext
1. Set Master Password:
   - Do you want to create a master password? (Yes/No)
   - Set your master password: [Enter your master password]

2. Login:
   - Enter your master password: [Enter your master password]

3. Main Menu:
   - Choose an option:
     - Save Password
     - Retrieve Password
     - Generate Password
     - Exit

4. Save Password:
   - Enter the service name: [Enter service name]
   - Enter the username: [Enter username]
   - Enter the password: [Enter password]

5. Retrieve Password:
   - Enter the service name: [Enter service name]
   - Enter the username: [Enter username]
   - Retrieved Password: [Display retrieved password]

6. Generate Password:
   - Generated Password: [Display generated password]
   - Copy to Clipboard: [Click to copy generated password]

7. Exit:
   - Close the application.

