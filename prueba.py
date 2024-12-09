from werkzeug.security import generate_password_hash

print("Admin:", generate_password_hash("1234"))
print("Técnico:", generate_password_hash("12345"))
print("Cliente:", generate_password_hash("123456"))