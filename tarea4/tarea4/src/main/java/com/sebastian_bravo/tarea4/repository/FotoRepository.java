package com.sebastian_bravo.tarea4.repository;

import com.sebastian_bravo.tarea4.model.Foto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FotoRepository extends JpaRepository<Foto, Integer> {
    List<Foto> findByEliminadaOrderByIdDesc(Boolean eliminada);
}