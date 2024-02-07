package com.ulejoyeu.shopproducts;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.servers.Server;

@OpenAPIDefinition(
        info = @Info(
                contact = @Contact(
                        name = "Ulrich Lejoyeux",
                        email = "ulrich.lejoyeux@alten.com"
                ),
                description = "Backend to handle products",
                title = "Alten Shop Back Products",
                version = "1.0.0"
        ),
        servers = {
                @Server(
                        description = "Local ENV",
                        url = "http://localhost:9000"
                )
        }
)
public class OpenAPIConfig {
}
