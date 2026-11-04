package com.tracker.vulnerabilities;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class ProductRepository {

    private final JdbcTemplate jdbc;    // Spring class that simplifies the communication with database

    public ProductRepository( JdbcTemplate jdbc ) {
        this.jdbc = jdbc;
    }

    public List<Product> findAll() {
        
        // String sql = """ ... """;  --> sql variable contains text which is SQL request
        String sql = """
                SELECT id, name, version
                FROM products
                ORDER BY name, version
        """;

        // rs = result set to store the return value from SQL request
        return jdbc.query( sql, (rs, rowNum) -> new Product (

                    rs.getLong("id"),
                    rs.getString("name"),
                    rs.getString("version")
        ));

    }
}