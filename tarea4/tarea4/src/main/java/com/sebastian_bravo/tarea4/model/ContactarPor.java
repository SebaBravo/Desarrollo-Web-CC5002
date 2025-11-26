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

    // CORRECCIÓN: La base de datos usa 'actividad_id', no 'aviso_id'
    @ManyToOne
    @JoinColumn(name = "actividad_id", nullable = false)
    private AvisoAdopcion aviso;

    // Constructor vacío
    public ContactarPor() {}

    public ContactarPor(MetodoContacto nombre, String identificador, AvisoAdopcion aviso) {
        this.nombre = nombre;
        this.identificador = identificador;
        this.aviso = aviso;
    }

    // Getters y Setters
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public MetodoContacto getNombre() { return nombre; }
    public void setNombre(MetodoContacto nombre) { this.nombre = nombre; }

    public String getIdentificador() { return identificador; }
    public void setIdentificador(String identificador) { this.identificador = identificador; }

    public AvisoAdopcion getAviso() { return aviso; }
    public void setAviso(AvisoAdopcion aviso) { this.aviso = aviso; }
}