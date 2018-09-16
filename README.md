# CCO-130-Socket

# Descrição da etapa 1 pelo Prof. Paulo Matias


> **Etapa 1**
> O objetivo da primeira etapa é adquirir alguma vivência no uso de sockets. Implemente
> algum protocolo qualquer de camada de aplicação usando sockets TCP ou UDP, na linguagem
> e na plataforma de sua escolha.
>
> Dê preferência a algum protocolo de camada de aplicação que funcione sobre TCP, pois a
> próxima etapa do projeto será a implementação do TCP. Prefira também implementar algum
> protocolo que permita enviar grandes quantidades de dados em uma única conexão, pois isso
> será importante para testar o controle de fluxo e o controle de congestionamento do TCP
> durante a próxima etapa.
>
> Note que usar algum programa ou biblioteca pronta não equivale a implementar um protocolo
> de camada de aplicação! Use diretamente a API de sockets de baixo nível disponível na sua
> linguagem / plataforma. Durante a aula, mostramos alguns exemplos do uso de sockets TCP
> em Python. Esses exemplos estão disponíveis aqui.
>
> Caso você opte por alguma plataforma que não tenha suporte nativo a sockets, por exemplo
> FPGA ou microcontrolador, por enquanto você pode 1) trabalhar apenas com testes unitários;
>  2) trabalhar com simulação e integrar sockets ao simulador; ou 3) executar sockets em um
> computador para emular a parte ainda inexistente do circuito, e comunicar-se com a placa
> de desenvolvimento por meio de algum protocolo simples. Algumas dessas estratégias são
> exemplificadas neste esboço em Bluespec.

## Test.sh

```sh
nc localhost 8080
nc localhost 8080
```

# Planos

Como tem que ter grandes documentos sendo enviados para testar o controle de
fluxo e congestionamento, acho que vou implementar um GIS, com proxy para o
OSM.
