package com.sebastian_bravo.tarea4.model;

import java.time.LocalDateTime;
import java.util.List;
import jakarta.persistence.*;

@Entity
@Table(name = "aviso_adopcion")
public class AvisoAdopcion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "fecha_ingreso", nullable = false)
    private LocalDateTime fechaIngreso;

    @Column(name = "sector", length = 100)
    private String sector;

    @Column(name = "nombre", nullable = false, length = 200)
    private String nombreContacto; 

    @Column(name = "email", nullable = false, length = 100)
    private String email;

    @Column(name = "celular", length = 15)
    private String celular;

    @Enumerated(EnumType.STRING) 
    @Column(name = "tipo", nullable = false)
    private TipoMascota tipo; 

    @Column(name = "cantidad", nullable = false)
    private Integer cantidad;

    @Column(name = "edad", nullable = false)
    private Integer edad;

    @Enumerated(EnumType.STRING)
    @Column(name = "unidad_medida", nullable = false)
    private UnidadMedida unidadMedida;

    @Column(name = "fecha_entrega", nullable = false)
    private LocalDateTime fechaEntrega;

    @Column(name = "descripcion", columnDefinition = "TEXT")
    private String descripcion;

    @ManyToOne
    @JoinColumn(name = "comuna_id", nullable = false)
    private Comuna comuna;
    
    @OneToMany(mappedBy = "aviso")
    private List<Foto> fotos;

    @OneToMany(mappedBy = "aviso")
    private List<ContactarPor> contactos;

    @OneToMany(mappedBy = "aviso")
    private List<Nota> notas;

    @OneToMany(mappedBy = "aviso")
    private List<Comentario> comentarios;

    // --- GETTERS (Esto es lo que faltaba para Thymeleaf) ---
    public Integer getId() { return id; }
    public LocalDateTime getFechaIngreso() { return fechaIngreso; }
    public String getSector() { return sector; }
    public String getNombreContacto() { return nombreContacto; }
    public String getEmail() { return email; } // ¡CRUCIAL!
    public String getCelular() { return celular; }
    public TipoMascota getTipo() { return tipo; }
    public Integer getCantidad() { return cantidad; }
    public Integer getEdad() { return edad; }
    public UnidadMedida getUnidadMedida() { return unidadMedida; }
    public LocalDateTime getFechaEntrega() { return fechaEntrega; }
    public String getDescripcion() { return descripcion; }
    public Comuna getComuna() { return comuna; } // ¡CRUCIAL!
    public List<Foto> getFotos() { return fotos; }
    public List<ContactarPor> getContactos() { return contactos; }
    public List<Nota> getNotas() { return notas; }
    public List<Comentario> getComentarios() { return comentarios; }

    // Lógica de negocio para promedio
    public String getPromedioNotas() {
        if (this.notas == null || this.notas.isEmpty()) {
            return "-"; 
        }
        double promedio = this.notas.stream()
                                .mapToInt(Nota::getNota)
                                .average()
                                .orElse(0.0);
        return String.format("%.1f", promedio);
    }
}