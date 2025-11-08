package com.sebastian_bravo.tarea4.model;

import jakarta.persistence.*;

@Entity
@Table(name = "comuna")
public class Comuna {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "nombre", nullable = false, length = 200)
    private String nombre;

    
    @ManyToOne
    @JoinColumn(name = "region_id", nullable = false)
    private Region region;
    
    
    public Integer getId() {
        return id;
    }
    public String getNombre() {
        return nombre;
    }
    public Region getRegion() {
        return region;
    }
}