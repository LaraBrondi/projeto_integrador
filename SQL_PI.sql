use projeto_integrador;
create table Monitoramento_Sustentabilidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(100) NOT NULL,
    consumo_agua REAL NOT NULL,
    consumo_energia REAL NOT NULL,
    residuos_nao_reciclaveis REAL NOT NULL,
    residuos_reciclados REAL NOT NULL,
    transporte_usado VARCHAR(50) NOT NULL,
    data DATE NOT NULL
);
INSERT INTO Monitoramento_Sustentabilidade 
VALUES
(1, 'Arthur Pires', 120.5, 90.3, 1.2, 3.5, 'ônibus', '2025-04-01'),
(2, 'Beatriz Ramos', 200.0, 150.0, 2.5, 2.0, 'bicicleta', '2025-04-02'),
(3, 'Caio Fernandes', 180.2, 110.0, 1.0, 4.0, 'ônibus', '2025-04-03'),
(4, 'Diana Amorim', 220.0, 170.5, 3.0, 1.0, 'carro', '2025-04-04'),
(5, 'Eduardo Azevedo', 140.8, 80.5, 0.8, 5.0, 'bicicleta', '2025-04-05');
select * from monitoramento_sustentabilidade;
INSERT INTO Monitoramento_Sustentabilidade 
VALUES
(6, 'Felipe Martins', 160.0, 95.0, 1.5, 2.8, 'metrô', '2025-04-06'),
(7, 'Gabriela Lima', 190.5, 120.7, 2.2, 3.1, 'ônibus', '2025-04-07'),
(8, 'Henrique Alves', 210.3, 165.2, 2.8, 1.5, 'carro', '2025-04-08'),
(9, 'Isabela Duarte', 130.0, 85.0, 0.9, 4.2, 'bicicleta', '2025-04-09'),
(10, 'João Victor', 175.0, 105.0, 1.7, 2.5, 'ônibus', '2025-04-10'),
(11, 'Karen Lopes', 145.2, 92.5, 1.1, 3.8, 'metrô', '2025-04-11'),
(12, 'Lucas Ferreira', 155.5, 98.0, 1.4, 3.0, 'bicicleta', '2025-04-12'),
(13, 'Mariana Castro', 200.8, 140.0, 2.6, 2.2, 'ônibus', '2025-04-13'),
(14, 'Nicolas Ribeiro', 220.5, 175.3, 3.2, 0.5, 'carro', '2025-04-14'),
(15, 'Olivia Moreira', 138.7, 88.9, 1.0, 4.5, 'bicicleta', '2025-04-15');
select * from monitoramento_sustentabilidade;
alter table Monitoramento_Sustentabilidade modify column nome_usuario varchar(150) NOT NULL;

ALTER TABLE Monitoramento_Sustentabilidade 
ADD classificacao VARCHAR(150) NOT NULL;


