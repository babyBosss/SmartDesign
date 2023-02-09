Task for SmartDesign 
---
REST API методы:
* Создать новый товар
* Получить список названий товаров, с возможностью фильтрации (поиска) и сортировки по назвавнию и (или) цене
* Добавить товар в корзину, поменять количество товара в корзине


### Installation 

Download repo
```
git clone https://github.com/babyBosss/SmartDesign.git
```
Start database server
```
docker pull postgres  

docker run -d --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

Launch the application 
```
cd SmartDesign 

python3 create_db.py

python3 main.py
```


| URL    | Method  |Params | Description | 
|--------|---------|-------|-------------|
| 127.0.0.1:80/api/create_new|POST| vendor_code,name,brand,selling_price   |  Создать новый товар |
| 127.0.0.1:80/api/product_list|GET| orderby (optional) | Получить список названий товаров  |
| 127.0.0.1:80/api/product_list/search|GET| name or(and) price | Поиск и сортировка по назвавнию и (или) цене|
|127.0.0.1:80/api/cart/add_product|POST| vendor_code, amount|Добавить в корзину|
|127.0.0.1:80/api/cart/update_amount|PUT| vendor_code, amount|Обновить количество в корзине|
|127.0.0.1:80/api/product/info|GET| vendor_code|Информация о товаре|



#### Examples
```
curl -X POST http://127.0.0.1:80/api/create_new -H "Content-Type: application/json" -d '{"vendor_code":"1234567", "name":"new phone", "selling_price":11111, "brand":"my brand"}'

curl -X GET http://127.0.0.1:80/api/product_list
curl -X GET http://127.0.0.1:80/api/product_list -H "Content-Type: application/json" -d '{"orderby":"desc"}'

curl -X GET http://127.0.0.1:80/api/product_list/search -H "Content-Type: application/json" -d '{"name":"a"}'
curl -X GET http://127.0.0.1:80/api/product_list/search -H "Content-Type: application/json" -d '{"name":"a", "price":"=10990"}'

curl -X POST http://127.0.0.1:80/api/cart/add_product -H "Content-Type: application/json" -d '{"vendor_code":"10CMA456XXH", "amount":3}'

curl -X PUT http://127.0.0.1:80/api/cart/update_amount -H "Content-Type: application/json" -d '{"vendor_code":"10CMA456XXH", "amount":1}'

curl -X GET http://127.0.0.1:80/api/product/info -H "Content-Type: application/json" -d '{"vendor_code":"120874054"}'  

curl -X GET http://127.0.0.1:80/api/other-url 
```
