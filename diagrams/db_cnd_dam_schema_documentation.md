# Documentação do Banco de Dados: `db_cnd_dam`

## Tabela: `audit_trail_entry`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 313.070
- Tamanho em Disco (aprox.): 89.66 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:34:34
- Última Atualização: 2025-09-17 15:16:23

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `model_type` | `varchar(255)` | MUL | NO | None |  |  |
| `happened_at` | `int` |  | NO | None |  |  |
| `foreign_pk` | `varchar(255)` |  | NO | None |  |  |
| `user_id` | `int` | MUL | YES | None |  |  |
| `type` | `varchar(255)` |  | NO | None |  |  |
| `data` | `text` |  | YES | None |  |  |

---

## Tabela: `auth_assignment`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 79
- Tamanho em Disco (aprox.): 0.03 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:12

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `item_name` | `varchar(64)` | PRI | NO | None |  | → `auth_item`.`name` |
| `user_id` | `int` | PRI | NO | None |  | → `user`.`id` |
| `created_at` | `int` |  | YES | None |  |  |

---

## Tabela: `auth_item`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 190
- Tamanho em Disco (aprox.): 0.06 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:13

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `name` | `varchar(64)` | PRI | NO | None |  |  |
| `type` | `int` | MUL | NO | None |  |  |
| `description` | `text` |  | YES | None |  |  |
| `rule_name` | `varchar(64)` | MUL | YES | None |  | → `auth_rule`.`name` |
| `data` | `text` |  | YES | None |  |  |
| `created_at` | `int` |  | YES | None |  |  |
| `updated_at` | `int` |  | YES | None |  |  |
| `group_code` | `varchar(64)` | MUL | YES | None |  | → `auth_item_group`.`code` |

---

## Tabela: `auth_item_child`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 20
- Tamanho em Disco (aprox.): 0.03 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:14

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `parent` | `varchar(64)` | PRI | NO | None |  | → `auth_item`.`name` |
| `child` | `varchar(64)` | PRI | NO | None |  | → `auth_item`.`name` |

---

## Tabela: `auth_item_group`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 2
- Tamanho em Disco (aprox.): 0.02 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:15

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `code` | `varchar(64)` | PRI | NO | None |  |  |
| `name` | `varchar(255)` |  | NO | None |  |  |
| `created_at` | `int` |  | YES | None |  |  |
| `updated_at` | `int` |  | YES | None |  |  |

---

## Tabela: `auth_rule`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 0
- Tamanho em Disco (aprox.): 0.02 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:16

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `name` | `varchar(64)` | PRI | NO | None |  |  |
| `data` | `text` |  | YES | None |  |  |
| `created_at` | `int` |  | YES | None |  |  |
| `updated_at` | `int` |  | YES | None |  |  |

---

## Tabela: `cidade`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 5.571
- Tamanho em Disco (aprox.): 0.41 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:17

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_estado` | `int` | MUL | NO | None |  | → `estado`.`id` |
| `nome` | `varchar(45)` |  | NO | None |  |  |

---

## Tabela: `cnd`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 63.162
- Tamanho em Disco (aprox.): 5.03 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:19
- Última Atualização: 2025-09-17 14:31:21

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_contribuinte` | `int` | MUL | NO | None |  | → `contribuinte`.`id` |
| `validade_certidao` | `date` |  | NO | None |  |  |
| `emissao` | `datetime` |  | NO | None |  |  |
| `numero` | `int` |  | NO | None |  |  |
| `chave` | `varchar(45)` |  | NO | None |  |  |

---

## Tabela: `contribuinte`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 196.517
- Tamanho em Disco (aprox.): 32.08 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:22
- Última Atualização: 2025-09-17 15:16:23

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | NO | None |  | → `entidade`.`id` |
| `nome_razao` | `varchar(120)` |  | NO | None |  |  |
| `cpf_cnpj` | `varchar(14)` |  | NO | None |  |  |
| `rg` | `varchar(20)` |  | YES | None |  |  |
| `uf` | `varchar(2)` |  | YES | None |  |  |
| `cidade` | `varchar(50)` |  | NO | None |  |  |
| `endereco` | `varchar(255)` |  | NO | None |  |  |
| `complemento` | `varchar(100)` |  | YES | None |  |  |
| `inscricao_municipal` | `varchar(20)` |  | YES | None |  |  |
| `status_cnd` | `int` |  | NO | None |  |  |

---

## Tabela: `dados_iptu`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 107.220
- Tamanho em Disco (aprox.): 29.52 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:35
- Última Atualização: 2025-09-16 14:21:32

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `endereco_imovel` | `varchar(255)` |  | NO | None |  |  |
| `bairro_imovel` | `varchar(255)` |  | YES | None |  |  |
| `complemento_imovel` | `varchar(255)` |  | YES | None |  |  |
| `area_terreno` | `decimal(15,2)` |  | NO | None |  |  |
| `area_edificacao` | `decimal(15,2)` |  | NO | None |  |  |
| `valor_m2_terreno` | `decimal(15,2)` |  | NO | None |  |  |
| `valor_m2_edificacao` | `decimal(15,2)` |  | NO | None |  |  |
| `aliquotas` | `varchar(30)` |  | NO | None |  |  |
| `valor_cip` | `decimal(15,2)` |  | NO | None |  |  |

---

## Tabela: `dados_tlf`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 21.725
- Tamanho em Disco (aprox.): 4.33 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:51
- Última Atualização: 2025-09-16 18:11:36

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `cod_cnae` | `varchar(10)` |  | NO | None |  |  |
| `atividade_principal` | `text` |  | NO | None |  |  |

---

## Tabela: `dam`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 125.910
- Tamanho em Disco (aprox.): 39.03 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:50:54
- Última Atualização: 2025-09-17 13:50:02

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_receita` | `int` | MUL | NO | None |  | → `receita`.`id` |
| `fk_contribuinte` | `int` | MUL | NO | None |  | → `contribuinte`.`id` |
| `fk_valores_dam` | `int` | MUL | NO | None |  | → `valores_dam`.`id` |
| `fk_dados_tlf` | `int` | MUL | YES | None |  | → `dados_tlf`.`id` |
| `fk_dados_iptu` | `int` | MUL | YES | None |  | → `dados_iptu`.`id` |
| `tipo` | `int` |  | NO | None |  |  |
| `numero` | `int` |  | NO | None |  |  |
| `exercicio` | `int` |  | NO | None |  |  |
| `inscricao` | `varchar(14)` |  | YES | None |  |  |
| `emissao` | `date` |  | NO | None |  |  |
| `vencimento` | `date` |  | NO | None |  |  |
| `vencimento_pgto` | `date` |  | YES | None |  |  |
| `data_pgto` | `date` |  | YES | None |  |  |
| `instrucoes` | `text` |  | YES | None |  |  |
| `qrcode_img` | `text` |  | YES | None |  |  |

---

## Tabela: `dam_log`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 11.081
- Tamanho em Disco (aprox.): 5.06 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:51:08
- Última Atualização: 2025-09-17 14:06:38

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | NO | None |  |  |
| `fk_dam` | `int` | MUL | YES | None |  |  |
| `numero_dam` | `int` |  | NO | None |  |  |
| `user_agent` | `char(255)` |  | NO | None |  |  |
| `ip` | `char(15)` |  | NO | None |  |  |
| `visit_time` | `datetime` |  | NO | None |  |  |
| `browser` | `char(30)` |  | YES | None |  |  |
| `os` | `char(20)` |  | YES | None |  |  |

---

## Tabela: `entidade`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 36
- Tamanho em Disco (aprox.): 0.05 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:51:10

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_cidade` | `int` | MUL | NO | None |  | → `cidade`.`id` |
| `nome` | `varchar(100)` |  | NO | None |  |  |
| `cnpj` | `varchar(14)` | UNI | NO | None |  |  |
| `cep` | `varchar(9)` |  | NO | None |  |  |
| `bairro` | `varchar(100)` |  | NO | None |  |  |
| `endereco` | `varchar(100)` |  | NO | None |  |  |
| `complemento` | `varchar(100)` |  | YES | None |  |  |
| `secretaria` | `varchar(50)` |  | NO | None |  |  |
| `departamento` | `varchar(50)` |  | NO | None |  |  |
| `brasao` | `text` |  | YES | None |  |  |
| `validade_certidao` | `int` |  | NO | None |  |  |
| `chave` | `text` |  | NO | None |  |  |
| `sigla_tlf` | `varchar(3)` |  | NO | None |  |  |
| `url` | `varchar(255)` |  | NO | None |  |  |
| `sigla` | `varchar(100)` |  | YES | None |  |  |

---

## Tabela: `estado`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 27
- Tamanho em Disco (aprox.): 0.02 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:51:12

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `nome` | `varchar(45)` |  | NO | None |  |  |
| `uf` | `varchar(2)` |  | NO | None |  |  |

---

## Tabela: `migration`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 15
- Tamanho em Disco (aprox.): 0.02 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:51:13

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `version` | `varchar(180)` | PRI | NO | None |  |  |
| `apply_time` | `int` |  | YES | None |  |  |

---

## Tabela: `receita`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 1.511
- Tamanho em Disco (aprox.): 0.16 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:51:14

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `nome` | `varchar(10)` |  | NO | None |  |  |
| `descricao` | `varchar(255)` |  | NO | None |  |  |

---

## Tabela: `requests`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 33.095
- Tamanho em Disco (aprox.): 85.08 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:51:15
- Última Atualização: 2025-09-17 15:16:23

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `bigint` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | YES | None |  | → `entidade`.`id` |
| `nome_arquivo` | `varchar(255)` |  | NO | None |  |  |
| `ip` | `varchar(15)` |  | NO | None |  |  |
| `local_ip` | `char(15)` |  | NO | None |  |  |
| `data_ini_req` | `datetime` |  | NO | None |  |  |
| `data_fim_req` | `datetime` |  | NO | None |  |  |
| `status` | `int` |  | NO | None |  |  |
| `mensagem` | `text` |  | NO | None |  |  |

---

## Tabela: `user`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 38
- Tamanho em Disco (aprox.): 0.03 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:51:42

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | YES | None |  | → `entidade`.`id` |
| `username` | `varchar(255)` |  | NO | None |  |  |
| `auth_key` | `varchar(32)` |  | NO | None |  |  |
| `password_hash` | `varchar(255)` |  | NO | None |  |  |
| `confirmation_token` | `varchar(255)` |  | YES | None |  |  |
| `status` | `int` |  | NO | 1 |  |  |
| `superadmin` | `smallint` |  | YES | 0 |  |  |
| `created_at` | `int` |  | NO | None |  |  |
| `updated_at` | `int` |  | NO | None |  |  |
| `registration_ip` | `varchar(15)` |  | YES | None |  |  |
| `bind_to_ip` | `varchar(255)` |  | YES | None |  |  |
| `email` | `varchar(128)` |  | YES | None |  |  |
| `email_confirmed` | `smallint` |  | NO | 0 |  |  |

---

## Tabela: `user_visit_log`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 273.356
- Tamanho em Disco (aprox.): 58.09 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:51:43
- Última Atualização: 2025-09-17 16:20:37

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `token` | `varchar(255)` |  | NO | None |  |  |
| `ip` | `varchar(15)` |  | NO | None |  |  |
| `language` | `char(2)` |  | NO | None |  |  |
| `user_agent` | `varchar(255)` |  | NO | None |  |  |
| `user_id` | `int` | MUL | YES | None |  | → `user`.`id` |
| `visit_time` | `int` |  | NO | None |  |  |
| `browser` | `varchar(30)` |  | YES | None |  |  |
| `os` | `varchar(20)` |  | YES | None |  |  |

---

## Tabela: `valores_dam`

- Motor (Engine): `InnoDB`
- Total de Linhas (aprox.): 135.105
- Tamanho em Disco (aprox.): 48.50 MB
- Collation: `utf8mb3_general_ci`
- Data de Criação: 2024-04-17 22:52:06
- Última Atualização: 2025-09-17 13:50:02

### Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `codigo_barras` | `varchar(48)` |  | YES | None |  |  |
| `valor_dam` | `decimal(15,2)` |  | NO | None |  |  |
| `base_calculo` | `decimal(15,2)` |  | NO | None |  |  |
| `parcela` | `varchar(20)` |  | NO | None |  |  |
| `valor_juros` | `decimal(15,2)` |  | NO | None |  |  |
| `valor_multa` | `decimal(15,2)` |  | NO | None |  |  |
| `valor_correcao` | `decimal(15,2)` |  | NO | None |  |  |
| `valor_desconto` | `decimal(15,2)` |  | NO | None |  |  |
| `valor_taxa_exp` | `decimal(15,2)` |  | NO | None |  |  |
| `valor_pagar` | `decimal(15,2)` |  | NO | None |  |  |
| `valor_pago` | `decimal(15,2)` |  | NO | None |  |  |

---

