from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    def load(data):
        return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])


def list_products(page: int = 1, per_page: int = 20):
    conn = dao.connect('products.db')
    cursor = conn.cursor()
    
    # Fetch products with pagination and only required columns
    offset = (page - 1) * per_page
    cursor.execute('SELECT id, name, description, cost, qty FROM products LIMIT ? OFFSET ?', (per_page, offset))
    
    products = []
    rows = cursor.fetchall()
    
    for row in rows:
        products.append({
            'id': row['id'],
            'name': row['name'],
            'description': row['description'],
            'cost': row['cost'],
            'qty': row['qty']
        })
    
    cursor.close()
    conn.close()
    
    return products


def get_product(product_id: int) -> Product:
    return Product.load(dao.get_product(product_id))


def add_product(product: dict):
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    dao.update_qty(product_id, qty)


