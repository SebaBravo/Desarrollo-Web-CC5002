package com.sebastian_bravo.tarea4.model;

import jakarta.persistence.*;

@Entity
@Table(name = "foto")
public class Foto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "nombre_archivo", nullable = false, length = 300)
    private String nombreArchivo;

    @Column(name = "ruta_archivo", nullable = false, length = 300)
    private String rutaArchivo;

    @ManyToOne
    @JoinColumn(name = "actividad_id", nullable = false)
    private AvisoAdopcion aviso;

    // CORRECCIÓN: Cambiamos Byte a Boolean porque MySQL TINYINT(1) se mapea a Boolean
    @Column(name = "eliminada", nullable = false)
    private Boolean eliminada = false;

    // Constructores
    public Foto() {
    }

    public Foto(String rutaArchivo, String nombreArchivo, AvisoAdopcion aviso) {
        this.rutaArchivo = rutaArchivo;
        this.nombreArchivo = nombreArchivo;
        this.aviso = aviso;
        this.eliminada = false; // false = 0 en base de datos
    }

    // Getters y Setters
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getNombreArchivo() { return nombreArchivo; }
    public void setNombreArchivo(String nombreArchivo) { this.nombreArchivo = nombreArchivo; }

    public String getRutaArchivo() { return rutaArchivo; }
    public void setRutaArchivo(String rutaArchivo) { this.rutaArchivo = rutaArchivo; }

    public AvisoAdopcion getAviso() { return aviso; }
    public void setAviso(AvisoAdopcion aviso) { this.aviso = aviso; }

    public Boolean getEliminada() { return eliminada; }
    public void setEliminada(Boolean eliminada) { this.eliminada = eliminada; }
}