package com.sebastian_bravo.tarea4.model;

import jakarta.persistence.*;

@Entity
@Table(name = "contactar_por")
public class ContactarPor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    
    @Enumerated(EnumType.STRING)
    @Column(name = "nombre", nullable = false)
    private MetodoContacto nombre; 
 

    @Column(name = "identificador", nullable = false, length = 150)
    private String identificador;

    @ManyToOne
    @JoinColumn(name = "aviso_id", nullable = false)
    private AvisoAdopcion aviso;

    
    public MetodoContacto getNombre() {
        return nombre;
    }
}