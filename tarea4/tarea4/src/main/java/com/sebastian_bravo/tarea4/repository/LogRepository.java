package com.sebastian_bravo.tarea4.repository;

import com.sebastian_bravo.tarea4.model.Log;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LogRepository extends JpaRepository<Log, Long> {
    
    List<Log> findAllByOrderByFechaDesc();
}