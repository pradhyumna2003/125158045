from flask import Flask, request, jsonify
import uuid
import requests

app = Flask(__name__)

# Mock data representing products from different e-commerce companies
categories = [
    "Phone", "Computer", "TV", "Earphone", "Tablet", "Charger", 
    "Mouse", "Keypad", "Bluetooth", "Pendrive", "Remote", 
    "Speaker", "Headset", "Laptop", "PC"
]
companies = ["AMZ", "FLP", "SNP", "MYN", "AZO"]
test_url="http://20.244.56.144/test/companies/AMZ/categories/"
auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIxMTM4Njc5LCJpYXQiOjE3MjExMzgzNzksImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjA4ZTBmMjZhLTg2NTUtNDBhMS1hYjdlLWJhZmI4NGZhM2JjZCIsInN1YiI6IjEyNTE1ODA0NUBzYXN0cmEuYWMuaW4ifSwiY29tcGFueU5hbWUiOiJTQVNUUkEiLCJjbGllbnRJRCI6IjA4ZTBmMjZhLTg2NTUtNDBhMS1hYjdlLWJhZmI4NGZhM2JjZCIsImNsaWVudFNlY3JldCI6IkFFb0NuRHNvd2lya1dCQU4iLCJvd25lck5hbWUiOiJQcmFkaHl1bW5hIiwib3duZXJFbWFpbCI6IjEyNTE1ODA0NUBzYXN0cmEuYWMuaW4iLCJyb2xsTm8iOiIxMjUxNTgwNDUifQ.saSBVehwjfTiqRnUCZpaevYP6RB7H281DSgZc312XhI"

headers = {
    "Authorization": f"Bearer {auth_token}"
}

def generate_unique_id():
    return str(uuid.uuid4())

@app.route('/categories/<categoryname>/products', methods=['GET'])
def get_products(categoryname):
    if categoryname not in categories:
        return jsonify({'error': 'Category not found'}), 404

    products = response = requests.get(f'{test_url}{categoryname}/products?top=10&minPrice=10&maxPrice=1000', headers=headers, timeout=0.5)
    n = int(request.args.get('n', 10))
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort_by', 'rating')
    order = request.args.get('order', 'desc')

    # Sorting products based on the query parameters
    reverse = (order == 'desc')
    products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    # Implement pagination
    start = (page - 1) * n
    end = start + n
    paginated_products = products[start:end]

    # Add unique IDs to each product
    for product in paginated_products:
        product['id'] = generate_unique_id()

    return jsonify(paginated_products)

if __name__ == '__main__':
    app.run(debug=True)
