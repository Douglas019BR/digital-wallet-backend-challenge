## Considerações

Seria possível elaborar uma melhor relação do uso do banco de dados para teste, eu gosto da abordagem de subir um container local com um banco de teste para tornar completamente independente do banco de dados do projeto.
Por simplificação e prazo curto vou manter a abordagem de simplesmente criar um usuário de testes no banco de dados e mockar demais chamadas ao banco.