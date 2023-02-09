from flask import Flask, jsonify, request
import psycopg2
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host='127.0.0.1',
        port='5432',
        user="postgres",
        password="mysecretpassword",
        database="postgres")


#  Создать новый товар
@app.route("/api/create_new", methods=["POST"])
def create_new():
    r = request.get_json()
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO product (vendor_code, name, brand, selling_price) VALUES (%s,%s,%s,%s);",
                    (r.get("vendor_code"), r.get("name"), r.get("brand"), r.get("selling_price")))
        conn.commit()
        answer = {"result": "success"}
    except Exception as e:
        conn.rollback()
        answer = {"result": "error", "description": str(e)}
    finally:
        conn.close()
    return jsonify(answer)


# Получить список названий товаров
@app.route("/api/product_list", methods=["GET"])
def get_list():
    content_type = request.headers.get('Content-Type')
    sort = ""
    if content_type == 'application/json':
        sort = request.json.get("orderby")
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT name FROM  product order by name {sort};")
        answer = {"result": "success", "names": [i[0] for i in cur.fetchall()]}
    except:
        answer = {"result": "error", "description": "'orderby' value should be in ['asc', 'desc']"}
    finally:
        conn.close()
    return jsonify(answer)


# Поиск и сортировка по назвавнию и (или) цене
@app.route("/api/product_list/search", methods=["GET"])
def search():
    conn = get_connection()
    try:
        cur = conn.cursor()
        name = request.json.get("name")
        price = request.json.get("price")
        if name and price:
            cur.execute(f"SELECT name FROM product where name like '%{name}%' and selling_price {price};")
        elif name:
            cur.execute(f"SELECT name FROM product where name like '%{name}%';")
        else:
            cur.execute(f"SELECT name FROM product where selling_price {price};")
        answer = {"result": "success", "found_names": [i[0] for i in cur.fetchall()]}
    except Exception as e:
        answer = {"result": "error", "description": "'price' examples: '>100', '=100', '>=100'"}
    finally:
        conn.close()
    return jsonify(answer)


# Добавить в корзину
@app.route("/api/cart/add_product")
def add_to_card():
    conn = get_connection()
    try:
        cur = conn.cursor()
        vendor_code = request.json.get("vendor_code")
        amount = request.json.get("amount")
        if vendor_code and amount:
            cur.execute(f"SELECT * FROM cart where vendor_code='{vendor_code}'")
            if not cur.fetchone():
                cur.execute(
                    f"INSERT INTO cart (vendor_code, amount, total_price) VALUES ('{vendor_code}',{amount} , {amount}*(select selling_price from product where product.vendor_code='{vendor_code}'));")
            else:
                cur.execute(
                    f"update cart set amount = amount + {amount}, total_price=(amount + {amount})*(select selling_price from product where product.vendor_code='{vendor_code}')  where vendor_code='{vendor_code}';")
            answer = {"result": "success"}
            conn.commit()
        else:
            answer = {"result": "error", "description": "specify the fields 'vendor_code' and 'amount'"}

    except Exception as e:
        answer = {"result": "error", "description": str(e)}
    finally:
        conn.close()
    return jsonify(answer)


# Обновить количество в корзине
@app.route("/api/cart/update_amount", methods=["PUT"])
def card_update_amount():
    conn = get_connection()
    try:
        cur = conn.cursor()
        vendor_code = request.json.get("vendor_code")
        amount = request.json.get("amount")
        if vendor_code and amount:
            cur.execute(
                f"update cart set amount = {amount}, total_price=({amount})*(select selling_price from product where product.vendor_code='{vendor_code}')  where vendor_code='{vendor_code}';")
            answer = {"result": "success"}
            conn.commit()
        else:
            answer = {"result": "error", "description": "specify the fields 'vendor_code' and 'amount'"}
    except Exception as e:
        answer = {"result": "error", "description": str(e)}
    finally:
        conn.close()
    return jsonify(answer)

#  Информация о товаре
@app.route("/api/product/info", methods=["GET"])
def info():
    conn = get_connection()
    try:
        cur = conn.cursor()
        vendor_code = request.json.get("vendor_code")
        cur.execute(f"SELECT vendor_code,name,brand,selling_price  FROM product where vendor_code='{vendor_code}';")
        res = cur.fetchall()
        answer = {"result": "success",
                  'vendor_code': res[0][0],
                  'name': res[0][1],
                  'brand': res[0][2],
                  'price': res[0][3]}
    except Exception as e:
        answer = {"result": "error", "description": str(e)}
    finally:
        conn.close()
    return jsonify(answer)


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
