# 📦 Documentação do Banco de Dados: `db_almoxarifado`

🤖 **Análise com IA Habilitada (Modelo: gemini-1.5-flash-latest)**

## 🎯 Resumo Executivo do Banco de Dados (Gerado por IA)

Erro ao gerar o resumo automático do banco de dados.

### 📊 Estatísticas Gerais do Banco
- **Total de Tabelas:** 38
- **Total de Linhas (estimado):** 416.418
- **Tamanho Total em Disco (estimado):** 85.97 MB

---
## 📋 Tabela: `almoxarifado`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 109
- **Tamanho em Disco (aprox.):** 0.05 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:11

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | NO | None |  | → `entidade`.`id` |
| `fk_lotacao` | `int` | MUL | NO | None |  | → `lotacao`.`id` |
| `descricao` | `varchar(100)` |  | NO | None |  |  |
| `endereco` | `varchar(100)` |  | YES | None |  |  |

---

## 📋 Tabela: `almoxarife_has_almoxarifado`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 297
- **Tamanho em Disco (aprox.):** 0.05 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:12
- **Última Atualização:** 2025-09-16 18:05:49

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_almoxarife` | `int` | MUL | NO | None |  | → `user`.`id` |
| `fk_almoxarifado` | `int` | MUL | NO | None |  | → `almoxarifado`.`id` |

---

## 📋 Tabela: `aprovador_has_lotacao`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 1.121
- **Tamanho em Disco (aprox.):** 0.09 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:13
- **Última Atualização:** 2025-09-16 18:05:49

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_aprovador` | `int` | MUL | NO | None |  | → `user`.`id` |
| `fk_lotacao` | `int` | MUL | NO | None |  | → `lotacao`.`id` |

---

## 📋 Tabela: `audit_trail_entry`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 83.296
- **Tamanho em Disco (aprox.):** 36.59 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:15
- **Última Atualização:** 2025-09-17 14:10:39

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
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

## 📋 Tabela: `auth_assignment`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 782
- **Tamanho em Disco (aprox.):** 0.11 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:28
- **Última Atualização:** 2025-09-16 18:05:49

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `item_name` | `varchar(64)` | PRI | NO | None |  | → `auth_item`.`name` |
| `user_id` | `int` | PRI | NO | None |  | → `user`.`id` |
| `created_at` | `int` |  | YES | None |  |  |

---

## 📋 Tabela: `auth_item`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 326
- **Tamanho em Disco (aprox.):** 0.09 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:29

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
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

## 📋 Tabela: `auth_item_child`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 134
- **Tamanho em Disco (aprox.):** 0.03 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:30

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `parent` | `varchar(64)` | PRI | NO | None |  | → `auth_item`.`name` |
| `child` | `varchar(64)` | PRI | NO | None |  | → `auth_item`.`name` |

---

## 📋 Tabela: `auth_item_group`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 4
- **Tamanho em Disco (aprox.):** 0.02 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:31

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `code` | `varchar(64)` | PRI | NO | None |  |  |
| `name` | `varchar(255)` |  | NO | None |  |  |
| `created_at` | `int` |  | YES | None |  |  |
| `updated_at` | `int` |  | YES | None |  |  |

---

## 📋 Tabela: `auth_rule`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 0
- **Tamanho em Disco (aprox.):** 0.02 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:33

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `name` | `varchar(64)` | PRI | NO | None |  |  |
| `data` | `text` |  | YES | None |  |  |
| `created_at` | `int` |  | YES | None |  |  |
| `updated_at` | `int` |  | YES | None |  |  |

---

## 📋 Tabela: `cidade`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 5.571
- **Tamanho em Disco (aprox.):** 0.41 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:34

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_estado` | `int` | MUL | NO | None |  | → `estado`.`id` |
| `nome` | `varchar(45)` |  | NO | None |  |  |

---

## 📋 Tabela: `entidade`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 24
- **Tamanho em Disco (aprox.):** 0.05 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:35

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_cidade` | `int` | MUL | NO | None |  | → `cidade`.`id` |
| `nome` | `varchar(100)` |  | NO | None |  |  |
| `cnpj` | `varchar(14)` | UNI | NO | None |  |  |
| `endereco` | `varchar(100)` |  | NO | None |  |  |
| `sigla` | `varchar(50)` |  | NO | None |  |  |
| `brasao` | `text` |  | YES | None |  |  |
| `status` | `tinyint(1)` |  | NO | 1 |  |  |

---

## 📋 Tabela: `estado`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 27
- **Tamanho em Disco (aprox.):** 0.02 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:36

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `nome` | `varchar(45)` |  | NO | None |  |  |
| `uf` | `varchar(2)` |  | NO | None |  |  |

---

## 📋 Tabela: `fornecedor`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 540
- **Tamanho em Disco (aprox.):** 0.17 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:38
- **Última Atualização:** 2025-09-11 13:33:09

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_cidade` | `int` | MUL | YES | None |  | → `cidade`.`id` |
| `fk_estado` | `int` | MUL | YES | None |  | → `estado`.`id` |
| `fk_entidade` | `int` | MUL | NO | None |  | → `entidade`.`id` |
| `cpf_cnpj` | `varchar(14)` |  | NO | None |  |  |
| `nome_razao` | `varchar(100)` |  | NO | None |  |  |
| `endereco` | `varchar(100)` |  | YES | None |  |  |
| `telefone` | `varchar(11)` |  | YES | None |  |  |
| `email` | `varchar(255)` |  | YES | None |  |  |
| `status` | `tinyint(1)` |  | NO | None |  |  |

---

## 📋 Tabela: `inventario`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 36
- **Tamanho em Disco (aprox.):** 0.06 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:39

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_responsavel` | `int` | MUL | NO | None |  | → `user`.`id` |
| `fk_almoxarifado` | `int` | MUL | NO | None |  | → `almoxarifado`.`id` |
| `numero` | `int` | MUL | NO | None |  |  |
| `data_abertura` | `datetime` |  | NO | None |  |  |
| `data_processamento` | `datetime` |  | YES | None |  |  |
| `status` | `tinyint(1)` |  | NO | None |  |  |
| `flag_processamento` | `tinyint(1)` |  | YES | None |  |  |
| `metodo` | `tinyint(1)` |  | YES | None |  |  |

---

## 📋 Tabela: `item_almoxarifado`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 13.420
- **Tamanho em Disco (aprox.):** 2.36 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:40
- **Última Atualização:** 2025-09-17 14:10:39

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_produto` | `int` | MUL | NO | None |  | → `produto`.`id` |
| `fk_lote` | `int` | MUL | YES | None |  | → `lote`.`id` |
| `fk_almoxarifado` | `int` | MUL | NO | None |  | → `almoxarifado`.`id` |
| `quantidade` | `decimal(10,3)` |  | NO | None |  |  |
| `valor_medio` | `decimal(10,3)` |  | YES | None |  |  |

---

## 📋 Tabela: `item_inventario`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 161
- **Tamanho em Disco (aprox.):** 0.06 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:42

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_inventario` | `int` | MUL | NO | None |  | → `inventario`.`id` |
| `fk_produto` | `int` | MUL | NO | None |  | → `produto`.`id` |
| `fk_lote` | `int` | MUL | YES | None |  | → `lote`.`id` |
| `contagem1` | `decimal(10,3)` |  | NO | None |  |  |
| `contagem2` | `decimal(10,3)` |  | YES | None |  |  |

---

## 📋 Tabela: `item_movimentacao`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 130.587
- **Tamanho em Disco (aprox.):** 15.06 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2025-08-11 19:56:25
- **Última Atualização:** 2025-09-17 14:10:39

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_movimentacao_geral` | `int` | MUL | NO | None |  | → `movimentacao_geral`.`id` |
| `fk_produto` | `int` | MUL | NO | None |  | → `produto`.`id` |
| `fk_lote` | `int` | MUL | YES | None |  | → `lote`.`id` |
| `quantidade` | `decimal(10,3)` |  | NO | None |  |  |
| `lote` | `varchar(100)` |  | YES | None |  |  |
| `valor_unitario` | `decimal(12,6)` |  | YES | None |  |  |

---

## 📋 Tabela: `item_requisicao_entrega`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 47.106
- **Tamanho em Disco (aprox.):** 5.55 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:46
- **Última Atualização:** 2025-09-17 14:10:39

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_item_requisicao` | `int` | MUL | NO | None |  | → `itens_requisicao`.`id` |
| `fk_lote` | `int` | MUL | YES | None |  | → `lote`.`id` |
| `quantidade` | `decimal(10,3)` |  | NO | None |  |  |
| `data` | `date` |  | NO | None |  |  |

---

## 📋 Tabela: `item_requisicao_transferencia_entrega`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 1.833
- **Tamanho em Disco (aprox.):** 0.23 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:49
- **Última Atualização:** 2025-09-17 11:48:42

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_item_requisicao` | `int` | MUL | NO | None |  | → `itens_transferencia`.`id` |
| `fk_lote` | `int` | MUL | YES | None |  | → `lote`.`id` |
| `quantidade` | `decimal(10,3)` |  | NO | None |  |  |
| `data` | `date` |  | NO | None |  |  |

---

## 📋 Tabela: `itens_requisicao`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 49.772
- **Tamanho em Disco (aprox.):** 6.55 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:50
- **Última Atualização:** 2025-09-17 14:10:39

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 47
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_requisicao` | `int` | MUL | NO | None |  | → `requisicao`.`id` |
| `fk_produto_servico` | `int` | MUL | NO | None |  | → `produto`.`id` |
| `quantidade_pedida` | `decimal(10,3)` |  | NO | None |  |  |
| `quantidade_autorizada` | `decimal(10,3)` |  | YES | None |  |  |
| `quantidade_entregue` | `decimal(10,3)` |  | YES | None |  |  |
| `quantidade_cancelada` | `decimal(10,3)` |  | YES | None |  |  |
| `status` | `tinyint(1)` |  | NO | None |  |  |
| `motivo` | `varchar(255)` |  | YES | None |  |  |

---

## 📋 Tabela: `itens_transferencia`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 1.850
- **Tamanho em Disco (aprox.):** 0.25 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:53
- **Última Atualização:** 2025-09-17 11:48:42

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_produto_servico` | `int` | MUL | NO | None |  | → `produto`.`id` |
| `fk_requisicao` | `int` | MUL | NO | None |  | → `requisicao_transferencia`.`id` |
| `quantidade_pedida` | `decimal(10,3)` |  | NO | None |  |  |
| `quantidade_cancelada` | `decimal(10,3)` |  | YES | None |  |  |
| `quantidade_entregue` | `decimal(10,3)` |  | YES | None |  |  |
| `status` | `tinyint(1)` |  | NO | None |  |  |

---

## 📋 Tabela: `local_produto`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 1.237
- **Tamanho em Disco (aprox.):** 0.19 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:54

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_almoxarifado` | `int` | MUL | NO | None |  | → `almoxarifado`.`id` |
| `fk_produto` | `int` | MUL | NO | None |  | → `produto`.`id` |
| `descricao` | `varchar(255)` |  | NO | None |  |  |

---

## 📋 Tabela: `lotacao`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 232
- **Tamanho em Disco (aprox.):** 0.03 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:55

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_secretaria` | `int` | MUL | NO | None |  | → `secretaria`.`id` |
| `nome` | `varchar(100)` |  | NO | None |  |  |

---

## 📋 Tabela: `lote`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 4.279
- **Tamanho em Disco (aprox.):** 1.64 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:57
- **Última Atualização:** 2025-09-17 11:23:23

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | NO | None |  | → `entidade`.`id` |
| `nome_fabricante` | `char(50)` |  | NO | None |  |  |
| `numero` | `char(30)` |  | NO | None |  |  |
| `data_fabricacao` | `date` |  | YES | None |  |  |
| `data_validade` | `date` |  | NO | None |  |  |

---

## 📋 Tabela: `migration`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 19
- **Tamanho em Disco (aprox.):** 0.02 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:58

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `version` | `varchar(180)` | PRI | NO | None |  |  |
| `apply_time` | `int` |  | YES | None |  |  |

---

## 📋 Tabela: `movimentacao_geral`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 18.918
- **Tamanho em Disco (aprox.):** 4.75 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:32:59
- **Última Atualização:** 2025-09-17 14:10:39

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_almoxarifado_origem` | `int` | MUL | NO | None |  | → `almoxarifado`.`id` |
| `fk_almoxarifado_destino` | `int` | MUL | YES | None |  | → `almoxarifado`.`id` |
| `fk_inventario` | `int` | MUL | YES | None |  | → `inventario`.`id` |
| `fk_nota_fiscal` | `int` | MUL | YES | None |  | → `nota_fiscal`.`id` |
| `fk_operacao` | `int` | MUL | NO | None |  | → `operacao`.`id` |
| `fk_requisicao` | `int` | MUL | YES | None |  | → `requisicao`.`id` |
| `fk_requisicao_transferencia` | `int` | MUL | YES | None |  | → `requisicao_transferencia`.`id` |
| `fk_movimentador` | `int` | MUL | NO | None |  | → `user`.`id` |
| `fk_lotacao_devolucao` | `int` | MUL | YES | None |  | → `lotacao`.`id` |
| `numero` | `int` | MUL | NO | None |  |  |
| `data` | `datetime` |  | NO | None |  |  |
| `historico` | `text` |  | YES | None |  |  |
| `status` | `tinyint(1)` |  | NO | None |  |  |

---

## 📋 Tabela: `nota_fiscal`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 6.277
- **Tamanho em Disco (aprox.):** 0.44 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2025-07-25 18:33:28
- **Última Atualização:** 2025-09-17 13:30:03

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_fornecedor` | `int` | MUL | NO | None |  | → `fornecedor`.`id` |
| `numero` | `varchar(100)` |  | NO | None |  |  |
| `serie` | `varchar(100)` |  | NO | None |  |  |
| `total` | `decimal(12,2)` |  | NO | 0.00 |  |  |
| `data_emissao` | `date` |  | NO | None |  |  |

---

## 📋 Tabela: `operacao`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 333
- **Tamanho em Disco (aprox.):** 0.08 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:33:03

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | NO | None |  | → `entidade`.`id` |
| `codigo` | `varchar(5)` |  | NO | None |  |  |
| `descricao` | `varchar(255)` |  | NO | None |  |  |
| `tipo` | `tinyint(1)` |  | NO | None |  |  |
| `op_nota` | `tinyint(1)` |  | NO | None |  |  |

---

## 📋 Tabela: `parametros_entidade`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 24
- **Tamanho em Disco (aprox.):** 0.03 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:33:04

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | NO | None |  | → `entidade`.`id` |
| `travar_saldo` | `tinyint(1)` |  | NO | None |  |  |

---

## 📋 Tabela: `produto`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 11.557
- **Tamanho em Disco (aprox.):** 1.86 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2025-07-25 18:33:30
- **Última Atualização:** 2025-09-17 13:29:30

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_tipo_produto` | `int` | MUL | NO | None |  | → `tipo_produto`.`id` |
| `fk_unidade_medida` | `int` | MUL | NO | None |  | → `unidade_medida`.`id` |
| `codigo` | `varchar(20)` |  | NO | None |  |  |
| `descricao` | `varchar(255)` |  | NO | None |  |  |
| `estoque_minimo` | `decimal(10,3)` |  | YES | None |  |  |
| `estoque_maximo` | `decimal(10,3)` |  | YES | None |  |  |
| `prazo_reposicao` | `int` |  | YES | None |  |  |
| `status` | `tinyint(1)` |  | NO | None |  |  |
| `codigo_barras` | `char(255)` |  | YES | None |  |  |

---

## 📋 Tabela: `requisicao`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 18.428
- **Tamanho em Disco (aprox.):** 4.81 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:33:07
- **Última Atualização:** 2025-09-17 14:10:39

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_secretaria` | `int` | MUL | NO | None |  | → `secretaria`.`id` |
| `fk_lotacao` | `int` | MUL | NO | None |  | → `lotacao`.`id` |
| `fk_requisitante` | `int` | MUL | NO | None |  | → `user`.`id` |
| `fk_autorizador` | `int` | MUL | YES | None |  | → `user`.`id` |
| `fk_almoxarifado` | `int` | MUL | NO | None |  | → `almoxarifado`.`id` |
| `motivo` | `text` |  | YES | None |  |  |
| `numero` | `int` | MUL | NO | None |  |  |
| `data_criacao` | `datetime` |  | NO | None |  |  |
| `data_parecer` | `datetime` |  | YES | None |  |  |
| `status` | `tinyint(1)` |  | NO | None |  |  |

---

## 📋 Tabela: `requisicao_transferencia`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 430
- **Tamanho em Disco (aprox.):** 0.09 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:33:09
- **Última Atualização:** 2025-09-17 11:48:42

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_almoxarifado_origem` | `int` | MUL | NO | None |  | → `almoxarifado`.`id` |
| `fk_almoxarifado_destino` | `int` | MUL | NO | None |  | → `almoxarifado`.`id` |
| `fk_requisitante` | `int` | MUL | NO | None |  | → `user`.`id` |
| `data_criacao` | `datetime` |  | NO | None |  |  |
| `numero` | `int` |  | NO | None |  |  |
| `status` | `tinyint(1)` |  | NO | None |  |  |
| `observacoes` | `text` |  | YES | None |  |  |

---

## 📋 Tabela: `secretaria`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 61
- **Tamanho em Disco (aprox.):** 0.03 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:33:10

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | NO | None |  | → `entidade`.`id` |
| `nome` | `varchar(100)` |  | NO | None |  |  |
| `responsavel` | `varchar(100)` |  | NO | None |  |  |
| `sigla` | `varchar(3)` |  | NO | None |  |  |

---

## 📋 Tabela: `tipo_produto`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 169
- **Tamanho em Disco (aprox.):** 0.03 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:33:11
- **Última Atualização:** 2025-09-10 18:01:36

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | NO | None |  | → `entidade`.`id` |
| `descricao` | `varchar(255)` |  | NO | None |  |  |

---

## 📋 Tabela: `unidade_medida`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 269
- **Tamanho em Disco (aprox.):** 0.05 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:33:13

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | NO | None |  | → `entidade`.`id` |
| `descricao` | `varchar(255)` |  | NO | None |  |  |
| `sigla` | `varchar(3)` | MUL | NO | None |  |  |

---

## 📋 Tabela: `user`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 297
- **Tamanho em Disco (aprox.):** 0.14 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:33:14
- **Última Atualização:** 2025-09-17 12:44:35

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_entidade` | `int` | MUL | YES | None |  | → `entidade`.`id` |
| `fk_lotacao` | `int` | MUL | YES | None |  | → `lotacao`.`id` |
| `fk_secretaria` | `int` | MUL | YES | None |  | → `secretaria`.`id` |
| `username` | `varchar(255)` |  | NO | None |  |  |
| `foto` | `text` |  | YES | None |  |  |
| `nome_completo` | `varchar(100)` |  | NO | None |  |  |
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

## 📋 Tabela: `user_lotacao_secundaria`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 200
- **Tamanho em Disco (aprox.):** 0.05 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2025-07-25 18:33:27
- **Última Atualização:** 2025-09-16 18:05:49

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `fk_user` | `int` | MUL | NO | None |  | → `user`.`id` |
| `fk_lotacao` | `int` | MUL | NO | None |  | → `lotacao`.`id` |

---

## 📋 Tabela: `user_visit_log`

### ℹ️ Informações Gerais
- **Motor (Engine):** `InnoDB`
- **Total de Linhas (aprox.):** 16.692
- **Tamanho em Disco (aprox.):** 3.91 MB
- **Collation:** `utf8mb3_general_ci`
- **Data de Criação:** 2024-04-17 22:33:16
- **Última Atualização:** 2025-09-17 13:07:36

### 🤖 Análise da Inteligência Artificial
**> Descrição da Tabela:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Propósito de Negócio:** Erro: 429 You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. [violations {
  quota_metric: "generativelanguage.googleapis.com/generate_content_free_tier_requests"
  quota_id: "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
  quota_dimensions {
    key: "model"
    value: "gemini-1.5-flash"
  }
  quota_dimensions {
    key: "location"
    value: "global"
  }
  quota_value: 50
}
, links {
  description: "Learn more about Gemini API quotas"
  url: "https://ai.google.dev/gemini-api/docs/rate-limits"
}
, retry_delay {
  seconds: 45
}
]

**> Insights sobre Colunas:** *Nenhum insight específico fornecido.*

### 🏗️ Estrutura Detalhada das Colunas
| Nome da Coluna | Tipo de Dado | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |
|---|---|---|---|---|---|---|
| `id` | `int` | PRI | NO | None |  |  |
| `token` | `varchar(255)` |  | NO | None |  |  |
| `ip` | `varchar(15)` |  | NO | None |  |  |
| `language` | `char(2)` |  | NO | None |  |  |
| `user_agent` | `varchar(255)` |  | NO | None |  |  |
| `user_id` | `int` | MUL | YES | None |  |  |
| `visit_time` | `int` |  | NO | None |  |  |
| `browser` | `varchar(30)` |  | YES | None |  |  |
| `os` | `varchar(20)` |  | YES | None |  |  |

---

