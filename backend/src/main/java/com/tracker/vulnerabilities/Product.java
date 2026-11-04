package com.tracker.vulnerabilities;

//records are immutable data classes that require only the type and name of fields.
public record Product(

        Long id,
        String name,
        String version

) {}