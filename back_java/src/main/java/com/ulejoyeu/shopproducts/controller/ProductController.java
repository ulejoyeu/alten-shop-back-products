package com.ulejoyeu.shopproducts.controller;

import com.ulejoyeu.shopproducts.entities.Product;
import com.ulejoyeu.shopproducts.repositories.ProductRepository;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("products")
@Service
@CrossOrigin
@Tag(name = "Products")
public class ProductController {
    @Autowired
    private ProductRepository productRepository;

    @Operation(summary = "Get all products")
    @GetMapping(value = "")
    public ResponseEntity<List<Product>> findAllProducts() {
        return ResponseEntity.ok(productRepository.findAll());
    }

    @Operation(summary = "Get a product by its id")
    @ApiResponses(value = {
            @ApiResponse(
                    responseCode = "200",
                    description = "Found the product",
                    content = { @Content(mediaType = "application/json", schema = @Schema(implementation = Product.class))}),
            @ApiResponse(
                    responseCode = "404",
                    description = "Product not found",
                    content = @Content
            )
    })
    @GetMapping(value = "/{id}")
    public ResponseEntity<Product> findById(@Parameter(description = "id of the product to be searched") @PathVariable Long id) {
        Optional<Product> product = productRepository.findById(id);
        return product.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }

    @Operation(summary = "Create a new product")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "201",
                            description = "New product created",
                            content = { @Content(mediaType = "application/json", schema = @Schema(implementation = Product.class)) }
                    )
            }
    )
    @PostMapping(value = "")
    public ResponseEntity<Product> createProduct(@RequestBody Product product) {
        Product createdProduct = productRepository.save(product);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdProduct);
    }

    @Operation(summary = "Update an existing product retrieved by its id")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Existing product has been updated",
                            content = { @Content(mediaType = "application/json", schema = @Schema(implementation = Product.class)) }
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "Product not found",
                            content = @Content
                    )
            }
    )
    @PatchMapping(value = "/{id}")
    public ResponseEntity<Product> updateProduct(@Parameter(description = "id of the product to be updated") @PathVariable Long id, @RequestBody Product product) {
        Optional<Product> oldProduct = productRepository.findById(id);
        // Patch existing product
        if (oldProduct.isPresent()) {
            Product newProduct = oldProduct.get();
            newProduct.setCode(product.getCode());
            newProduct.setName(product.getName());
            newProduct.setDescription(product.getDescription());
            newProduct.setPrice(product.getPrice());
            newProduct.setQuantity(product.getQuantity());
            newProduct.setInventoryStatus(product.getInventoryStatus());
            newProduct.setCategory(product.getCategory());
            newProduct.setImage(product.getImage());
            newProduct.setRating(product.getRating());

            productRepository.save(newProduct);
            return ResponseEntity.ok(newProduct);
        }
        return ResponseEntity.notFound().build();
    }

    @Operation(summary = "Delete a product by its id")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Product has been successfully deleted", content = @Content),
            @ApiResponse(responseCode = "404", description = "Product has not been found", content = @Content)
    })
    @DeleteMapping(value = "/{id}")
    public ResponseEntity<Map<String, String>> deleteProduct(@Parameter(description = "id of the product to be deleted") @PathVariable Long id) {
        if (productRepository.existsById(id)) {
            productRepository.deleteById(id);
            return ResponseEntity.ok(Map.of("message", "Product with id " + id + " has been successfully deleted"));
        }
        return ResponseEntity.notFound().build();
    }
}
