## Considerações

Seria possível elaborar uma melhor relação do uso do banco de dados para teste, eu gosto da abordagem de subir um container local com um banco de teste para tornar completamente independente do banco de dados do projeto.
Por simplificação e prazo curto vou manter a abordagem de simplesmente criar um usuário de testes no banco de dados e mockar demais chamadas ao banco.

Por conta da organização de testes do FastApi somado com a não especificidades de testes unitários, mas sim de testes automatizados, os testes foram elaborados em torno das rotas, e não necessáriamente em torno de unidades, caracterizando-se assim muito mais testes de integração/api do que como testes unitários de fato. Tal escolha garante maior cobertura de código testado com menos testes e também o melhor funcionamento da aplicação, visto que testa de fato o funcionamento de cada rota