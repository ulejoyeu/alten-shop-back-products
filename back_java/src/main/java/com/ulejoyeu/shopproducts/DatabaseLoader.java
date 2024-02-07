package com.ulejoyeu.shopproducts;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ulejoyeu.shopproducts.entities.Product;
import com.ulejoyeu.shopproducts.repositories.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.InputStream;
import java.util.Arrays;

@Component
public class DatabaseLoader implements CommandLineRunner {

    @Autowired
    private ProductRepository productRepository;
    @Autowired
    private ResourceLoader resourceLoader;

    @Override
    public void run(String... args) throws Exception {
        Resource resource = resourceLoader.getResource("classpath:products.json");
        InputStream inputStream = resource.getInputStream();

        ObjectMapper mapper = new ObjectMapper();
        Product[] products = mapper.readValue(inputStream, Product[].class);
        Arrays.stream(products).forEach(productRepository::save);

        inputStream.close();
    }
}
