package com.sebastian_bravo.tarea4.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.sebastian_bravo.tarea4.repository.AvisoAdopcionRepository;
import com.sebastian_bravo.tarea4.repository.NotaRepository;
import com.sebastian_bravo.tarea4.model.AvisoAdopcion;
import com.sebastian_bravo.tarea4.model.Nota;

import java.util.List;
import java.util.Optional;

@Controller
public class AvisoController {

    @Autowired
    private AvisoAdopcionRepository avisoAdopcionRepository;

    @Autowired
    private NotaRepository notaRepository;

    @GetMapping("/")
    public String redirigirAListado() {
        return "redirect:/listado";
    }

    @GetMapping("/listado")
    public String mostrarListado(Model model) {
        List<AvisoAdopcion> avisos = avisoAdopcionRepository.findAll();
        model.addAttribute("avisos", avisos);
        
        model.addAttribute("autor", "Sebastian Bravo"); 
        return "listado"; 
    }

    @PostMapping("/api/evaluar/{avisoId}/{nota}")
    @ResponseBody 
    public ResponseEntity<String> evaluarAviso(
            @PathVariable("avisoId") Integer avisoId,
            @PathVariable("nota") Integer nota) {
        
        if (nota < 1 || nota > 7) {
            return ResponseEntity.badRequest().body("La nota debe estar entre 1 y 7.");
        }

        Optional<AvisoAdopcion> avisoOpt = avisoAdopcionRepository.findById(avisoId);
        if (avisoOpt.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        
        AvisoAdopcion aviso = avisoOpt.get();

        Nota nuevaNota = new Nota(aviso, nota);
        notaRepository.save(nuevaNota);

        AvisoAdopcion avisoActualizado = avisoAdopcionRepository.findById(avisoId).get();
        String nuevoPromedio = avisoActualizado.getPromedioNotas();

        return ResponseEntity.ok(nuevoPromedio);
    }
}