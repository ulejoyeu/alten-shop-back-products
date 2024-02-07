# Back-end

Développer un back-end permettant la gestion de produits définis plus bas. Vous pouvez utiliser la technologie de votre choix parmis la list suivante :

- nodejs/express
- Java/Spring Boot
- C#/.net Core
- Python/Flask

Le back-end doit gérer les API REST suivantes : 

| Resource           | POST                  | GET                            | PATCH                                    | PUT | DELETE           |
| ------------------ | --------------------- | ------------------------------ | ---------------------------------------- | --- | ---------------- |
| **/products**      | Create a new products | Retrieve all products          | X                                        | X   |     X            |
| **/products/1**    | X                     | Retrieve details for product 1 | Update details of product 1 if it exists | X   | Remove product 1 |

Un produit a les caractéristiques suivantes : 

``` typescript
class Product {
  id: number;
  code: string;
  name: string;
  description: string;
  price: number;
  quantity: number;
  inventoryStatus: string;
  category: string;
  image?: string;
  rating?: number;
}
```

Le back-end créé doit pouvoir gérer les produits dans une base de données SQL/NoSQL ou dans un fichier json.

Une liste de produits est disponible dans ce fichier : `front/assets/products.json`

Un front-end en Angular est disponible et permet d'utiliser l'API via cette adresse : `http://localhost:3000`

vous pouvez lancer le front-end angular avec la commande 'ng serve'

# Bonus

Vous pouvez ajouter des tests Postman ou Swagger pour valider votre API

# Solutions développées

J'ai réalisé deux APIs permettant de gérer les listes de produits 

## API Python Flask

L'API se trouve dans le dossier `back_python_flask`. Elle utilise un environnement virtuel python dont les dépendances se trouvent dans le fichier `requirements.txt`.

Pour créer l'environnement virtuel et installer les dépendances, il faut lancer les commandes suivantes sous Windows :
```
python -m virtualenv venv
venv/Scripts/activate.bat
pip install -r requirements.txt
```

Une fois l'environnement virtual créé, activé et les dépendances installées, le serveur se lance via la commande :
```
python app.py
```

La racine de l'API se trouve à l'adrese `http://127.0.0.1:5000/products`

Une documentation Swagger décrivant l'API est disponible à l'URL `http://127.0.0.1:5000/swagger/#/default`

## Front-End utilisant l'API Flask

Le front-end Angular permettant d'utiliser l'API Flask se trouve dans le dossier `front_python`.

Pour le lancer, il faut s'assurer que les dépendances sont bien installées en lançant la commande :
```
npm install
```

Puis l'application se lance avec la commande :
```
npm run start
```

L'application est alors disponible à l'URL `http://localhost:4200/products`

## API Spring Boot

L'API se trouve dans le dossier `back_java`. C'est une application Spring Boot utilisant le gestionnaire de dépendances Maven. Pour lancer l'application, il suffit d'importer le projet via le fichier `pom.xml` dans IntelliJ ou Eclipse.

Pour lancer l'application, il faut exécuter le fichier `ShopproductsApplication.java` qui se trouve dans le package `com.ulejoyeu.shopproducts`.

La racine de l'API se trouve alors à l'adresse `http://127.0.0.1:9000/products`.

Une documentation Swagger décrivant l'API est disponible à l'adresse `http://127.0.0.1:9000/swagger-ui/index.html#/`.

### Front-End utilisant l'API Spring Boot

Le front-end Angular permettant d'utilliser l'API Flask se trouve dans le dossier `front_java`.

Pour le lancer, il faut s'assurer que les dépendances sont bien installées en lançant la commande :
```
npm install
```

Puis l'application se lance avec la commande :
```
npm run start
```

L'application est alors disponible à l'URL `http://localhost:4200/products`