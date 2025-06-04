

# VirtualCoin

 Video Demo: https://youtu.be/VMQjynSVoyM

##NOTE
University Project collaborated by Muhammad Moosa (moosa817) and Ammar Munnawar (ammar-munawar)

## Project Description
VirtualCoin is a prototype cryptocurrency application built to showcase how blockchain technology with transactions works. The application demonstrates the fundamental principles of blockchain, including block creation, transaction handling, and secure signing. Users can sign up, log in, make transactions, and explore the blockchain through a user-friendly interface.

## Distinctiveness and Complexity
### Distinctiveness
VirtualCoin stands out from other projects due to its focus on blockchain technology and cryptocurrency. Unlike typical social networks or e-commerce sites, VirtualCoin delves into the complexities of blockchains, transactions, and cryptographic security. The application provides a hands-on demonstration of how a blockchain operates, making it unique and educational.

### Complexity
VirtualCoin involves several complex components:
1. **Blockchain Implementation:** The project includes a custom blockchain implementation, where each block contains multiple transactions. Blocks are linked together through cryptographic hashes.
2. **Transaction Management:** The application manages transactions between users, including signing and verifying transactions using RSA keys.
3. **User Authentication and Authorization:** Users can sign up, log in, and have unique public keys associated with their accounts.
4. **Cryptographic Security:** The project uses cryptographic functions for signing transactions, ensuring that transactions are secure and tamper-proof.
5. **Dynamic and Interactive UI:** The application provides an interactive blockchain explorer, allowing users to view blocks and transactions in a visually appealing manner.
6. **Mobile-Responsive Design:** The project is designed to be mobile-responsive, ensuring a seamless experience across different devices.

## File Structure and Contents
- **coinapp/**
  - **__init__.py**
  - **admin.py**
  - **apps.py**
  - **blockchain.py:** Contains the blockchain logic, including block creation and hashing.
  - **crypto_utils.py:** Provides cryptographic functions for generating RSA key pairs and signing data.
  - **forms.py:** Contains Django forms for user registration and login.
  - **migrations/**: Database migration files.
  - **models.py:** Defines the database models for CustomUser, Transaction, and Block.
  - **templates/**: Contains HTML templates for different pages.
    - **base.html:** Base template for the application.
    - **blockchain.html:** Template for the blockchain explorer page.
    - **index.html:** Template for the homepage.
    - **login.html:** Template for the login page.
    - **make_transaction.html:** Template for making transactions.
    - **setup.html:** Template for the initial setup page.
    - **signup.html:** Template for the signup page.
    - **success.html:** Template for the success page.
  - **tests.py:** Contains tests for the application.
  - **transactions.py:** Handles transaction logic, including creating and verifying transactions.
  - **urls.py:** URL routing for the application.
  - **views.py:** Contains the view functions for handling HTTP requests.
- **db.sqlite3:** SQLite database file.
- **manage.py:** Django management script.
- **requirements.txt:** Lists the Python packages required to run the application.
- **static/**: Contains static files (CSS, JavaScript, images).
- **virtualcoin_project/**
  - **__init__.py**
  - **asgi.py**
  - **settings.py:** Django settings for the project.
  - **urls.py:** URL routing for the project.
  - **wsgi.py**

## How to Run the Application
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd virtualcoin
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application:**
   Open your web browser and go to `http://127.0.0.1:8000`

## Additional Information
- **System Initial Setup:**
  Upon registration, each new user is given 1000 virtual coins as an initial balance. Users are also provided with their RSA private key file for signing transactions.
- **Making Transactions:**
  Users can send coins to other users by providing the recipient's username or public key, the amount to send, and their private key file for signing the transaction.
- **Blockchain Explorer:**
  Users can explore the blockchain to view all blocks and their associated transactions, along with hashes and other details.

## Dependencies
The application requires the following Python packages, as listed in `requirements.txt`:
- asgiref==3.8.1
- cffi==1.16.0
- cryptography==42.0.8
- Django==5.0.6
- pycparser==2.22
- sqlparse==0.5.0
- typing_extensions==4.12.2

Ensure these dependencies are installed to run the application successfully.

---

Feel free to customize this README.md further based on any additional details or specific requirements you have.
