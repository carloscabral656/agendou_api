# agendou-api

API FastAPI com Poetry, PostgreSQL, SQLAlchemy (async) e Alembic.

## Variáveis de ambiente

Copie `.env.example` para `.env` e defina pelo menos:

- `DATABASE_URL` — URL async (`postgresql+asyncpg://...`)
- `JWT_SECRET_KEY` — segredo forte (mínimo 32 caracteres recomendado para HS256) para assinar JWT

## Autenticação (JWT stateless)

- **Registro:** `POST /auth/register` com `company_id`, `full_name`, `email`, `password` (a empresa deve existir no banco).
- **Login:** `POST /auth/login` com `email`, `password` e opcionalmente `company_id` (obrigatório se houver mais de um usuário com o mesmo e-mail).
- **Perfil:** `GET /users/me` e `PATCH /users/me` com header `Authorization: Bearer <access_token>`.
- **Logout:** `POST /auth/logout` não invalida o token no servidor. O cliente deve **descartar** o JWT; até expirar, quem tiver o token continua autenticado. Para revogação server-side no futuro, use denylist (ex.: Redis) ou refresh tokens.

## Recuperação de senha

- `POST /auth/forgot-password` — envio de e-mail é stub (log); em produção, configure um adapter de e-mail.
- `POST /auth/reset-password` — `token` (JWT de reset) e `new_password`.

## Desenvolvimento

```bash
poetry install --all-groups
docker compose up -d postgres
cp .env.example .env
poetry run alembic upgrade head
poetry run uvicorn agendou_api.main:app --reload
```

## Exemplo de rota protegida por role

`GET /auth/admin-only-example` exige `company_admin` ou `super_admin`.

## Empresas, configurações e unidades (multi-tenant)

Todas as rotas abaixo com `{company_id}` exigem JWT. Usuários do tenant só acessam a própria empresa (`user.company_id`); `super_admin` acessa qualquer `company_id`.

**Papéis (resumo):**

- `GET` empresa / settings / unidades: `company_admin`, `manager`, `staff`, `super_admin`
- `PATCH` empresa e settings: `company_admin`, `super_admin`
- Criar/editar unidades: `company_admin`, `manager`, `super_admin`
- `DELETE` unidade (desativa, `status=inactive`): `company_admin`, `super_admin`

**Onboarding público (cadastro de empresa + primeiro admin):**

- `POST /companies/onboarding` — sem `Authorization`. Cria empresa, `company_settings` padrão, usuário `company_admin` e devolve `access_token` + dados da empresa e do usuário.

**Outros endpoints:**

- `GET /companies/me` — empresa do usuário autenticado (exige `company_id` no usuário).
- `GET /companies` — lista paginada (`skip`, `limit`); apenas `super_admin`.
- `GET/PATCH /companies/{company_id}`
- `GET/PATCH /companies/{company_id}/settings`
- `GET/POST /companies/{company_id}/units`, `GET/PATCH /companies/{company_id}/units/{unit_id}`, `DELETE ...` (soft delete)

**Telas (cliente HTTP):** use `POST /companies/onboarding` no fluxo de cadastro; guarde o `access_token` e chame as rotas de unidades com `Authorization: Bearer ...` e o `company_id` retornado (ou o do token).

Em produção, proteja o onboarding com rate limiting ou CAPTCHA no gateway.
