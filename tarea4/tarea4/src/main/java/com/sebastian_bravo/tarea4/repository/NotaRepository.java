package com.sebastian_bravo.tarea4.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.sebastian_bravo.tarea4.model.Nota;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Integer> {
    
}