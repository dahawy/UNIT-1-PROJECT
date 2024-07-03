import uuid
import bcrypt

# Generate a uniqe number of 8 digits
def generateUniqueID():
    unique_uuid = uuid.uuid4()
    # Convert UUID to a string and strip dashes
    uuid_str = str(unique_uuid).replace('-', '')
    # Extract the first 5 characters/digits
    uniqueID = uuid_str[:8]
    return uniqueID.upper()


# Function to hash a password
def hashPassword(password):
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashedPassword

# Function to verify a password
def verifyPassword(inputPassword, hashedPassword):
    return bcrypt.checkpw(inputPassword.encode('utf-8'), hashedPassword)
