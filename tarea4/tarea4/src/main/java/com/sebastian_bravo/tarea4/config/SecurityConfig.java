package com.sebastian_bravo.tarea4.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests((requests) -> requests
                // 1. Recursos estáticos y Webjars -> Públicos
                .requestMatchers("/static/**", "/css/**", "/js/**", "/images/**", "/uploads/**", "/*.css", "/*.js", "/*.png", "/*.jpg", "/*.ico").permitAll()
                
                // 2. Rutas públicas de la tarea anterior -> Públicos
                .requestMatchers("/", "/listado", "/listado_avisos", "/detalle_aviso/**", "/estadisticas", "/api/**").permitAll()
                
                // 3. ¡IMPORTANTE! Permitir la página de error para poder ver qué falla
                .requestMatchers("/error").permitAll()

                // 4. Rutas protegidas TAREA 5 (Admin) -> Requieren autenticación
                .requestMatchers("/t5-admin-fotos", "/mensajes-log").authenticated()
                
                // Cualquier otra cosa -> Requiere autenticación por defecto
                .anyRequest().authenticated()
            )
            .formLogin((form) -> form
                .permitAll()
                .defaultSuccessUrl("/t5-admin-fotos", true)
            )
            .logout((logout) -> logout.permitAll())
            // Deshabilitar CSRF puede ayudar si tienes problemas con los POST de las API desde JS
            .csrf(csrf -> csrf.ignoringRequestMatchers("/api/**"));

        return http.build();
    }

    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails admin = User.withDefaultPasswordEncoder()
                .username("cc5002")
                .password("examen")
                .roles("ADMIN")
                .build();

        return new InMemoryUserDetailsManager(admin);
    }
}