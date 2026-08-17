# Estructura de la Base de Datos - Korva Nicaragua
Generado: 2026-07-30 12:33

## Usuarios

### EmailVerificationToken (`users_emailverificationtoken`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | user_id | INTEGER UNSIGNED | NO |  | User |  |
| 3 | token | UUID | NO |  |  |  |
| 4 | created_at | DATETIME | NO |  |  |  |
| 5 | expires_at | DATETIME | NO |  |  |  |

### Profile (`users_profile`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | user_id | INTEGER UNSIGNED | NO |  | User |  |
| 3 | business_name | VARCHAR(255) | NO |  |  |  |
| 4 | logo | VARCHAR(500) | NULL |  |  |  |
| 5 | banner | VARCHAR(500) | NULL |  |  |  |
| 6 | ruc | VARCHAR(255) | NO |  |  |  |
| 7 | verified | BOOLEAN | NO |  |  | DEFAULT FALSE |
| 8 | city | VARCHAR(255) | NO |  |  |  |
| 9 | sector | VARCHAR(255) | NO |  |  |  |
| 10 | popularity_score | INTEGER | NO |  |  | DEFAULT 0 |
| 11 | followers_count | INTEGER | NO |  |  | DEFAULT 0 |
| 12 | associates_count | INTEGER | NO |  |  | DEFAULT 0 |
| 13 | collaborations_count | INTEGER | NO |  |  | DEFAULT 0 |
| 14 | bio | TEXT | NULL |  |  |  |
| 15 | latitude | FLOAT | NULL |  |  |  |
| 16 | longitude | FLOAT | NULL |  |  |  |
| 17 | created_at | DATETIME | NO |  |  |  |
| 18 | updated_at | DATETIME | NO |  |  |  |

### Report (`users_report`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | reporter_id | INTEGER UNSIGNED | NO |  | User |  |
| 3 | reported_id | INTEGER UNSIGNED | NO |  | User |  |
| 4 | reason | VARCHAR(255) | NO |  |  |  |
| 5 | description | TEXT | NO |  |  |  |
| 6 | created_at | DATETIME | NO |  |  |  |
| 7 | resolved | BOOLEAN | NO |  |  | DEFAULT FALSE |

### Block (`users_block`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | blocker_id | INTEGER UNSIGNED | NO |  | User |  |
| 3 | blocked_id | INTEGER UNSIGNED | NO |  | User |  |
| 4 | created_at | DATETIME | NO |  |  |  |

### Profile ↔ Message (`messaging_message_read_by`)

| # | Columna | Tipo | FK |
|---|---------|------|----|
| 1 | message_id | INTEGER UNSIGNED | -> Message |
| 2 | profile_id | INTEGER UNSIGNED | -> Profile |

### Profile ↔ Event (`events_event_attendees`)

| # | Columna | Tipo | FK |
|---|---------|------|----|
| 1 | event_id | INTEGER UNSIGNED | -> Event |
| 2 | profile_id | INTEGER UNSIGNED | -> Profile |

### Profile ↔ Group (`groups_group_members`)

| # | Columna | Tipo | FK |
|---|---------|------|----|
| 1 | group_id | INTEGER UNSIGNED | -> Group |
| 2 | profile_id | INTEGER UNSIGNED | -> Profile |

---

## Red Social

### Post (`social_post`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | title | VARCHAR(255) | NO |  |  |  |
| 3 | content | TEXT | NO |  |  |  |
| 4 | image | VARCHAR(500) | NULL |  |  |  |
| 5 | video | VARCHAR(500) | NULL |  |  |  |
| 6 | author_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 7 | timestamp | DATETIME | NO |  |  |  |
| 8 | updated_at | DATETIME | NO |  |  |  |
| 9 | upvotes | INTEGER | NO |  |  | DEFAULT 0 |
| 10 | downvotes | INTEGER | NO |  |  | DEFAULT 0 |
| 11 | moderation_status | VARCHAR(255) | NO |  |  | DEFAULT 'approved' |
| 12 | moderation_reason | TEXT | NULL |  |  |  |
| 13 | tagged_items | INTEGER UNSIGNED | NULL |  | TaggedItem |  |

### PostImage (`social_postimage`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | post_id | INTEGER UNSIGNED | NO |  | Post |  |
| 3 | image | VARCHAR(500) | NO |  |  |  |
| 4 | uploaded_at | DATETIME | NO |  |  |  |

### Vote (`social_vote`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | user_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | post_id | INTEGER UNSIGNED | NO |  | Post |  |
| 4 | vote_type | VARCHAR(255) | NO |  |  |  |
| 5 | created_at | DATETIME | NO |  |  |  |
| 6 | updated_at | DATETIME | NO |  |  |  |

### Comment (`social_comment`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | post_id | INTEGER UNSIGNED | NO |  | Post |  |
| 3 | author_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 4 | content | TEXT | NO |  |  |  |
| 5 | timestamp | DATETIME | NO |  |  |  |
| 6 | updated_at | DATETIME | NO |  |  |  |
| 7 | upvotes | INTEGER | NO |  |  | DEFAULT 0 |
| 8 | downvotes | INTEGER | NO |  |  | DEFAULT 0 |

### Favorite (`social_favorite`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | user_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | post_id | INTEGER UNSIGNED | NO |  | Post |  |
| 4 | created_at | DATETIME | NO |  |  |  |

### Post ↔ Tag (`taggit_taggeditem`)

| # | Columna | Tipo | FK |
|---|---------|------|----|
| 1 | tag_id | INTEGER UNSIGNED | -> Tag |
| 2 | content_type_id | INTEGER UNSIGNED | -> ContentType |
| 3 | object_id | INTEGER | |
| 4 | content_object | GENERICFOREIGNKEY | |

---

## Marketplace

### Product (`marketplace_product`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | name | VARCHAR(255) | NO |  |  |  |
| 3 | description | TEXT | NO |  |  |  |
| 4 | price | DECIMAL(10,2) | NO |  |  |  |
| 5 | currency | VARCHAR(255) | NO |  |  | DEFAULT 'NIO' |
| 6 | category | VARCHAR(255) | NO |  |  |  |
| 7 | image | VARCHAR(500) | NULL |  |  |  |
| 8 | contact_whatsapp | VARCHAR(255) | NO |  |  |  |
| 9 | user_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 10 | created_at | DATETIME | NO |  |  |  |
| 11 | updated_at | DATETIME | NO |  |  |  |
| 12 | is_active | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 13 | views_count | INTEGER | NO |  |  | DEFAULT 0 |

### ProductFavorite (`marketplace_productfavorite`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | user_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | product_id | INTEGER UNSIGNED | NO |  | Product |  |
| 4 | created_at | DATETIME | NO |  |  |  |

### Review (`marketplace_review`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | reviewer_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | seller_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 4 | product_id | INTEGER UNSIGNED | NULL |  | Product |  |
| 5 | rating | INTEGER | NO |  |  |  |
| 6 | comment | TEXT | NO |  |  |  |
| 7 | created_at | DATETIME | NO |  |  |  |

### Deal (`marketplace_deal`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | product_id | INTEGER UNSIGNED | NO |  | Product |  |
| 3 | seller_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 4 | title | VARCHAR(255) | NO |  |  |  |
| 5 | description | TEXT | NO |  |  |  |
| 6 | discount_percent | INTEGER UNSIGNED | NO |  |  |  |
| 7 | original_price | DECIMAL(10,2) | NO |  |  |  |
| 8 | deal_price | DECIMAL(10,2) | NO |  |  |  |
| 9 | starts_at | DATETIME | NO |  |  |  |
| 10 | ends_at | DATETIME | NO |  |  |  |
| 11 | is_active | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 12 | created_at | DATETIME | NO |  |  |  |

### BankAccount (`marketplace_bankaccount`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | seller_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | bank | VARCHAR(255) | NO |  |  |  |
| 4 | account_type | VARCHAR(255) | NO |  |  | DEFAULT 'monetaria' |
| 5 | account_number | VARCHAR(255) | NO |  |  |  |
| 6 | account_holder | VARCHAR(255) | NO |  |  |  |
| 7 | id_number | VARCHAR(255) | NO |  |  |  |
| 8 | phone | VARCHAR(255) | NO |  |  |  |
| 9 | verified | BOOLEAN | NO |  |  | DEFAULT FALSE |
| 10 | created_at | DATETIME | NO |  |  |  |
| 11 | updated_at | DATETIME | NO |  |  |  |

### Transaction (`marketplace_transaction`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | product_id | INTEGER UNSIGNED | NO |  | Product |  |
| 3 | buyer_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 4 | seller_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 5 | amount | DECIMAL(10,2) | NO |  |  |  |
| 6 | currency | VARCHAR(255) | NO |  |  | DEFAULT 'NIO' |
| 7 | commission_percent | DECIMAL(10,2) | NO |  |  | DEFAULT 5 |
| 8 | commission_amount | DECIMAL(10,2) | NO |  |  |  |
| 9 | seller_amount | DECIMAL(10,2) | NO |  |  |  |
| 10 | reference | VARCHAR(255) | NO |  |  |  |
| 11 | status | VARCHAR(255) | NO |  |  | DEFAULT 'pending' |
| 12 | bank | VARCHAR(255) | NO |  |  |  |
| 13 | payment_date | DATETIME | NULL |  |  |  |
| 14 | buyer_notes | TEXT | NO |  |  |  |
| 15 | created_at | DATETIME | NO |  |  |  |
| 16 | updated_at | DATETIME | NO |  |  |  |

### PayoutRequest (`marketplace_payoutrequest`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | seller_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | amount | DECIMAL(10,2) | NO |  |  |  |
| 4 | bank_account_id | INTEGER UNSIGNED | NULL |  | BankAccount |  |
| 5 | status | VARCHAR(255) | NO |  |  | DEFAULT 'pending' |
| 6 | admin_notes | TEXT | NO |  |  |  |
| 7 | created_at | DATETIME | NO |  |  |  |
| 8 | processed_at | DATETIME | NULL |  |  |  |

---

## Mensajeria

### Message (`messaging_message`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | sender_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | recipient_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 4 | content | TEXT | NO |  |  |  |
| 5 | image | VARCHAR(500) | NULL |  |  |  |
| 6 | video | VARCHAR(500) | NULL |  |  |  |
| 7 | timestamp | DATETIME | NO |  |  |  |

### Conversation (`messaging_conversation`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | user1_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | user2_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 4 | created_at | DATETIME | NO |  |  |  |
| 5 | updated_at | DATETIME | NO |  |  |  |

---

## Notificaciones

### Notification (`notifications_notification`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | recipient_id | INTEGER UNSIGNED | NO |  | User |  |
| 3 | sender_id | INTEGER UNSIGNED | NULL |  | User |  |
| 4 | notification_type | VARCHAR(255) | NO |  |  |  |
| 5 | title | VARCHAR(255) | NO |  |  |  |
| 6 | message | TEXT | NO |  |  |  |
| 7 | related_object_id | INTEGER UNSIGNED | NULL |  |  |  |
| 8 | related_object_type | VARCHAR(255) | NO |  |  |  |
| 9 | is_read | BOOLEAN | NO |  |  | DEFAULT FALSE |
| 10 | created_at | DATETIME | NO |  |  |  |

### NotificationPreference (`notifications_notificationpreference`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | user_id | INTEGER UNSIGNED | NO |  | User |  |
| 3 | email_messages | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 4 | email_likes | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 5 | email_comments | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 6 | email_follows | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 7 | email_product_inquiries | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 8 | email_mentions | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 9 | email_system | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 10 | push_messages | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 11 | push_likes | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 12 | push_comments | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 13 | push_follows | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 14 | push_product_inquiries | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 15 | push_mentions | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 16 | push_system | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 17 | created_at | DATETIME | NO |  |  |  |
| 18 | updated_at | DATETIME | NO |  |  |  |

---

## Core / IA

### KorvaAIConfig (`core_korvaaiconfig`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | user_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | user_api_key | VARCHAR(255) | NULL |  |  |  |
| 4 | grok_api_key | VARCHAR(255) | NULL |  |  |  |
| 5 | uses_personal_key | BOOLEAN | NO |  |  | DEFAULT FALSE |
| 6 | preferred_provider | VARCHAR(255) | NO |  |  | DEFAULT 'gemini' |
| 7 | seen_ai_tutorial | BOOLEAN | NO |  |  | DEFAULT FALSE |
| 8 | total_tokens_used | INTEGER UNSIGNED | NO |  |  | DEFAULT 0 |
| 9 | monthly_token_limit | INTEGER UNSIGNED | NO |  |  | DEFAULT 100000 |
| 10 | created_at | DATETIME | NO |  |  |  |
| 11 | updated_at | DATETIME | NO |  |  |  |

### AIConversation (`core_aiconversation`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | user_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 3 | title | VARCHAR(255) | NO |  |  |  |
| 4 | created_at | DATETIME | NO |  |  |  |
| 5 | updated_at | DATETIME | NO |  |  |  |

### AIMessage (`core_aimessage`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | conversation_id | INTEGER UNSIGNED | NO |  | AIConversation |  |
| 3 | role | VARCHAR(255) | NO |  |  |  |
| 4 | content | TEXT | NO |  |  |  |
| 5 | tokens_used | INTEGER UNSIGNED | NO |  |  | DEFAULT 0 |
| 6 | provider | VARCHAR(255) | NO |  |  | DEFAULT 'gemini' |
| 7 | timestamp | DATETIME | NO |  |  |  |

---

## Eventos

### Event (`events_event`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | title | VARCHAR(255) | NO |  |  |  |
| 3 | description | TEXT | NO |  |  |  |
| 4 | category | VARCHAR(255) | NO |  |  | DEFAULT 'feria' |
| 5 | organizer_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 6 | date | DATE | NO |  |  |  |
| 7 | time | TIME | NULL |  |  |  |
| 8 | location | VARCHAR(255) | NO |  |  |  |
| 9 | city | VARCHAR(255) | NO |  |  | DEFAULT 'managua' |
| 10 | image | VARCHAR(500) | NULL |  |  |  |
| 11 | max_attendees | INTEGER UNSIGNED | NULL |  |  |  |
| 12 | is_active | BOOLEAN | NO |  |  | DEFAULT TRUE |
| 13 | created_at | DATETIME | NO |  |  |  |

---

## Grupos

### Group (`groups_group`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | name | VARCHAR(255) | NO |  |  |  |
| 3 | description | TEXT | NO |  |  |  |
| 4 | sector | VARCHAR(255) | NO |  |  |  |
| 5 | image | VARCHAR(500) | NULL |  |  |  |
| 6 | admin_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 7 | created_at | DATETIME | NO |  |  |  |

### GroupPost (`groups_grouppost`)

| # | Columna | Tipo | Nulo | Clave | FK | Valor por defecto |
|---|---------|------|------|-------|----|-----------------|
| 1 | id | BIG INT AUTO_INCREMENT | NO | PK |  |  |
| 2 | group_id | INTEGER UNSIGNED | NO |  | Group |  |
| 3 | author_id | INTEGER UNSIGNED | NO |  | Profile |  |
| 4 | content | TEXT | NO |  |  |  |
| 5 | image | VARCHAR(500) | NULL |  |  |  |
| 6 | created_at | DATETIME | NO |  |  |  |

---
