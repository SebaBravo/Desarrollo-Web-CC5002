package com.sebastian_bravo.tarea4.model;

import java.util.List;
import jakarta.persistence.*; 

@Entity
@Table(name = "region")
public class Region {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "nombre", nullable = false, length = 200)
    private String nombre;

    
    @OneToMany(mappedBy = "region")
    private List<Comuna> comunas;

    
    public Integer getId() {
        return id;
    }
    public String getNombre() {
        return nombre;
    }
}