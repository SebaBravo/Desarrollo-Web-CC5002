package com.sebastian_bravo.tarea4.controller;

import com.sebastian_bravo.tarea4.model.Foto;
import com.sebastian_bravo.tarea4.model.Log;
import com.sebastian_bravo.tarea4.repository.FotoRepository;
import com.sebastian_bravo.tarea4.repository.LogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;
import java.util.Optional;

@Controller
public class AdminController {

    @Autowired
    private FotoRepository fotoRepository;

    @Autowired
    private LogRepository logRepository;

    // 1. Pantalla de Administración de Fotos
    @GetMapping("/t5-admin-fotos")
    public String adminFotos(Model model) {
        // Busca fotos que NO estén eliminadas (false), ordenadas por ID descendente (más nuevas primero)
        List<Foto> fotos = fotoRepository.findByEliminadaOrderByIdDesc(false);
        model.addAttribute("fotos", fotos);
        return "admin_fotos"; // Retorna la plantilla admin_fotos.html
    }

    // 2. Acción de Eliminar Foto (POST)
    @PostMapping("/t5-admin-fotos/eliminar")
    public String eliminarFoto(@RequestParam("idFoto") Integer idFoto,
                               @RequestParam("motivo") String motivo,
                               RedirectAttributes redirectAttributes) {
        
        // Validación del motivo (Requisito: 5 a 200 caracteres)
        if (motivo == null || motivo.trim().length() < 5 || motivo.trim().length() > 200) {
            redirectAttributes.addFlashAttribute("error", "El motivo debe tener entre 5 y 200 caracteres.");
            return "redirect:/t5-admin-fotos";
        }

        Optional<Foto> fotoOpt = fotoRepository.findById(idFoto);
        if (fotoOpt.isPresent()) {
            Foto foto = fotoOpt.get();
            
            // A. Borrado Lógico (Soft Delete)
            foto.setEliminada(true); // true = 1 en la BD
            fotoRepository.save(foto);

            // B. Guardar Log de Auditoría (Requisito estricto del enunciado)
            // Formato: "eliminado foto {id-foto} por usuario admin, motivo: {motivo}"
            String mensajeLog = String.format("eliminado foto %d por usuario admin, motivo: %s", foto.getId(), motivo);
            Log log = new Log(mensajeLog);
            logRepository.save(log);

            redirectAttributes.addFlashAttribute("success", "Foto eliminada correctamente.");
        } else {
            redirectAttributes.addFlashAttribute("error", "Foto no encontrada.");
        }

        return "redirect:/t5-admin-fotos";
    }

    // 3. Pantalla de Visualización de Logs
    @GetMapping("/mensajes-log")
    public String verLogs(Model model) {
        List<Log> logs = logRepository.findAllByOrderByFechaDesc();
        model.addAttribute("logs", logs);
        return "mensajes_log"; // Retorna la plantilla mensajes_log.html
    }
}