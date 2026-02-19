CREATE TABLE users (
  id UUID PRIMARY KEY,
  channel VARCHAR(20) NOT NULL,
  external_user_id VARCHAR(120) NOT NULL,
  display_name VARCHAR(120),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE conversations (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  channel VARCHAR(20) NOT NULL,
  current_state VARCHAR(50) NOT NULL,
  detected_product VARCHAR(30),
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  metadata_json JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE messages (
  id UUID PRIMARY KEY,
  conversation_id UUID REFERENCES conversations(id),
  direction VARCHAR(10) NOT NULL,
  channel VARCHAR(20) NOT NULL,
  message_text TEXT,
  raw_payload_json JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE leads (
  id UUID PRIMARY KEY,
  conversation_id UUID REFERENCES conversations(id),
  user_id UUID REFERENCES users(id),
  product VARCHAR(30) NOT NULL,
  status VARCHAR(20) NOT NULL,
  qualification_answers_json JSONB DEFAULT '{}'::jsonb,
  customer_preference VARCHAR(30) DEFAULT 'nao_informado',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lead_data (
  id UUID PRIMARY KEY,
  lead_id UUID REFERENCES leads(id),
  name BYTEA,
  cpf BYTEA,
  birth_date BYTEA,
  phone VARCHAR(20),
  email VARCHAR(120),
  nis_number BYTEA,
  benefit_amount NUMERIC(10,2),
  company_name VARCHAR(120),
  card_bank VARCHAR(60),
  preferred_installments SMALLINT,
  consent_given BOOLEAN DEFAULT FALSE,
  consent_timestamp TIMESTAMPTZ
);

CREATE TABLE handoffs (
  id UUID PRIMARY KEY,
  lead_id UUID REFERENCES leads(id),
  handoff_payload_json JSONB NOT NULL,
  status VARCHAR(20) NOT NULL,
  assigned_to UUID,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE followups (
  id UUID PRIMARY KEY,
  lead_id UUID REFERENCES leads(id),
  scheduled_for TIMESTAMPTZ NOT NULL,
  sent_at TIMESTAMPTZ,
  template_name VARCHAR(40) NOT NULL,
  status VARCHAR(20) NOT NULL
);

CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  entity_type VARCHAR(30) NOT NULL,
  entity_id UUID NOT NULL,
  action VARCHAR(60) NOT NULL,
  actor_type VARCHAR(20) NOT NULL,
  actor_id UUID,
  before_json JSONB,
  after_json JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);
