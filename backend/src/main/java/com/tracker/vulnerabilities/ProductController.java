package com.tracker.vulnerabilities;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController                             // inform that this class is a REST controller
@RequestMapping("/api/products")     // set the base path for all endpoints in this controller
public class ProductController {

    private final ProductRepository repository; //final means const, can't override
    public ProductController( ProductRepository repository ) {
        this.repository = repository;
    }

    @GetMapping
    public List<Product> getAll() {
        return repository.findAll();    // Spring method that returns data from database in JSON format
    }

}