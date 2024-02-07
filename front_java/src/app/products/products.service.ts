import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Product } from './product.class';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {

    private static productslist: Product[] = null;
    private products$: BehaviorSubject<Product[]> = new BehaviorSubject<Product[]>([]);
    private API_BASE_URL = 'http://127.0.0.1:9000'; // Url du backend Java

    constructor(private http: HttpClient) { }

    getProducts(): Observable<Product[]> {
        if( ! ProductsService.productslist )
        {
            this.http.get<any>(this.API_BASE_URL + '/products').subscribe(data => {
                ProductsService.productslist = data;
                
                this.products$.next(ProductsService.productslist);
            });
        }
        else
        {
            this.products$.next(ProductsService.productslist);
        }

        return this.products$;
    }

    create(prod: Product): Observable<Product[]> {
        this.http.post<any>(this.API_BASE_URL + '/products', prod).subscribe(data => {
            ProductsService.productslist.push(data);
            this.products$.next(ProductsService.productslist);
        });

        return this.products$;
    }

    update(prod: Product): Observable<Product[]>{
        this.http.patch<any>(`${this.API_BASE_URL}/products/${prod.id}`, prod).subscribe(data => {
            
            ProductsService.productslist.forEach(element => {
                if(element.id == prod.id)
                {
                    element.name = data.name;
                    element.category = data.category;
                    element.code = data.code;
                    element.description = data.description;
                    element.image = data.image;
                    element.inventoryStatus = data.inventoryStatus;
                    element.price = data.price;
                    element.quantity = data.quantity;
                    element.rating = data.rating;
                }
            });

            this.products$.next(ProductsService.productslist);
        });

        return this.products$;
    }


    delete(id: number): Observable<Product[]>{
        console.log(`${this.API_BASE_URL}/products/${id}`);
        
        this.http.delete<any>(`${this.API_BASE_URL}/products/${id}`).subscribe(
            response => {
                console.log({response});
                ProductsService.productslist = ProductsService.productslist.filter(value => { return value.id !== id } );
                this.products$.next(ProductsService.productslist);
            }
        )
        return this.products$;
    }
}