# LinkedIn Job Automation Bot

Este projeto é um bot automatizado desenvolvido em Python usando Selenium, projetado para realizar buscas personalizadas de vagas de emprego no LinkedIn. O bot permite que o usuário escolha filtros como a data de anúncio das vagas e a localização. Após aplicar os filtros, o bot coleta todos os resultados da busca (títulos das vagas e links) e os armazena automaticamente em um arquivo Excel, facilitando a análise posterior das oportunidades encontradas.

Funcionalidades:
 - Autenticação automática no LinkedIn.
 - Busca e aplicação de filtros personalizados (localização, data de anúncio, etc.).
 - Interação com botões e campos de busca.
 - Armazenamento dos resultados em um arquivo Excel (nomes das vagas e links).
 - Interface interativa para seleção dos filtros de busca.

Bibliotecas:
 - Selenium: Para automação do navegador e interação com a interface do LinkedIn.
 - OpenPyXL: Para criação e manipulação de arquivos Excel.
 - Time: Para controle de pausas entre as interações.
