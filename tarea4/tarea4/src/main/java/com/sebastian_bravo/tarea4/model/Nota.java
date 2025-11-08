package com.sebastian_bravo.tarea4.model;

import jakarta.persistence.*;

@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "nota", nullable = false)
    private Integer nota;

    @ManyToOne
    @JoinColumn(name = "aviso_id", nullable = false)
    private AvisoAdopcion aviso;

    
    public Nota() {} 
    
    public Nota(AvisoAdopcion aviso, Integer nota) {
        this.aviso = aviso;
        this.nota = nota;
    }

    // Getters
    public Integer getNota() { return nota; }
}